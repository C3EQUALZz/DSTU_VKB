//! Кодировка слова как массив малых секретов: индекс каждой буквы в алфавите.
//!
//! Алгоритм лаб 6 (Миньотта/Асмут-Блум) применяется к каждой букве независимо.
//! Так удаётся показать работу схемы на компактных простых, не уходя в
//! арифметику чисел > 10^9.

use shared::alphabet::index_of;

/// Преобразовать слово в массив малых секретов (по одному на каждую букву).
///
/// Для условия β < S < α схемы Миньотта необходимо чтобы S попадал между двумя
/// произведениями. На малых простых это удовлетворимо, например, для basis
/// [5, 7, 11, 13, 17] (α=385, β=221) при S ∈ (221, 385). Поэтому каждая буква
/// сдвигается на +250 — секрет становится из диапазона [250, 282].
pub const LETTER_OFFSET: u32 = 250;

pub fn encode_word(word: &str) -> Option<Vec<u32>> {
    word.chars()
        .map(|c| index_of(c).map(|i| i as u32 + LETTER_OFFSET))
        .collect()
}

pub fn decode_word(values: &[u32]) -> String {
    use shared::alphabet::ALPHABET;
    values
        .iter()
        .filter_map(|&v| {
            let i = v.checked_sub(LETTER_OFFSET)? as usize;
            ALPHABET.get(i).copied()
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn encode_decode_roundtrip() {
        let word = "АНКЛАВ";
        let codes = encode_word(word).unwrap();
        assert_eq!(decode_word(&codes), word);
    }

    #[test]
    fn encode_unknown_char_returns_none() {
        assert!(encode_word("Hello").is_none());
    }
}
