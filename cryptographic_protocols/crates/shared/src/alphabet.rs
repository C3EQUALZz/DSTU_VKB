//! Русский 32-буквенный алфавит со знаком пробела.
//!
//! Используется лабораторными 3 (простая замена) и 4 (Виженер).
//! Согласно условию: Е и Ё считаются одной буквой (ранг 3), Ь и Ъ — одной (ранг 20).
//! Знак подчёркивания «_» = пробел.

/// 32-буквенный алфавит + знак пробела (33 символа).
/// Используется методичкой при шифровании и в таблицах частот.
pub const ALPHABET: [char; 33] = [
    'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т',
    'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', '_',
];

pub const ALPHABET_SIZE: usize = ALPHABET.len();

/// Частоты букв русского языка (из учебника, табл. 1.1).
/// Сумма ≈ 1.0. Порядок соответствует [`ALPHABET`].
pub const FREQUENCIES: [f64; 33] = [
    0.062, // А
    0.014, // Б
    0.038, // В
    0.013, // Г
    0.025, // Д
    0.072, // Е (включая Ё)
    0.007, // Ж
    0.016, // З
    0.062, // И
    0.010, // Й
    0.028, // К
    0.035, // Л
    0.026, // М
    0.053, // Н
    0.090, // О
    0.023, // П
    0.040, // Р
    0.045, // С
    0.053, // Т
    0.021, // У
    0.002, // Ф
    0.009, // Х
    0.004, // Ц
    0.012, // Ч
    0.006, // Ш
    0.003, // Щ
    0.014, // Ъ (вместе с Ь)
    0.016, // Ы
    0.014, // Ь
    0.003, // Э
    0.006, // Ю
    0.018, // Я
    0.175, // _ пробел
];

/// Возвращает индекс символа в алфавите (с приведением регистра, Ё→Е, Ъ→Ь).
pub fn index_of(c: char) -> Option<usize> {
    let up = match c {
        'ё' | 'Ё' => 'Е',
        'ъ' | 'Ъ' => 'Ь',
        other => other.to_uppercase().next().unwrap_or(other),
    };
    ALPHABET.iter().position(|&x| x == up)
}

/// Индекс совпадения (Index of Coincidence) для текста на русском алфавите.
///
/// IC = Σ f_i·(f_i−1) / (n·(n−1)),
/// где f_i — частота i-го символа, n — длина текста.
///
/// Для случайного текста IC ≈ 1/33 ≈ 0.0303.
/// Для осмысленного русского IC ≈ 0.053..0.07.
pub fn index_of_coincidence(text: &[usize]) -> f64 {
    let n = text.len();
    if n < 2 {
        return 0.0;
    }
    let mut counts = [0u64; ALPHABET_SIZE];
    for &i in text {
        counts[i] += 1;
    }
    let numerator: u64 = counts.iter().map(|&f| f * f.saturating_sub(1)).sum();
    numerator as f64 / (n as u64 * (n as u64 - 1)) as f64
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn alphabet_has_33_symbols() {
        assert_eq!(ALPHABET.len(), 33);
        assert_eq!(ALPHABET[0], 'А');
        assert_eq!(ALPHABET[32], '_');
    }

    #[test]
    fn frequencies_sum_close_to_one() {
        // Таблица из методички — сумма получается ~1.015 из-за округлений до тысячных.
        let s: f64 = FREQUENCIES.iter().sum();
        assert!((s - 1.0).abs() < 0.05, "sum was {s}");
    }

    #[test]
    fn index_of_handles_yo_and_hard_sign() {
        assert_eq!(index_of('А'), Some(0));
        assert_eq!(index_of('а'), Some(0));
        assert_eq!(index_of('Е'), Some(5));
        assert_eq!(index_of('Ё'), Some(5));
        assert_eq!(index_of('ё'), Some(5));
        assert_eq!(index_of('Ъ'), Some(28));
        assert_eq!(index_of('Ь'), Some(28));
        assert_eq!(index_of('_'), Some(32));
        assert_eq!(index_of('?'), None);
    }

    #[test]
    fn ic_for_uniform_text_near_one_over_alphabet_size() {
        let text: Vec<usize> = (0..ALPHABET_SIZE).cycle().take(33 * 100).collect();
        let ic = index_of_coincidence(&text);
        let expected = 1.0 / ALPHABET_SIZE as f64;
        assert!((ic - expected).abs() < 0.01, "ic={ic}, expected≈{expected}");
    }
}
