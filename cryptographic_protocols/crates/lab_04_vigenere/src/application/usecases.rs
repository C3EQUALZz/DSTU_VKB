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

#[tracing::instrument(skip_all)]
pub fn run_encrypt(plain: &str, key: &str) -> Result<EncryptReport, DomainError> {
    tracing::info!(
        symbols = plain.chars().count(),
        "начато шифрование Виженера"
    );
    let p = to_indices(plain)?;
    let k = to_indices(key)?;
    let c = encrypt(&p, &k)?;
    tracing::info!(symbols = c.len(), "шифрование Виженера завершено");
    Ok(EncryptReport {
        plain: plain.to_string(),
        key: key.to_string(),
        cipher: from_indices(&c),
    })
}

#[tracing::instrument(skip_all)]
pub fn run_decrypt(cipher: &str, key: &str) -> Result<DecryptReport, DomainError> {
    tracing::info!(
        symbols = cipher.chars().count(),
        "подготовка шифртекста Виженера"
    );
    let c = to_indices(cipher)?;
    let k = to_indices(key)?;
    let p = decrypt(&c, &k)?;
    tracing::info!(symbols = p.len(), "расшифровка Виженера завершена");
    Ok(DecryptReport {
        cipher: cipher.to_string(),
        key: key.to_string(),
        plain: from_indices(&p),
    })
}

#[tracing::instrument(skip_all)]
pub fn run_cryptanalysis(
    cipher: &str,
    range: std::ops::RangeInclusive<usize>,
) -> Result<CryptanalysisReport, DomainError> {
    tracing::info!(
        symbols = cipher.chars().count(),
        "подготовка шифртекста Виженера"
    );
    let c = to_indices(cipher)?;
    tracing::info!(
        min_key = *range.start(),
        max_key = *range.end(),
        "начат криптоанализ Виженера"
    );
    let scores = key_length_scores(&c, range.clone());
    let (key, plain) = break_cipher(&c, range)?;
    tracing::info!(
        key_length = key.len(),
        symbols = plain.len(),
        "криптоанализ Виженера завершён"
    );
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
