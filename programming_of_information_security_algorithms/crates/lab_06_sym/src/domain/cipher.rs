//! Доменный контракт для симметричного провайдера — это паттерн Strategy:
//! одна и та же логика usecase'ов работает поверх любой реализации,
//! а конкретная реализация выбирается по платформе.
//!
//! Все методы — fallible и возвращают [`CryptoError`]. В реализациях
//! не должно быть `panic!`/`unwrap()` — ошибки нативного API нужно
//! аккуратно прокидывать наверх.

use thiserror::Error;

use crate::domain::key::{
    AES_BLOCK_BYTES, AES_KEY_BYTES, HMAC_KEY_BYTES, HMAC_TAG_BYTES, IV_BYTES, SymmetricKey,
};

#[derive(Debug, Error)]
pub enum CryptoError {
    #[error("системный криптопровайдер вернул ошибку: {0}")]
    Native(String),
    #[error("плохой шифртекст: {0}")]
    BadCiphertext(String),
    #[error("MAC не совпал — шифртекст подделан или ключ неверен")]
    MacMismatch,
    #[error("ошибка ввода-вывода: {0}")]
    Io(#[from] std::io::Error),
}

/// Trait Strategy для криптопровайдеров: всё, что нужно от системного API.
///
/// Реализации:
/// - [`crate::infrastructure::providers::active`] выбирается компиляционно;
/// - на macOS — обёртка над CommonCrypto;
/// - на Linux — `openssl` поверх системного libcrypto;
/// - на Windows — CNG через `windows-sys`.
pub trait SymmetricCryptoProvider {
    /// Имя провайдера (для логов и UI).
    fn name(&self) -> &'static str;

    /// Источник случайных байт. Системный, не статическое seeding.
    ///
    /// # Errors
    /// Если системный RNG отказал.
    fn fill_random(&self, buf: &mut [u8]) -> Result<(), CryptoError>;

    /// Генерирует свежий симметричный ключ (AES + HMAC).
    fn generate_key(&self) -> Result<SymmetricKey, CryptoError> {
        let mut aes = [0u8; AES_KEY_BYTES];
        let mut hmac = [0u8; HMAC_KEY_BYTES];
        self.fill_random(&mut aes)?;
        self.fill_random(&mut hmac)?;
        Ok(SymmetricKey::from_parts(aes, hmac))
    }

    /// AES-256-CBC шифрование с PKCS#7 padding'ом.
    ///
    /// # Errors
    /// — Ошибка системного API.
    fn aes_cbc_encrypt(
        &self,
        key: &[u8; AES_KEY_BYTES],
        iv: &[u8; IV_BYTES],
        plaintext: &[u8],
    ) -> Result<Vec<u8>, CryptoError>;

    /// AES-256-CBC расшифрование с PKCS#7 padding'ом.
    ///
    /// # Errors
    /// — Ошибка системного API (включая неверный padding на чужом ключе).
    fn aes_cbc_decrypt(
        &self,
        key: &[u8; AES_KEY_BYTES],
        iv: &[u8; IV_BYTES],
        ciphertext: &[u8],
    ) -> Result<Vec<u8>, CryptoError>;

    /// HMAC-SHA-256.
    ///
    /// # Errors
    /// — Ошибка системного API.
    fn hmac_sha256(
        &self,
        key: &[u8; HMAC_KEY_BYTES],
        data: &[u8],
    ) -> Result<[u8; HMAC_TAG_BYTES], CryptoError>;
}

/// Высокоуровневая операция: encrypt-then-MAC.
///
/// Возвращает «сырое тело» шифртекста = `IV || ciphertext || HMAC(IV || ciphertext)`.
/// Magic-заголовок добавляется в [`crate::infrastructure::storage`].
///
/// # Errors
/// Любая ошибка провайдера.
pub fn seal(
    provider: &dyn SymmetricCryptoProvider,
    key: &SymmetricKey,
    plaintext: &[u8],
) -> Result<Vec<u8>, CryptoError> {
    let mut iv = [0u8; IV_BYTES];
    provider.fill_random(&mut iv)?;
    let ct = provider.aes_cbc_encrypt(&key.aes, &iv, plaintext)?;
    let mut to_mac = Vec::with_capacity(IV_BYTES + ct.len());
    to_mac.extend_from_slice(&iv);
    to_mac.extend_from_slice(&ct);
    let mac = provider.hmac_sha256(&key.hmac, &to_mac)?;
    let mut out = Vec::with_capacity(to_mac.len() + HMAC_TAG_BYTES);
    out.extend_from_slice(&to_mac);
    out.extend_from_slice(&mac);
    Ok(out)
}

/// Обратное к [`seal`]: проверяет MAC и расшифровывает.
///
/// # Errors
/// `CryptoError::MacMismatch` если MAC не совпал; `BadCiphertext` для
/// структурных ошибок; `Native` для ошибок системного API.
pub fn open(
    provider: &dyn SymmetricCryptoProvider,
    key: &SymmetricKey,
    raw: &[u8],
) -> Result<Vec<u8>, CryptoError> {
    let min_len = IV_BYTES + AES_BLOCK_BYTES + HMAC_TAG_BYTES;
    if raw.len() < min_len {
        return Err(CryptoError::BadCiphertext(format!(
            "тело шифртекста короче {min_len} байт"
        )));
    }
    let mac_offset = raw.len() - HMAC_TAG_BYTES;
    let (to_check, tag_bytes) = raw.split_at(mac_offset);
    let expected: &[u8; HMAC_TAG_BYTES] = tag_bytes.try_into().expect("split_at гарантирует длину");

    let computed = provider.hmac_sha256(&key.hmac, to_check)?;
    if !constant_time_eq(&computed, expected) {
        return Err(CryptoError::MacMismatch);
    }
    let iv: &[u8; IV_BYTES] = to_check[..IV_BYTES]
        .try_into()
        .expect("длина IV проверена выше");
    let ct = &to_check[IV_BYTES..];
    provider.aes_cbc_decrypt(&key.aes, iv, ct)
}

/// Сравнение байтов без раннего выхода — защита от timing-side-channel.
fn constant_time_eq(a: &[u8], b: &[u8]) -> bool {
    if a.len() != b.len() {
        return false;
    }
    let mut diff: u8 = 0;
    for (x, y) in a.iter().zip(b.iter()) {
        diff |= x ^ y;
    }
    diff == 0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn constant_time_eq_basic() {
        assert!(constant_time_eq(b"abc", b"abc"));
        assert!(!constant_time_eq(b"abc", b"abd"));
        assert!(!constant_time_eq(b"abc", b"abcd"));
    }
}
