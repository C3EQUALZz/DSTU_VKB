//! Шифр Виженера на 33-буквенном русском алфавите.
//!
//! Шифрование: c_i = (p_i + k_{i mod L}) mod 33.
//! Дешифрование: p_i = (c_i − k_{i mod L} + 33) mod 33.

use shared::alphabet::{ALPHABET, ALPHABET_SIZE, index_of};

use super::errors::DomainError;

/// Перевести строку в массив индексов 0..33. Символы вне алфавита приводят к ошибке.
pub fn to_indices(text: &str) -> Result<Vec<usize>, DomainError> {
    text.chars()
        .map(|c| index_of(c).ok_or(DomainError::OutOfAlphabet { c }))
        .collect()
}

/// Перевести массив индексов обратно в строку.
pub fn from_indices(idx: &[usize]) -> String {
    idx.iter().map(|&i| ALPHABET[i % ALPHABET_SIZE]).collect()
}

/// Шифрование Виженера.
pub fn encrypt(plain_idx: &[usize], key_idx: &[usize]) -> Result<Vec<usize>, DomainError> {
    if key_idx.is_empty() {
        return Err(DomainError::EmptyKey);
    }
    Ok(plain_idx
        .iter()
        .enumerate()
        .map(|(i, &p)| {
            let c = (p + key_idx[i % key_idx.len()]) % ALPHABET_SIZE;
            tracing::info!(
                step = "vigenere.encrypt_symbol",
                position = i + 1,
                key_position = i % key_idx.len() + 1,
                plain_index = p,
                cipher_index = c,
                alphabet_size = ALPHABET_SIZE,
                "cipher_index = (p + k) mod 33"
            );
            c
        })
        .collect())
}

/// Дешифрование Виженера известным ключом.
pub fn decrypt(cipher_idx: &[usize], key_idx: &[usize]) -> Result<Vec<usize>, DomainError> {
    if key_idx.is_empty() {
        return Err(DomainError::EmptyKey);
    }
    Ok(cipher_idx
        .iter()
        .enumerate()
        .map(|(i, &c)| {
            let p = (c + ALPHABET_SIZE - key_idx[i % key_idx.len()]) % ALPHABET_SIZE;
            tracing::info!(
                step = "vigenere.decrypt_symbol",
                position = i + 1,
                key_position = i % key_idx.len() + 1,
                cipher_index = c,
                plain_index = p,
                alphabet_size = ALPHABET_SIZE,
                "plain_index = (c − k + 33) mod 33"
            );
            p
        })
        .collect())
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Эталонный пример методички: «ПРИВЕТ_МИР» + ключ «НОТА» → «ЬЮЪВТ_СМХЮ».
    #[test]
    fn methodichka_example_encrypts_to_yuyabtsmkhyu() {
        let p = to_indices("ПРИВЕТ_МИР").unwrap();
        let k = to_indices("НОТА").unwrap();
        let c = encrypt(&p, &k).unwrap();
        assert_eq!(from_indices(&c), "ЬЮЪВТ_СМХЮ");
    }

    #[test]
    fn encrypt_decrypt_roundtrip() {
        let p = to_indices("ПРИВЕТ_МИР").unwrap();
        let k = to_indices("КЛЮЧ").unwrap();
        let c = encrypt(&p, &k).unwrap();
        let d = decrypt(&c, &k).unwrap();
        assert_eq!(d, p);
    }
}
