//! Linux-реализация — поверх системного `libcrypto` (OpenSSL).
//!
//! Крейт `openssl` динамически линкуется с `libssl-dev`/`openssl-libs`
//! из вашего дистрибутива. С точки зрения условия лаб 6 это
//! «встроенный в ОС функционал» — мы не реализуем AES/HMAC сами,
//! а делегируем системному криптомодулю.

#![cfg(target_os = "linux")]

use openssl::hash::MessageDigest;
use openssl::pkey::PKey;
use openssl::rand::rand_bytes;
use openssl::sign::Signer;
use openssl::symm::{Cipher, decrypt as ossl_decrypt, encrypt as ossl_encrypt};

use crate::domain::cipher::{CryptoError, SymmetricCryptoProvider};
use crate::domain::key::{AES_KEY_BYTES, HMAC_KEY_BYTES, HMAC_TAG_BYTES, IV_BYTES};

pub struct OpenSslProvider;

impl OpenSslProvider {
    #[must_use]
    pub const fn new() -> Self {
        Self
    }
}

impl Default for OpenSslProvider {
    fn default() -> Self {
        Self::new()
    }
}

fn map_err<E: std::fmt::Display>(e: E) -> CryptoError {
    CryptoError::Native(e.to_string())
}

impl SymmetricCryptoProvider for OpenSslProvider {
    fn name(&self) -> &'static str {
        "Linux / OpenSSL (system libcrypto)"
    }

    fn fill_random(&self, buf: &mut [u8]) -> Result<(), CryptoError> {
        rand_bytes(buf).map_err(map_err)
    }

    fn aes_cbc_encrypt(
        &self,
        key: &[u8; AES_KEY_BYTES],
        iv: &[u8; IV_BYTES],
        plaintext: &[u8],
    ) -> Result<Vec<u8>, CryptoError> {
        ossl_encrypt(Cipher::aes_256_cbc(), key, Some(iv), plaintext).map_err(map_err)
    }

    fn aes_cbc_decrypt(
        &self,
        key: &[u8; AES_KEY_BYTES],
        iv: &[u8; IV_BYTES],
        ciphertext: &[u8],
    ) -> Result<Vec<u8>, CryptoError> {
        ossl_decrypt(Cipher::aes_256_cbc(), key, Some(iv), ciphertext).map_err(map_err)
    }

    fn hmac_sha256(
        &self,
        key: &[u8; HMAC_KEY_BYTES],
        data: &[u8],
    ) -> Result<[u8; HMAC_TAG_BYTES], CryptoError> {
        let pk = PKey::hmac(key).map_err(map_err)?;
        let mut signer = Signer::new(MessageDigest::sha256(), &pk).map_err(map_err)?;
        signer.update(data).map_err(map_err)?;
        let mut out = [0u8; HMAC_TAG_BYTES];
        let written = signer.sign(&mut out).map_err(map_err)?;
        debug_assert_eq!(written, HMAC_TAG_BYTES);
        Ok(out)
    }
}
