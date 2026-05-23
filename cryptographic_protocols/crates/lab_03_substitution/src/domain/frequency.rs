//! Частотный анализ для шифра простой замены.

use std::collections::HashMap;

use shared::alphabet::{ALPHABET, FREQUENCIES};

use super::cipher::Substitution;

/// Подсчёт частот токенов в шифртексте.
pub fn count_codes(codes: &[u32]) -> Vec<(u32, usize)> {
    let mut map: HashMap<u32, usize> = HashMap::new();
    for &c in codes {
        *map.entry(c).or_insert(0) += 1;
    }
    let mut v: Vec<(u32, usize)> = map.into_iter().collect();
    v.sort_by(|a, b| b.1.cmp(&a.1).then(a.0.cmp(&b.0)));
    v
}

/// Построить начальную подстановку по частотам:
/// самый частый шифрообразование соответствует самой частой букве алфавита,
/// и т.д. (жадный «по убыванию частоты»).
pub fn initial_substitution(codes: &[u32]) -> Substitution {
    let cipher_freq = count_codes(codes);
    // Эталонные буквы в порядке убывания частоты.
    let mut idx_by_freq: Vec<usize> = (0..ALPHABET.len()).collect();
    idx_by_freq.sort_by(|&a, &b| {
        FREQUENCIES[b]
            .partial_cmp(&FREQUENCIES[a])
            .unwrap_or(std::cmp::Ordering::Equal)
    });

    let mut sub = Substitution::default();
    for (i, (code, _)) in cipher_freq.iter().enumerate() {
        if let Some(&letter_idx) = idx_by_freq.get(i) {
            sub.map.insert(*code, ALPHABET[letter_idx]);
        }
    }
    sub
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn count_orders_by_frequency() {
        let codes = vec![1, 2, 2, 3, 3, 3];
        let c = count_codes(&codes);
        assert_eq!(c, vec![(3, 3), (2, 2), (1, 1)]);
    }

    #[test]
    fn initial_assignment_uses_most_frequent_letter_for_most_frequent_code() {
        // Если в тексте одно слово из 50 повторов одного шифр-кода,
        // он должен получить '_' (самая частая буква русского).
        let codes = vec![42u32; 50];
        let sub = initial_substitution(&codes);
        assert_eq!(sub.map.get(&42), Some(&'_'));
    }
}
