//! Сценарии (use cases) приложения. Каждый — тонкая обёртка над доменом
//! и инфраструктурой, отвечает только за оркестрацию.

use std::path::Path;

use color_eyre::eyre::WrapErr;
use color_eyre::{Result, eyre::eyre};
use tracing::{info, instrument};

use crate::domain::bigint::RandomSource;
use crate::domain::rsa::{self, KeyPair, PrivateKey, PublicKey};
use crate::infrastructure::storage;

/// Сценарий: сгенерировать пару ключей и записать в два файла.
pub struct GenerateKeysUseCase<'r, R: RandomSource> {
    pub rng: &'r mut R,
}

impl<R: RandomSource> GenerateKeysUseCase<'_, R> {
    /// Выполняет генерацию.
    ///
    /// # Errors
    /// Любые ошибки записи файлов.
    #[instrument(level = "info", skip(self), fields(bits))]
    pub fn run(&mut self, bits: usize, public_path: &Path, private_path: &Path) -> Result<KeyPair> {
        info!("generating RSA key pair");
        let kp = KeyPair::generate(bits, self.rng);
        storage::save_public_key(&kp.public, public_path)
            .wrap_err_with(|| format!("сохранение публичного ключа в {public_path:?}"))?;
        storage::save_private_key(&kp.private, private_path)
            .wrap_err_with(|| format!("сохранение приватного ключа в {private_path:?}"))?;
        info!(
            n_bits = kp.public.n.bit_length(),
            public_path = ?public_path,
            private_path = ?private_path,
            "RSA keys generated and saved"
        );
        Ok(kp)
    }
}

/// Сценарий: прочитать публичный ключ + plaintext-файл → записать шифртекст.
pub struct EncryptUseCase;

impl EncryptUseCase {
    /// # Errors
    /// Чтение/запись файлов, ошибки шифрования (блок слишком большой и т.п.).
    #[instrument(level = "info", fields(input = ?input, output = ?output))]
    pub fn run(public_path: &Path, input: &Path, output: &Path) -> Result<(PublicKey, Vec<u8>)> {
        let public = storage::load_public_key(public_path)
            .wrap_err_with(|| format!("чтение публичного ключа из {public_path:?}"))?;
        let plaintext = storage::load_bytes(input)
            .wrap_err_with(|| format!("чтение plaintext из {input:?}"))?;
        let ciphertext = rsa::encrypt(&public, &plaintext).map_err(|e| eyre!("шифрование: {e}"))?;
        storage::save_bytes(&ciphertext, output)
            .wrap_err_with(|| format!("запись шифртекста в {output:?}"))?;
        info!(
            plaintext_bytes = plaintext.len(),
            ciphertext_bytes = ciphertext.len(),
            "encryption completed"
        );
        Ok((public, ciphertext))
    }
}

/// Сценарий: прочитать приватный ключ + шифртекст → восстановить plaintext.
///
/// По требованию условия plaintext выводится на экран *и* записывается рядом
/// в файл (если указан путь для копии).
pub struct DecryptUseCase;

impl DecryptUseCase {
    /// # Errors
    /// Чтение файлов и/или ошибки расшифровки (битый формат, не тот ключ).
    #[instrument(level = "info", fields(input = ?input))]
    pub fn run(
        private_path: &Path,
        input: &Path,
        output: Option<&Path>,
    ) -> Result<(PrivateKey, Vec<u8>)> {
        let private = storage::load_private_key(private_path)
            .wrap_err_with(|| format!("чтение приватного ключа из {private_path:?}"))?;
        let ciphertext = storage::load_bytes(input)
            .wrap_err_with(|| format!("чтение шифртекста из {input:?}"))?;
        let plaintext =
            rsa::decrypt(&private, &ciphertext).map_err(|e| eyre!("расшифрование: {e}"))?;
        if let Some(out) = output {
            storage::save_bytes(&plaintext, out)
                .wrap_err_with(|| format!("запись plaintext в {out:?}"))?;
            info!(output = ?out, "plaintext copy saved");
        }
        info!(plaintext_bytes = plaintext.len(), "decryption completed");
        Ok((private, plaintext))
    }
}

#[cfg(test)]
mod tests {
    use std::fs;

    use super::*;
    use crate::domain::rng::DeterministicRng;

    fn tmp_path(name: &str) -> std::path::PathBuf {
        let pid = std::process::id();
        let nanos = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .map(|d| d.subsec_nanos())
            .unwrap_or(0);
        std::env::temp_dir().join(format!("psia_lab01_{name}_{pid}_{nanos}"))
    }

    #[test]
    fn end_to_end_through_disk() {
        let pubk = tmp_path("pub");
        let privk = tmp_path("priv");
        let plain = tmp_path("plain");
        let ct = tmp_path("ct");
        let plain_out = tmp_path("plain_out");

        let plaintext_bytes = "Hello, RSA! Лабораторная 1.".as_bytes();
        fs::write(&plain, plaintext_bytes).unwrap();

        let mut rng = DeterministicRng::new(0xCAFE_F00D);
        GenerateKeysUseCase { rng: &mut rng }
            .run(128, &pubk, &privk)
            .unwrap();
        EncryptUseCase::run(&pubk, &plain, &ct).unwrap();
        let (_, decrypted) = DecryptUseCase::run(&privk, &ct, Some(&plain_out)).unwrap();

        assert_eq!(decrypted, plaintext_bytes);
        assert_eq!(fs::read(&plain_out).unwrap(), decrypted);

        for p in [pubk, privk, plain, ct, plain_out] {
            let _ = fs::remove_file(p);
        }
    }
}
