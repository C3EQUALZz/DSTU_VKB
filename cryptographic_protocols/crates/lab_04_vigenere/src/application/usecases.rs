//! Сценарии лаб 4.

use crate::domain::cipher::{decrypt, encrypt, from_indices, to_indices};
use crate::domain::cryptanalysis::{break_cipher, key_length_scores};
use crate::domain::errors::DomainError;

#[derive(Debug, Clone)]
pub struct EncryptReport {
    pub plain: String,
    pub key: String,
    pub cipher: String,
}

#[derive(Debug, Clone)]
pub struct DecryptReport {
    pub cipher: String,
    pub key: String,
    pub plain: String,
}

#[derive(Debug, Clone)]
pub struct CryptanalysisReport {
    pub cipher: String,
    pub key_length_scores: Vec<(usize, f64)>,
    pub recovered_key: String,
    pub recovered_plain: String,
}

pub fn run_encrypt(plain: &str, key: &str) -> Result<EncryptReport, DomainError> {
    let p = to_indices(plain)?;
    let k = to_indices(key)?;
    let c = encrypt(&p, &k)?;
    Ok(EncryptReport {
        plain: plain.to_string(),
        key: key.to_string(),
        cipher: from_indices(&c),
    })
}

pub fn run_decrypt(cipher: &str, key: &str) -> Result<DecryptReport, DomainError> {
    let c = to_indices(cipher)?;
    let k = to_indices(key)?;
    let p = decrypt(&c, &k)?;
    Ok(DecryptReport {
        cipher: cipher.to_string(),
        key: key.to_string(),
        plain: from_indices(&p),
    })
}

pub fn run_cryptanalysis(
    cipher: &str,
    range: std::ops::RangeInclusive<usize>,
) -> Result<CryptanalysisReport, DomainError> {
    let c = to_indices(cipher)?;
    let scores = key_length_scores(&c, range.clone());
    let (key, plain) = break_cipher(&c, range)?;
    Ok(CryptanalysisReport {
        cipher: cipher.to_string(),
        key_length_scores: scores,
        recovered_key: from_indices(&key),
        recovered_plain: from_indices(&plain),
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn encrypt_roundtrip_via_usecase() {
        let r = run_encrypt("ПРИВЕТ_МИР", "НОТА").unwrap();
        assert_eq!(r.cipher, "ЬЮЪВТ_СМХЮ");
        let d = run_decrypt(&r.cipher, "НОТА").unwrap();
        assert_eq!(d.plain, "ПРИВЕТ_МИР");
    }
}
