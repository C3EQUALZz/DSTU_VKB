//! Windows-реализация — каркас FFI к CNG/NCrypt. Не реализовано.
//!
//! План: использовать `windows-sys::Win32::Security::Cryptography::NCrypt*`:
//! - `NCryptOpenStorageProvider(MS_KEY_STORAGE_PROVIDER)` — открыть KSP.
//! - `NCryptCreatePersistedKey(BCRYPT_RSA_ALGORITHM, 2048)` для генерации.
//! - `NCryptExportKey(BCRYPT_RSAPUBLIC_BLOB / RSAPRIVATE_BLOB)` — экспорт.
//! - `NCryptEncrypt` / `NCryptDecrypt` с `BCRYPT_PAD_OAEP` и
//!   `BCRYPT_OAEP_PADDING_INFO { pszAlgId = BCRYPT_SHA256_ALGORITHM }`.

#![cfg(target_os = "windows")]

use crate::domain::cipher::{
    AsymmetricCryptoProvider, CryptoError, RawKeyPair, RawPrivateKey, RawPublicKey,
};

pub struct CngProvider;

impl CngProvider {
    #[must_use]
    pub const fn new() -> Self {
        Self
    }
}

impl Default for CngProvider {
    fn default() -> Self {
        Self::new()
    }
}

fn todo_native(op: &str) -> CryptoError {
    CryptoError::Native(format!(
        "Windows-провайдер (NCrypt) ещё не реализован для операции «{op}»."
    ))
}

impl AsymmetricCryptoProvider for CngProvider {
    fn name(&self) -> &'static str {
        "Windows / CNG (NCrypt) — skeleton"
    }

    fn generate_rsa_keypair(&self, _bits: usize) -> Result<RawKeyPair, CryptoError> {
        Err(todo_native("NCryptCreatePersistedKey + NCryptExportKey"))
    }

    fn rsa_oaep_encrypt(
        &self,
        _public: &RawPublicKey,
        _plaintext: &[u8],
    ) -> Result<Vec<u8>, CryptoError> {
        Err(todo_native("NCryptEncrypt with BCRYPT_PAD_OAEP"))
    }

    fn rsa_oaep_decrypt(
        &self,
        _private: &RawPrivateKey,
        _ciphertext: &[u8],
    ) -> Result<Vec<u8>, CryptoError> {
        Err(todo_native("NCryptDecrypt with BCRYPT_PAD_OAEP"))
    }
}
