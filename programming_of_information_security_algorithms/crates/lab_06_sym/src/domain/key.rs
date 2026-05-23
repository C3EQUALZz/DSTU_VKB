//! Симметричный ключ для AES-256-CBC + HMAC-SHA-256 (encrypt-then-MAC).
//!
//! Ключ состоит из двух частей по 32 байта: один для AES, второй для HMAC.
//! Использование двух раздельных ключей — стандартная практика и стандарт
//! безопасности (см. RFC 7518 §5.2): не использовать один и тот же ключ
//! для шифрования и MAC.

/// Длина блока AES в байтах.
pub const AES_BLOCK_BYTES: usize = 16;
/// Длина AES-256 ключа.
pub const AES_KEY_BYTES: usize = 32;
/// Длина HMAC-SHA-256 ключа.
pub const HMAC_KEY_BYTES: usize = 32;
/// Длина IV для CBC.
pub const IV_BYTES: usize = AES_BLOCK_BYTES;
/// Длина HMAC-SHA-256.
pub const HMAC_TAG_BYTES: usize = 32;

/// Magic-заголовок файла ключа (16 байт).
pub const KEY_MAGIC: &[u8; 16] = b"PSIA-LAB6-AES\x00\x00\x00";
/// Magic-заголовок файла шифртекста (16 байт).
pub const CIPHERTEXT_MAGIC: &[u8; 16] = b"PSIA-LAB6-CTXT\x00\x00";

/// Симметричный ключ.
#[derive(Clone, PartialEq, Eq)]
pub struct SymmetricKey {
    pub aes: [u8; AES_KEY_BYTES],
    pub hmac: [u8; HMAC_KEY_BYTES],
}

impl SymmetricKey {
    /// Создаёт ключ из готовых байт. Используется только в тестах
    /// и при чтении из файла; на проде новый ключ генерится провайдером.
    #[must_use]
    pub const fn from_parts(aes: [u8; AES_KEY_BYTES], hmac: [u8; HMAC_KEY_BYTES]) -> Self {
        Self { aes, hmac }
    }

    /// Сериализует ключ в файл: magic + 32 байта AES + 32 байта HMAC.
    #[must_use]
    pub fn to_file_bytes(&self) -> Vec<u8> {
        let mut out = Vec::with_capacity(KEY_MAGIC.len() + AES_KEY_BYTES + HMAC_KEY_BYTES);
        out.extend_from_slice(KEY_MAGIC);
        out.extend_from_slice(&self.aes);
        out.extend_from_slice(&self.hmac);
        out
    }

    /// Десериализует ключ из файла.
    ///
    /// # Errors
    /// Если magic не совпадает или длина файла неверна.
    pub fn from_file_bytes(bytes: &[u8]) -> Result<Self, KeyFormatError> {
        let expected_len = KEY_MAGIC.len() + AES_KEY_BYTES + HMAC_KEY_BYTES;
        if bytes.len() != expected_len {
            return Err(KeyFormatError::WrongLength {
                expected: expected_len,
                actual: bytes.len(),
            });
        }
        if &bytes[..KEY_MAGIC.len()] != KEY_MAGIC {
            return Err(KeyFormatError::BadMagic);
        }
        let mut aes = [0u8; AES_KEY_BYTES];
        let mut hmac = [0u8; HMAC_KEY_BYTES];
        aes.copy_from_slice(&bytes[KEY_MAGIC.len()..KEY_MAGIC.len() + AES_KEY_BYTES]);
        hmac.copy_from_slice(&bytes[KEY_MAGIC.len() + AES_KEY_BYTES..]);
        Ok(Self { aes, hmac })
    }
}

// Не печатаем ключ в Debug-логах, чтобы он не утёк в `tracing`.
impl std::fmt::Debug for SymmetricKey {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("SymmetricKey")
            .field("aes", &"<redacted 32 bytes>")
            .field("hmac", &"<redacted 32 bytes>")
            .finish()
    }
}

#[derive(Debug, thiserror::Error, PartialEq, Eq)]
pub enum KeyFormatError {
    #[error("ожидалось {expected} байт ключа, получено {actual}")]
    WrongLength { expected: usize, actual: usize },
    #[error("неверный magic-заголовок ключа (не PSIA-LAB6-AES)")]
    BadMagic,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn round_trip_serializes_to_expected_size() {
        let key = SymmetricKey::from_parts([1u8; 32], [2u8; 32]);
        let bytes = key.to_file_bytes();
        assert_eq!(bytes.len(), 16 + 32 + 32);
        assert_eq!(&bytes[..16], KEY_MAGIC);
    }

    #[test]
    fn round_trip_through_bytes() {
        let key = SymmetricKey::from_parts([7u8; 32], [9u8; 32]);
        let bytes = key.to_file_bytes();
        let parsed = SymmetricKey::from_file_bytes(&bytes).unwrap();
        assert_eq!(parsed, key);
    }

    #[test]
    fn wrong_length_is_reported() {
        let err = SymmetricKey::from_file_bytes(&[0u8; 10]).unwrap_err();
        assert!(matches!(err, KeyFormatError::WrongLength { .. }));
    }

    #[test]
    fn bad_magic_is_reported() {
        let mut bytes = vec![0u8; 16 + 32 + 32];
        bytes[..16].copy_from_slice(b"XXXXXXXXXXXXXXXX");
        let err = SymmetricKey::from_file_bytes(&bytes).unwrap_err();
        assert!(matches!(err, KeyFormatError::BadMagic));
    }

    #[test]
    fn debug_does_not_leak_key_bytes() {
        let key = SymmetricKey::from_parts([0xAB; 32], [0xCD; 32]);
        let dbg = format!("{key:?}");
        assert!(!dbg.contains("ab"));
        assert!(!dbg.contains("cd"));
        assert!(dbg.contains("redacted"));
    }
}
