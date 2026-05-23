//! Сценарии лаб 6: для каждой буквы слова применяем обе схемы.

use num_bigint::BigUint;
use tracing::info;

use crate::domain::asmuth_bloom;
use crate::domain::encoding::{decode_word, encode_word};
use crate::domain::errors::DomainError;
use crate::domain::mignotte;

/// Малая таблица простых до 1500 — для жадного подбора (k, n)-последовательности.
pub const SMALL_PRIMES: &[u64] = &[
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
    101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193,
    197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307,
    311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421,
    431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547,
    557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659,
    661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797,
    809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929,
    937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039,
    1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153,
    1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279,
    1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409,
    1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471, 1481, 1483, 1487, 1489, 1493, 1499,
];

#[derive(Debug, Clone)]
pub struct LetterReport {
    pub letter_index: usize,
    pub letter: char,
    pub secret: u32,
    pub mignotte: MignotteSummary,
    pub asmuth_bloom: AsmuthBloomSummary,
}

#[derive(Debug, Clone)]
pub struct MignotteSummary {
    pub basis: Vec<u64>,
    pub shares: Vec<BigUint>,
    pub recovered_by_k: BigUint,
    pub recovered_by_n: BigUint,
}

#[derive(Debug, Clone)]
pub struct AsmuthBloomSummary {
    pub q: u64,
    pub basis: Vec<u64>,
    pub r: u64,
    pub shares: Vec<BigUint>,
    pub recovered_by_k: BigUint,
    pub recovered_by_n: BigUint,
}

#[derive(Debug, Clone)]
pub struct WordReport {
    pub word: String,
    pub k: usize,
    pub n: usize,
    pub letters: Vec<LetterReport>,
}

impl WordReport {
    pub fn recovered_word_by_k(&self) -> String {
        let codes: Vec<u32> = self
            .letters
            .iter()
            .map(|l| {
                l.mignotte
                    .recovered_by_k
                    .iter_u32_digits()
                    .next()
                    .unwrap_or(0)
            })
            .collect();
        decode_word(&codes)
    }
}

pub fn process_word(word: &str, k: usize, n: usize, r: u64) -> Result<WordReport, DomainError> {
    let codes = encode_word(word).ok_or_else(|| DomainError::SequenceNotFound {
        k,
        n,
        secret: format!("слово содержит символы вне алфавита: {word}"),
    })?;
    let chars: Vec<char> = word.chars().collect();
    info!(
        word,
        codes_len = codes.len(),
        k,
        n,
        "разделяем слово побуквенно"
    );

    let mut letters = Vec::with_capacity(codes.len());
    for (idx, (&c, &secret)) in chars.iter().zip(codes.iter()).enumerate() {
        let s_big = BigUint::from(secret);
        // Миньотта.
        let m_basis = mignotte::find_basis(&s_big, k, n, SMALL_PRIMES)?;
        let m_shares = mignotte::split(&s_big, &m_basis, k)?;
        let m_by_k = mignotte::reconstruct(&m_shares[..k])?;
        let m_by_n = mignotte::reconstruct(&m_shares)?;

        // Асмут-Блум.
        let ab_params = asmuth_bloom::find_params(&s_big, k, n, SMALL_PRIMES)?;
        let ab_shares = asmuth_bloom::split(&s_big, &ab_params, &BigUint::from(r))?;
        let ab_by_k = asmuth_bloom::reconstruct(&ab_shares[..k])?;
        let ab_by_n = asmuth_bloom::reconstruct(&ab_shares)?;

        letters.push(LetterReport {
            letter_index: idx,
            letter: c,
            secret,
            mignotte: MignotteSummary {
                basis: m_basis
                    .iter()
                    .map(|b| b.iter_u64_digits().next().unwrap_or(0))
                    .collect(),
                shares: m_shares.into_iter().map(|s| s.value).collect(),
                recovered_by_k: m_by_k,
                recovered_by_n: m_by_n,
            },
            asmuth_bloom: AsmuthBloomSummary {
                q: ab_params.q.iter_u64_digits().next().unwrap_or(0),
                basis: ab_params
                    .basis
                    .iter()
                    .map(|b| b.iter_u64_digits().next().unwrap_or(0))
                    .collect(),
                r,
                shares: ab_shares.into_iter().map(|s| s.value).collect(),
                recovered_by_k: ab_by_k,
                recovered_by_n: ab_by_n,
            },
        });
    }

    Ok(WordReport {
        word: word.to_string(),
        k,
        n,
        letters,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn roundtrip_for_each_word() {
        for word in ["АНКЛАВ", "ИНТЕРН", "НАДЗОР", "НАДРЕЗ"] {
            let report = process_word(word, 3, 5, 7).unwrap();
            for l in &report.letters {
                assert_eq!(l.mignotte.recovered_by_k, BigUint::from(l.secret));
                assert_eq!(l.mignotte.recovered_by_n, BigUint::from(l.secret));
                assert_eq!(l.asmuth_bloom.recovered_by_k, BigUint::from(l.secret));
                assert_eq!(l.asmuth_bloom.recovered_by_n, BigUint::from(l.secret));
            }
            assert_eq!(report.recovered_word_by_k(), word);
        }
    }
}
