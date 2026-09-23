//! Статистическое восстановление ключа по одному шифротексту.
//!
//! Это эвристика: на коротком или нетипичном тексте лучший кандидат может быть неверным.

use std::ops::RangeInclusive;

use super::language_counts::{
    EN_BIGRAMS, EN_LETTERS, RU_NO_YO_BIGRAMS, RU_NO_YO_LETTERS, RU_YO_BIGRAMS, RU_YO_LETTERS,
};
use super::scheme::{Alphabet, Scheme};

#[derive(Debug, thiserror::Error, PartialEq, Eq)]
pub enum AttackError {
    #[error("буква шифротекста на позиции {0} не принадлежит выбранному алфавиту")]
    InvalidText(usize),
    #[error("нужен диапазон длин ключа от 1 до длины шифротекста")]
    InvalidRange,
    #[error("шифротекст слишком короткий для статистического анализа: {0} символов, нужно ≥ 30")]
    TextTooShort(usize),
}

#[derive(Debug, Clone)]
pub struct AttackResult {
    pub key: String,
    pub plain: String,
    /// Средний логарифм правдоподобия соседних пар; больше означает лучший кандидат.
    pub score: f64,
    pub key_length: usize,
}

struct LanguageModel {
    letters: &'static [u32],
    bigrams: &'static [u32],
    n: usize,
    letter_total: f64,
    bigram_total: f64,
}

impl LanguageModel {
    fn for_alphabet(alphabet: Alphabet) -> Self {
        let (letters, bigrams): (&'static [u32], &'static [u32]) = match alphabet {
            Alphabet::Latin => (&EN_LETTERS, &EN_BIGRAMS),
            Alphabet::RussianWithYo => (&RU_YO_LETTERS, &RU_YO_BIGRAMS),
            Alphabet::RussianNoYo => (&RU_NO_YO_LETTERS, &RU_NO_YO_BIGRAMS),
        };
        Self {
            letters,
            bigrams,
            n: alphabet.size(),
            letter_total: f64::from(letters.iter().sum::<u32>()) + alphabet.size() as f64,
            bigram_total: f64::from(bigrams.iter().sum::<u32>())
                + (alphabet.size() * alphabet.size()) as f64,
        }
    }

    fn unigram(&self, symbol: usize) -> f64 {
        ((f64::from(self.letters[symbol]) + 1.0) / self.letter_total).ln()
    }

    fn score(&self, plain: &[usize]) -> f64 {
        let pair_score: f64 = plain
            .windows(2)
            .map(|pair| {
                ((f64::from(self.bigrams[pair[0] * self.n + pair[1]]) + 1.0) / self.bigram_total)
                    .ln()
            })
            .sum();
        let letter_score: f64 = plain.iter().map(|&symbol| self.unigram(symbol)).sum();
        (pair_score + 0.2 * letter_score) / plain.len() as f64
    }
}

fn decode(cipher: &[usize], key: &[usize], scheme: Scheme, n: usize) -> Vec<usize> {
    let mut plain = Vec::with_capacity(cipher.len());
    for (position, &symbol) in cipher.iter().enumerate() {
        let shift = match scheme {
            Scheme::Standard => key[position % key.len()],
            Scheme::Progressive => (key[position % key.len()] + position / key.len() % n) % n,
            Scheme::Autokey if position < key.len() => key[position],
            Scheme::Autokey => plain[position - key.len()],
        };
        plain.push((symbol + n - shift) % n);
    }
    plain
}

fn best_standard_key(
    cipher: &[usize],
    key_len: usize,
    scheme: Scheme,
    model: &LanguageModel,
) -> Vec<usize> {
    (0..key_len)
        .map(|column| {
            let adjusted: Vec<usize> = cipher
                .iter()
                .enumerate()
                .filter(|(position, _)| position % key_len == column)
                .map(|(position, &value)| {
                    let progression = if scheme == Scheme::Progressive {
                        position / key_len % model.n
                    } else {
                        0
                    };
                    (value + model.n - progression) % model.n
                })
                .collect();
            (0..model.n)
                .min_by(|&left, &right| {
                    let chi = |shift: usize| {
                        let mut counts = vec![0usize; model.n];
                        for &value in &adjusted {
                            counts[(value + model.n - shift) % model.n] += 1;
                        }
                        counts
                            .iter()
                            .enumerate()
                            .map(|(symbol, &count)| {
                                let expected = (f64::from(model.letters[symbol]) + 1.0)
                                    * adjusted.len() as f64
                                    / model.letter_total;
                                (count as f64 - expected).powi(2) / expected
                            })
                            .sum::<f64>()
                    };
                    chi(left).total_cmp(&chi(right))
                })
                .unwrap_or(0)
        })
        .collect()
}

