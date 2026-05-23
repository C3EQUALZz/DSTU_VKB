//! Сценарии лаб 7. Работают с `&dyn AsymmetricCryptoProvider`,
//! поэтому код одинаков на всех ОС.

use std::path::Path;

use color_eyre::Result;
use color_eyre::eyre::WrapErr;
use tracing::{info, instrument};

use crate::domain::cipher::AsymmetricCryptoProvider;
use crate::infrastructure::storage;

pub struct GenerateKeysUseCase;

impl GenerateKeysUseCase {
    /// # Errors
    /// Если провайдер отказался или диск недоступен.
    #[instrument(level = "info", skip(provider))]
    pub fn run(
        provider: &dyn AsymmetricCryptoProvider,
        bits: usize,
        public_path: &Path,
        private_path: &Path,
    ) -> Result<()> {
        info!(provider = provider.name(), bits, "generating RSA key pair");
        let kp = provider.generate_rsa_keypair(bits)?;
        storage::save_public(&kp.public, public_path)?;
        storage::save_private(&kp.private, private_path)?;
        info!(
            public = %public_path.display(),
            private = %private_path.display(),
            "keys saved"
        );
        Ok(())
    }
}

pub struct EncryptUseCase;

impl EncryptUseCase {
    /// # Errors
    /// Ошибка чтения файла, шифрования или записи.
    #[instrument(level = "info", skip(provider))]
    pub fn run(
        provider: &dyn AsymmetricCryptoProvider,
        public_path: &Path,
        input: &Path,
        output: &Path,
    ) -> Result<usize> {
        let public = storage::load_public(public_path)?;
        let plaintext =
            std::fs::read(input).wrap_err_with(|| format!("чтение {}", input.display()))?;
        let ct = provider.rsa_oaep_encrypt(&public, &plaintext)?;
        storage::save_ciphertext(&ct, output)?;
        info!(
            plaintext_bytes = plaintext.len(),
            ciphertext_bytes = ct.len(),
            "file encrypted"
        );
        Ok(ct.len())
    }
}

pub struct DecryptUseCase;

impl DecryptUseCase {
    /// # Errors
    /// Если ключ не подходит, шифртекст битый или диск недоступен.
    #[instrument(level = "info", skip(provider))]
    pub fn run(
        provider: &dyn AsymmetricCryptoProvider,
        private_path: &Path,
        input: &Path,
        output: &Path,
    ) -> Result<usize> {
        let private = storage::load_private(private_path)?;
        let payload = storage::load_ciphertext(input)?;
        let plaintext = provider.rsa_oaep_decrypt(&private, &payload)?;
        std::fs::write(output, &plaintext)
            .wrap_err_with(|| format!("запись {}", output.display()))?;
        info!(plaintext_bytes = plaintext.len(), "file decrypted");
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
        std::env::temp_dir().join(format!("psia_lab07_uc_{name}_{pid}_{nanos}"))
    }

    #[test]
    #[cfg_attr(target_os = "windows", ignore = "Windows-провайдер ещё каркас")]
    fn end_to_end_through_active_provider() {
        let pubk = tmp("pub");
        let privk = tmp("priv");
        let plain = tmp("plain.txt");
        let ct = tmp("ct.bin");
        let recovered = tmp("plain.dec");

        let payload = "Привет, RSA-OAEP!";
        fs::write(&plain, payload).unwrap();

        let p = active();
        GenerateKeysUseCase::run(&p, 2048, &pubk, &privk).unwrap();
        EncryptUseCase::run(&p, &pubk, &plain, &ct).unwrap();
        DecryptUseCase::run(&p, &privk, &ct, &recovered).unwrap();

        assert_eq!(fs::read_to_string(&recovered).unwrap(), payload);

        for f in [pubk, privk, plain, ct, recovered] {
            let _ = fs::remove_file(f);
        }
    }
}
