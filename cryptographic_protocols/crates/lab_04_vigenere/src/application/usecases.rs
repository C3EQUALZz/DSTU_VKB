//! Сценарии лаб 4.

use crate::domain::cipher::{Alphabet, decrypt, encrypt, from_indices, to_indices};
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
    run_encrypt_with_alphabet(plain, key, Alphabet::Lab04)
}

pub fn run_encrypt_with_alphabet(
    plain: &str,
    key: &str,
    alphabet: Alphabet,
) -> Result<EncryptReport, DomainError> {
    tracing::info!(
        symbols = plain.chars().count(),
        "начато шифрование Виженера"
    );
    let p = alphabet.to_indices(plain)?;
    let k = alphabet.to_indices(key)?;
    let c = encrypt(&p, &k)?;
    tracing::info!(symbols = c.len(), "шифрование Виженера завершено");
    Ok(EncryptReport {
        plain: plain.to_string(),
        key: key.to_string(),
        cipher: alphabet.render(&c),
    })
}

#[tracing::instrument(skip_all)]
pub fn run_decrypt(cipher: &str, key: &str) -> Result<DecryptReport, DomainError> {
    run_decrypt_with_alphabet(cipher, key, Alphabet::Lab04)
}

pub fn run_decrypt_with_alphabet(
    cipher: &str,
    key: &str,
    alphabet: Alphabet,
) -> Result<DecryptReport, DomainError> {
    tracing::info!(
        symbols = cipher.chars().count(),
        "подготовка шифртекста Виженера"
    );
    let c = alphabet.to_indices(cipher)?;
    let k = alphabet.to_indices(key)?;
    let p = decrypt(&c, &k)?;
    tracing::info!(symbols = p.len(), "расшифровка Виженера завершена");
    Ok(DecryptReport {
        cipher: cipher.to_string(),
        key: key.to_string(),
        plain: alphabet.render(&p),
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

#[cfg(test)]
mod russian_yo_tests {
    use super::*;

    #[test]
    fn report_example_and_yo() {
        let alphabet = Alphabet::RussianWithYo;
        let result = run_encrypt_with_alphabet("КРИПТОГРАФИЯ", "КЛЮЧ", alphabet).unwrap();
        assert_eq!(result.cipher, "ХЬЖЖЭЪБЗКАЖЦ");
        assert_eq!(
            run_decrypt_with_alphabet(&result.cipher, "КЛЮЧ", alphabet)
                .unwrap()
                .plain,
            "КРИПТОГРАФИЯ"
        );
        assert_eq!(
            run_encrypt_with_alphabet("ЕЁЯ", "Б", alphabet)
                .unwrap()
                .cipher,
            "ЁЖА"
        );
        assert_eq!(
            run_decrypt_with_alphabet("ЁЖА", "Б", alphabet)
                .unwrap()
                .plain,
            "ЕЁЯ"
        );
        assert!(run_encrypt_with_alphabet("А_", "Б", alphabet).is_err());
        assert!(run_encrypt_with_alphabet("А", "", alphabet).is_err());
        assert!(run_encrypt_with_alphabet("А", "_", alphabet).is_err());
        assert_eq!(
            run_encrypt_with_alphabet("", "Б", alphabet).unwrap().cipher,
            ""
        );
    }
}