fn autokey_plain(cipher: &[usize], key_len: usize, seeds: &[usize], n: usize) -> Vec<usize> {
    let mut plain = Vec::with_capacity(cipher.len());
    for (position, &symbol) in cipher.iter().enumerate() {
        let value = if position < key_len {
            seeds[position]
        } else {
            (symbol + n - plain[position - key_len]) % n
        };
        plain.push(value);
    }
    plain
}

fn best_autokey_key(cipher: &[usize], key_len: usize, model: &LanguageModel) -> Vec<usize> {
    let mut seeds = Vec::with_capacity(key_len);
    for column in 0..key_len {
        let best = (0..model.n)
            .max_by(|&left, &right| {
                let chain_score = |seed: usize| {
                    let mut previous = seed;
                    let mut score = model.unigram(seed);
                    let mut position = column + key_len;
                    while position < cipher.len() {
                        previous = (cipher[position] + model.n - previous) % model.n;
                        score += model.unigram(previous);
                        position += key_len;
                    }
                    score
                };
                chain_score(left).total_cmp(&chain_score(right))
            })
            .unwrap_or(0);
        seeds.push(best);
    }

    // Соседние буквы связывают независимые цепочки и уточняют начальное слово.
    for _ in 0..2 {
        for column in 0..key_len {
            let mut best = seeds[column];
            let mut best_score = model.score(&autokey_plain(cipher, key_len, &seeds, model.n));
            for seed in 0..model.n {
                seeds[column] = seed;
                let score = model.score(&autokey_plain(cipher, key_len, &seeds, model.n));
                if score > best_score {
                    best = seed;
                    best_score = score;
                }
            }
            seeds[column] = best;
        }
    }
    seeds
        .iter()
        .enumerate()
        .map(|(position, &plain)| (cipher[position] + model.n - plain) % model.n)
        .collect()
}

/// Возвращает наиболее вероятные ключ и открытый текст для выбранной схемы.
pub fn break_cipher(
    text: &str,
    alphabet: Alphabet,
    scheme: Scheme,
    range: RangeInclusive<usize>,
) -> Result<AttackResult, AttackError> {
    let mut cipher = Vec::new();
    for (position, ch) in text.chars().enumerate() {
        if let Some(value) = alphabet.index(ch) {
            cipher.push(value);
        } else if ch.is_alphabetic() {
            return Err(AttackError::InvalidText(position + 1));
        }
    }
    if cipher.len() < 30 {
        return Err(AttackError::TextTooShort(cipher.len()));
    }
    if range.is_empty() || *range.start() == 0 || *range.end() > cipher.len() {
        return Err(AttackError::InvalidRange);
    }
    let model = LanguageModel::for_alphabet(alphabet);
    let mut best: Option<(Vec<usize>, Vec<usize>, f64)> = None;
    for key_len in range {
        let key = match scheme {
            Scheme::Standard | Scheme::Progressive => {
                best_standard_key(&cipher, key_len, scheme, &model)
            }
            Scheme::Autokey => best_autokey_key(&cipher, key_len, &model),
        };
        let plain = decode(&cipher, &key, scheme, model.n);
        let score = model.score(&plain);
        tracing::info!(key_len, score, ?scheme, ?alphabet, "проверена длина ключа");
        if best.as_ref().is_none_or(|(_, _, current)| score > *current) {
            best = Some((key, plain, score));
        }
    }
    let Some((key, plain, score)) = best else {
        return Err(AttackError::InvalidRange);
    };
    let key: String = key
        .into_iter()
        .map(|value| alphabet.symbol(value))
        .collect();
    let mut symbols = plain.into_iter();
    let mut restored = String::with_capacity(text.len());
    for ch in text.chars() {
        if alphabet.index(ch).is_some() {
            if let Some(value) = symbols.next() {
                let letter = alphabet.symbol(value);
                if ch.is_lowercase() && alphabet != Alphabet::RussianNoYo {
                    restored.extend(letter.to_lowercase());
                } else {
                    restored.push(letter);
                }
            }
        } else {
            restored.push(ch);
        }
    }
    Ok(AttackResult {
        key_length: key.chars().count(),
        key,
        plain: restored,
        score,
    })
}
