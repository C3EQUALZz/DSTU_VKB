//! Windows-реализация — Cryptography API: Next Generation (CNG)
//! через `windows-sys::Win32::Security::Cryptography` (BCrypt).
//!
//! ВНИМАНИЕ: код-каркас. Полная сборка под `x86_64-pc-windows-msvc`
//! требует Windows-машины с MSVC и установленным таргетом. Здесь
//! отрисована структура — Strategy остаётся одинаковой, меняется только
//! движок. При запуске на Windows надо подключить
//! `windows-sys` с `Win32_Security_Cryptography` (уже прописано в
//! Cargo.toml) и реализовать вызовы `BCryptOpenAlgorithmProvider`,
//! `BCryptSetProperty(BCRYPT_CHAINING_MODE, BCRYPT_CHAIN_MODE_CBC)`,
//! `BCryptGenerateSymmetricKey`, `BCryptEncrypt`/`BCryptDecrypt`
//! с `BCRYPT_BLOCK_PADDING`, `BCryptCreateHash` с флагом
//! `BCRYPT_ALG_HANDLE_HMAC_FLAG=0x8` и SHA256-алгоритмом,
//! `BCryptHashData`, `BCryptFinishHash`, `BCryptGenRandom`
//! с `BCRYPT_USE_SYSTEM_PREFERRED_RNG`.
//!
//! Тонкость: имена алгоритмов BCrypt (`BCRYPT_AES_ALGORITHM`,
//! `BCRYPT_SHA256_ALGORITHM`, `BCRYPT_CHAIN_MODE_CBC`) в `windows-sys`
//! экспортируются как `PCWSTR` — `*const u16`. Для `BCryptSetProperty`
//! длину надо считать через `wcslen + 1` (с null-terminator'ом) и
//! умножать на `size_of::<u16>()`.

#![cfg(target_os = "windows")]

use crate::domain::cipher::{CryptoError, SymmetricCryptoProvider};
use crate::domain::key::{AES_KEY_BYTES, HMAC_KEY_BYTES, HMAC_TAG_BYTES, IV_BYTES};

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
        "Windows-провайдер ещё не реализован для операции «{op}». \
         См. крейтовый Cargo.toml — нужна Windows-машина для отладки FFI к BCrypt."
    ))
}

impl SymmetricCryptoProvider for CngProvider {
    fn name(&self) -> &'static str {
        "Windows / CNG (BCrypt) — skeleton"
    }

    fn fill_random(&self, _buf: &mut [u8]) -> Result<(), CryptoError> {
        Err(todo_native("BCryptGenRandom"))
    }

    fn aes_cbc_encrypt(
        &self,
        _key: &[u8; AES_KEY_BYTES],
        _iv: &[u8; IV_BYTES],
        _plaintext: &[u8],
    ) -> Result<Vec<u8>, CryptoError> {
        Err(todo_native("BCryptEncrypt"))
    }

    fn aes_cbc_decrypt(
        &self,
        _key: &[u8; AES_KEY_BYTES],
        _iv: &[u8; IV_BYTES],
        _ciphertext: &[u8],
    ) -> Result<Vec<u8>, CryptoError> {
        Err(todo_native("BCryptDecrypt"))
    }

    fn hmac_sha256(
        &self,
        _key: &[u8; HMAC_KEY_BYTES],
        _data: &[u8],
    ) -> Result<[u8; HMAC_TAG_BYTES], CryptoError> {
        Err(todo_native("BCryptCreateHash/BCryptHashData/BCryptFinishHash"))
    }
}
