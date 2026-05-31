//! Криптоанализ Виженера: индекс совпадения и подбор ключа.

use shared::alphabet::{ALPHABET_SIZE, FREQUENCIES, index_of_coincidence};
use tracing::debug;

use super::cipher::decrypt;
use super::errors::DomainError;

/// Индекс совпадения «осмысленного русского» — из методички.
pub const RUS_IC: f64 = 0.0553;

/// Индекс совпадения «равновероятного» — 1/33 ≈ 0.0303.
pub const UNIFORM_IC: f64 = 0.0303_03;

/// Разделить текст на L подстрок (i-я содержит символы с позициями i, i+L, i+2L, ...).
pub fn columns(text: &[usize], key_len: usize) -> Vec<Vec<usize>> {
    let mut cols = vec![Vec::new(); key_len];
    for (i, &c) in text.iter().enumerate() {
        cols[i % key_len].push(c);
    }
    cols
}

/// Для каждой длины ключа из диапазона `range` вычислить средний индекс совпадения по столбцам.
///
/// Самая «осмысленная» длина — та, при которой средний IC ≈ RUS_IC.
pub fn key_length_scores(
    text: &[usize],
    range: std::ops::RangeInclusive<usize>,
) -> Vec<(usize, f64)> {
    let mut out = Vec::new();
    for l in range {
        let cols = columns(text, l);
        let avg: f64 = cols.iter().map(|c| index_of_coincidence(c)).sum::<f64>() / l as f64;
        out.push((l, avg));
        debug!(key_len = l, avg_ic = avg, "key length candidate");
    }
    out
}

/// Доля от максимального IC, выше которой длина считается «осмысленной».
///
/// Истинная длина даёт IC ≈ максимуму (≥0.95 от него), а ложные «гармоники»
/// (например, L=2 при истинной длине 4) — заметно ниже (≤0.9). Порог 0.95
/// надёжно отделяет их.
pub const IC_PEAK_RATIO: f64 = 0.95;

/// Подобрать наилучшую длину ключа.
///
/// Истинная длина ключа даёт средний IC, близкий к [`RUS_IC`]; её кратные (2L, 3L)
/// дают такой же высокий IC, а ложные (шумовые) длины — заметно ниже. Берём
/// максимум IC по всем длинам и выбираем **наименьшую** длину, чей IC составляет
/// не менее [`IC_PEAK_RATIO`] от максимума, — это отсекает и шум, и кратные длины.
pub fn best_key_length(text: &[usize], range: std::ops::RangeInclusive<usize>) -> usize {
    let scores = key_length_scores(text, range);
    let Some(max_ic) = scores.iter().map(|(_, ic)| *ic).reduce(f64::max) else {
        return 1;
    };
    let cutoff = max_ic * IC_PEAK_RATIO;
    scores
        .iter()
        .find(|(_, ic)| *ic >= cutoff)
        .map_or(1, |(l, _)| *l)
}

/// Для столбца ciphertext подобрать сдвиг (буквы ключа), при котором χ² с эталонной
/// частотой русского языка минимально.
pub fn best_shift_for_column(column: &[usize]) -> usize {
    let n = column.len();
    if n == 0 {
        return 0;
    }
    let mut counts = [0u64; ALPHABET_SIZE];
    for &c in column {
        counts[c] += 1;
    }
    let mut best_shift = 0;
    let mut best_chi = f64::INFINITY;
    for s in 0..ALPHABET_SIZE {
        let chi: f64 = (0..ALPHABET_SIZE)
            .map(|i| {
                let observed = counts[(i + s) % ALPHABET_SIZE] as f64;
                let expected = FREQUENCIES[i] * n as f64;
                if expected.abs() < 1e-9 {
                    0.0
                } else {
                    (observed - expected).powi(2) / expected
                }
            })
            .sum();
        if chi < best_chi {
            best_chi = chi;
            best_shift = s;
        }
    }
    best_shift
}

/// Полный криптоанализ: определить длину ключа в диапазоне и восстановить сам ключ.
pub fn recover_key(
    cipher: &[usize],
    range: std::ops::RangeInclusive<usize>,
) -> Result<Vec<usize>, DomainError> {
    if cipher.len() < 30 {
        return Err(DomainError::TextTooShort {
            len: cipher.len(),
            needed: 30,
        });
    }
    let key_len = best_key_length(cipher, range);
    let key = columns(cipher, key_len)
        .iter()
        .map(|col| best_shift_for_column(col))
        .collect::<Vec<_>>();
    Ok(key)
}

/// Полный криптоанализ + дешифрование.
pub fn break_cipher(
    cipher: &[usize],
    range: std::ops::RangeInclusive<usize>,
) -> Result<(Vec<usize>, Vec<usize>), DomainError> {
    let key = recover_key(cipher, range)?;
    let plain = decrypt(cipher, &key)?;
    Ok((key, plain))
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::domain::cipher::{encrypt, from_indices, to_indices};

    #[test]
    fn recovers_short_key_on_long_text() {
        // Длинный осмысленный русский текст (повторим методическую фразу), ключ "КЛЮЧ".
        let plain = "В_ДАННОЙ_СТАТЬЕ_ПРИВЕДЕНЫ_РЕЗУЛЬТАТЫ_АНАЛИЗА_ФАКТОРОВ_ОКАЗЫВАЮЩИХ\
                     _ВЛИЯНИЕ_НА_ГОРЕЛОЧНОЕ_УСТРОЙСТВО_ТЕПЛОГЕНЕРАТОРОВ_А_ТАКЖЕ_МЕТОДОВ\
                     _ИХ_ВЫБОРА_ПРИВЕДЕНЫ_РЕЗУЛЬТАТЫ_ЭКСПЕРИМЕНТАЛЬНОГО_ИССЛЕДОВАНИЯ";
        let p = to_indices(plain).unwrap();
        let k = to_indices("КЛЮЧ").unwrap();
        let c = encrypt(&p, &k).unwrap();
        let recovered = recover_key(&c, 2..=8).unwrap();
        assert_eq!(recovered, k, "ключ должен восстановиться полностью");
        let decrypted = decrypt(&c, &recovered).unwrap();
        assert_eq!(from_indices(&decrypted), plain);
    }
}
