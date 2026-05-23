//! Доменный контракт для асимметричного провайдера: паттерн Strategy.
//!
//! Ключи и шифртекст наружу всегда представлены в виде `Vec<u8>`. Формат
//! ключей выбран **PKCS#1 DER** — его понимают и macOS Security framework,
//! и OpenSSL, и Windows CNG. Поверх него мы добавляем magic-заголовок
//! (см. [`crate::domain::keys`]), чтобы файл нельзя было перепутать.

use thiserror::Error;

#[derive(Debug, Error)]
pub enum CryptoError {
    #[error("системный криптопровайдер вернул ошибку: {0}")]
    Native(String),
    #[error("неверный формат ключа: {0}")]
    BadKeyFormat(String),
    #[error("блок plaintext'а слишком длинный для текущего модуля ({size} > max {max})")]
    PlaintextTooLong { size: usize, max: usize },
}

/// Сырое представление ключей — DER в формате PKCS#1.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RawPublicKey {
    pub bits: usize,
    /// PKCS#1 DER bytes (`RSAPublicKey`).
    pub der: Vec<u8>,
}

/// Сырое представление приватного ключа — PKCS#1 DER (`RSAPrivateKey`).
#[derive(Clone, PartialEq, Eq)]
pub struct RawPrivateKey {
    pub bits: usize,
    pub der: Vec<u8>,
}

// Никогда не печатаем приватный DER в Debug-логах.
impl std::fmt::Debug for RawPrivateKey {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("RawPrivateKey")
            .field("bits", &self.bits)
            .field("der", &"<redacted>")
            .finish()
    }
}

/// Сгенерированная пара ключей.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RawKeyPair {
    pub public: RawPublicKey,
    pub private: RawPrivateKey,
}

/// Trait Strategy для асимметричного криптопровайдера.
pub trait AsymmetricCryptoProvider {
    fn name(&self) -> &'static str;

    /// Генерирует RSA-пару заданного размера модуля. Стандарт — 2048.
    ///
    /// # Errors
    /// Если системный API не смог сгенерировать ключ.
    fn generate_rsa_keypair(&self, bits: usize) -> Result<RawKeyPair, CryptoError>;

    /// Шифрует один блок открытым ключом по схеме **RSA-OAEP** с MGF1-SHA-256.
    ///
    /// Размер блока: `bits/8 − 2·hashLen − 2 = bits/8 − 66` байт для SHA-256.
    /// Для модуля 2048 бит ⇒ ≤ 190 байт plaintext'а за раз.
    ///
    /// # Errors
    /// Если блок слишком длинный или системный API отказал.
    fn rsa_oaep_encrypt(
        &self,
        public: &RawPublicKey,
        plaintext: &[u8],
    ) -> Result<Vec<u8>, CryptoError>;

    /// Расшифровывает один OAEP-блок закрытым ключом.
    ///
    /// # Errors
    /// Если шифртекст битый или подан не тот ключ.
    fn rsa_oaep_decrypt(
        &self,
        private: &RawPrivateKey,
        ciphertext: &[u8],
    ) -> Result<Vec<u8>, CryptoError>;
}
