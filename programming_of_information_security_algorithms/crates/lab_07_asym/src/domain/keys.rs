//! Файловое представление ключей: magic + 4 байта bits + DER.

use thiserror::Error;

use crate::domain::cipher::{RawPrivateKey, RawPublicKey};

pub const PUBLIC_KEY_MAGIC: &[u8; 16] = b"PSIA-LAB7-PUB\x00\x00\x00";
pub const PRIVATE_KEY_MAGIC: &[u8; 16] = b"PSIA-LAB7-PRV\x00\x00\x00";
pub const CIPHERTEXT_MAGIC: &[u8; 16] = b"PSIA-LAB7-CTX\x00\x00\x00";

#[derive(Debug, Error, PartialEq, Eq)]
pub enum KeyFileError {
    #[error("файл короче, чем заголовок (magic + bits): получено {0} байт")]
    TooShort(usize),
    #[error("неверный magic — это не {expected:?}")]
    BadMagic { expected: &'static str },
}

/// Сериализация публичного ключа в файл.
#[must_use]
pub fn pack_public(key: &RawPublicKey) -> Vec<u8> {
    pack(PUBLIC_KEY_MAGIC, key.bits, &key.der)
}

/// Сериализация приватного ключа в файл.
#[must_use]
pub fn pack_private(key: &RawPrivateKey) -> Vec<u8> {
    pack(PRIVATE_KEY_MAGIC, key.bits, &key.der)
}

/// Сериализация шифртекста: только magic + payload (никакого bits — он
/// определяется ключом при расшифровке).
#[must_use]
pub fn pack_ciphertext(payload: &[u8]) -> Vec<u8> {
    let mut out = Vec::with_capacity(CIPHERTEXT_MAGIC.len() + payload.len());
    out.extend_from_slice(CIPHERTEXT_MAGIC);
    out.extend_from_slice(payload);
    out
}

/// Десериализация публичного ключа.
///
/// # Errors
/// — `TooShort` / `BadMagic`.
pub fn unpack_public(bytes: &[u8]) -> Result<RawPublicKey, KeyFileError> {
    let (bits, der) = unpack(PUBLIC_KEY_MAGIC, bytes, "PSIA-LAB7-PUB")?;
    Ok(RawPublicKey { bits, der })
}

/// Десериализация приватного ключа.
///
/// # Errors
/// — `TooShort` / `BadMagic`.
pub fn unpack_private(bytes: &[u8]) -> Result<RawPrivateKey, KeyFileError> {
    let (bits, der) = unpack(PRIVATE_KEY_MAGIC, bytes, "PSIA-LAB7-PRV")?;
    Ok(RawPrivateKey { bits, der })
}

/// Снимает magic с шифртекста.
///
/// # Errors
/// — `TooShort` / `BadMagic`.
pub fn unpack_ciphertext(bytes: &[u8]) -> Result<Vec<u8>, KeyFileError> {
    if bytes.len() < CIPHERTEXT_MAGIC.len() {
        return Err(KeyFileError::TooShort(bytes.len()));
    }
    if &bytes[..CIPHERTEXT_MAGIC.len()] != CIPHERTEXT_MAGIC {
        return Err(KeyFileError::BadMagic {
            expected: "PSIA-LAB7-CTX",
        });
    }
    Ok(bytes[CIPHERTEXT_MAGIC.len()..].to_vec())
}

fn pack(magic: &[u8; 16], bits: usize, der: &[u8]) -> Vec<u8> {
    let mut out = Vec::with_capacity(magic.len() + 4 + der.len());
    out.extend_from_slice(magic);
    let bits_u32: u32 = u32::try_from(bits).unwrap_or(0);
    out.extend_from_slice(&bits_u32.to_be_bytes());
    out.extend_from_slice(der);
    out
}

fn unpack(
    expected_magic: &[u8; 16],
    bytes: &[u8],
    label: &'static str,
) -> Result<(usize, Vec<u8>), KeyFileError> {
    let header = expected_magic.len() + 4;
    if bytes.len() < header {
        return Err(KeyFileError::TooShort(bytes.len()));
    }
    if &bytes[..expected_magic.len()] != expected_magic {
        return Err(KeyFileError::BadMagic { expected: label });
    }
    let bits_arr: [u8; 4] = bytes[expected_magic.len()..header]
        .try_into()
        .expect("длина 4 проверена выше");
    let bits = u32::from_be_bytes(bits_arr) as usize;
    Ok((bits, bytes[header..].to_vec()))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pack_unpack_public_round_trip() {
        let key = RawPublicKey {
            bits: 2048,
            der: b"<some DER>".to_vec(),
        };
        let bytes = pack_public(&key);
        let parsed = unpack_public(&bytes).unwrap();
        assert_eq!(parsed, key);
    }

    #[test]
    fn pack_unpack_private_round_trip() {
        let key = RawPrivateKey {
            bits: 2048,
            der: b"<some DER private>".to_vec(),
        };
        let bytes = pack_private(&key);
        let parsed = unpack_private(&bytes).unwrap();
        assert_eq!(parsed, key);
    }

    #[test]
    fn pack_unpack_ciphertext_round_trip() {
        let payload = b"opaque ciphertext blob".to_vec();
        let bytes = pack_ciphertext(&payload);
        let parsed = unpack_ciphertext(&bytes).unwrap();
        assert_eq!(parsed, payload);
    }

    #[test]
    fn bad_magic_rejected() {
        let mut bytes = pack_public(&RawPublicKey {
            bits: 2048,
            der: vec![1, 2, 3],
        });
        bytes[..16].copy_from_slice(b"WRONG-MAGIC-DATA");
        assert!(matches!(
            unpack_public(&bytes),
            Err(KeyFileError::BadMagic { .. })
        ));
    }

    #[test]
    fn debug_for_private_key_redacts_der() {
        let key = RawPrivateKey {
            bits: 2048,
            der: vec![0xDE, 0xAD, 0xBE, 0xEF],
        };
        let dbg = format!("{key:?}");
        assert!(!dbg.contains("deadbeef"));
        assert!(dbg.contains("redacted"));
    }
}
