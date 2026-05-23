//! Тонкие сценарии. Берут провайдер по ссылке на trait-объект —
//! поэтому работают одинаково на всех ОС.

use std::path::Path;

use color_eyre::Result;
use color_eyre::eyre::WrapErr;
use tracing::{info, instrument};

use crate::domain::cipher::{SymmetricCryptoProvider, open, seal};
use crate::domain::key::SymmetricKey;
use crate::infrastructure::storage;

/// Генерация ключа и сохранение в файл.
pub struct GenerateKeyUseCase;

impl GenerateKeyUseCase {
    /// # Errors
    /// Если провайдер не смог дать случайные байты, либо ошибка IO.
    #[instrument(level = "info", skip(provider), fields(path = %path.display()))]
    pub fn run(provider: &dyn SymmetricCryptoProvider, path: &Path) -> Result<SymmetricKey> {
        info!(provider = provider.name(), "generating symmetric key");
        let key = provider.generate_key()?;
        storage::save_key(&key, path)
            .wrap_err_with(|| format!("сохранение ключа в {}", path.display()))?;
        info!("key saved");
        Ok(key)
    }
}

pub struct EncryptUseCase;

impl EncryptUseCase {
    /// # Errors
    /// Если файлы недоступны или шифрование не удалось.
    #[instrument(level = "info", skip(provider), fields(
        provider = provider.name(),
        input = %input.display(),
        output = %output.display()
    ))]
    pub fn run(
        provider: &dyn SymmetricCryptoProvider,
        key_path: &Path,
        input: &Path,
        output: &Path,
    ) -> Result<usize> {
        let key = storage::load_key(key_path)?;
        let plaintext =
            std::fs::read(input).wrap_err_with(|| format!("чтение {}", input.display()))?;
        let raw = seal(provider, &key, &plaintext)?;
        storage::save_ciphertext(&raw, output)?;
        info!(
            plaintext_bytes = plaintext.len(),
            ciphertext_bytes = raw.len(),
            "file encrypted"
        );
        Ok(raw.len())
    }
}

pub struct DecryptUseCase;

impl DecryptUseCase {
    /// # Errors
    /// Если MAC не совпал, файл повреждён или ключ не подходит.
    #[instrument(level = "info", skip(provider), fields(
        provider = provider.name(),
        input = %input.display(),
        output = %output.display()
    ))]
    pub fn run(
        provider: &dyn SymmetricCryptoProvider,
        key_path: &Path,
        input: &Path,
        output: &Path,
    ) -> Result<usize> {
        let key = storage::load_key(key_path)?;
        let raw = storage::load_ciphertext(input)?;
        let plaintext = open(provider, &key, &raw)?;
        std::fs::write(output, &plaintext)
            .wrap_err_with(|| format!("запись {}", output.display()))?;
        info!(
            plaintext_bytes = plaintext.len(),
            ciphertext_bytes = raw.len(),
            "file decrypted"
        );
        Ok(plaintext.len())
    }
}

#[cfg(test)]
mod tests {
    use std::fs;
    use std::path::PathBuf;

    use super::*;
    use crate::infrastructure::providers::active;

    fn tmp(name: &str) -> PathBuf {
        let pid = std::process::id();
        let nanos = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .map(|d| d.subsec_nanos())
            .unwrap_or(0);
        std::env::temp_dir().join(format!("psia_lab06_uc_{name}_{pid}_{nanos}"))
    }

    #[test]
    fn end_to_end_through_active_provider() {
        let key_path = tmp("key");
        let plain = tmp("plain.txt");
        let ct = tmp("ct.bin");
        let recovered = tmp("plain.dec");

        let plaintext = "Привет, симметричное шифрование 6!\nMulti-line.".as_bytes();
        fs::write(&plain, plaintext).unwrap();

        let p = active();
        GenerateKeyUseCase::run(&p, &key_path).unwrap();
        EncryptUseCase::run(&p, &key_path, &plain, &ct).unwrap();
        DecryptUseCase::run(&p, &key_path, &ct, &recovered).unwrap();

        assert_eq!(fs::read(&recovered).unwrap(), plaintext);

        for path in [key_path, plain, ct, recovered] {
            let _ = fs::remove_file(path);
        }
    }

    #[test]
    fn corrupted_ciphertext_fails_mac() {
        let key_path = tmp("key2");
        let plain = tmp("plain2.txt");
        let ct = tmp("ct2.bin");
        let recovered = tmp("plain2.dec");

        fs::write(&plain, b"some payload").unwrap();
        let p = active();
        GenerateKeyUseCase::run(&p, &key_path).unwrap();
        EncryptUseCase::run(&p, &key_path, &plain, &ct).unwrap();

        // Меняем один байт ближе к концу — точно в области HMAC.
        let mut bytes = fs::read(&ct).unwrap();
        let last = bytes.len() - 1;
        bytes[last] ^= 0xFF;
        fs::write(&ct, &bytes).unwrap();

        let err = DecryptUseCase::run(&p, &key_path, &ct, &recovered).unwrap_err();
        let msg = format!("{err:#}");
        assert!(
            msg.contains("MAC") || msg.contains("подделан"),
            "ожидалось MAC mismatch, получено: {msg}"
        );

        for path in [key_path, plain, ct, recovered] {
            let _ = fs::remove_file(path);
        }
    }
}
