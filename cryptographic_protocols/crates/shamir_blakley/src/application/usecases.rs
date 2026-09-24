//! Восстановление символов и расшифровка по приложению Б методички.

use num_bigint::BigInt;
use num_traits::ToPrimitive;
use thiserror::Error;

use crate::domain::DomainError;
use crate::domain::blakley;
use crate::domain::exact::Rational;
use crate::domain::shamir;

#[derive(Debug)]
pub struct VariantInput {
    pub number: Option<usize>,
    pub shamir: Vec<[shamir::Share; 5]>,
    pub blakley: Vec<[blakley::PlaneShare; 5]>,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Scheme {
    Shamir,
    Blakley,
}

impl Scheme {
    pub fn name(self) -> &'static str {
        match self {
            Self::Shamir => "Шамир",
            Self::Blakley => "Блэкли",
        }
    }
}

#[derive(Debug)]
pub struct SymbolResult {
    pub index: usize,
    pub code: BigInt,
    pub letter: char,
    /// Для Шамира: коэффициенты от свободного члена. Для Блэкли: координаты точки.
    pub solution: Vec<Rational>,
}

#[derive(Debug)]
pub struct RecoveryReport {
    pub scheme: Scheme,
    pub share_count: usize,
    pub symbols: Vec<SymbolResult>,
    pub word: String,
}

#[derive(Debug, Error)]
pub enum ApplicationError {
    #[error("можно восстановить только по 3 или 5 долям")]
    InvalidShareCount,
    #[error("число символов в двух схемах должно совпадать и быть положительным")]
    InvalidSymbolCount,
    #[error("{0}")]
    Domain(#[from] DomainError),
    #[error("код {0} не является русской заглавной буквой в таблице приложения Б")]
    InvalidCharacterCode(String),
    #[error("результаты Шамира и Блэкли не совпали")]
    SchemeMismatch,
}

pub fn recover(
    input: &VariantInput,
    scheme: Scheme,
    share_count: usize,
) -> Result<RecoveryReport, ApplicationError> {
    if !matches!(share_count, 3 | 5) {
        return Err(ApplicationError::InvalidShareCount);
    }
    if input.shamir.is_empty() || input.shamir.len() != input.blakley.len() {
        return Err(ApplicationError::InvalidSymbolCount);
    }
    tracing::info!(
        scheme = scheme.name(),
        share_count,
        "восстановление сообщения"
    );

    let mut symbols = Vec::with_capacity(input.shamir.len());
    let mut word = String::with_capacity(input.shamir.len() * 2);
    for index in 0..input.shamir.len() {
        let solution = match scheme {
            Scheme::Shamir => shamir::reconstruct(&input.shamir[index][..share_count])?,
            Scheme::Blakley => blakley::reconstruct(&input.blakley[index][..share_count])?,
        };
        let code = solution[0]
            .as_integer()
            .ok_or_else(|| ApplicationError::InvalidCharacterCode(solution[0].to_string()))?
            .clone();
        let letter = decode_uppercase_cp1251(&code)?;
        tracing::info!(symbol = index + 1, code = %code, letter = %letter, "символ восстановлен");
        word.push(letter);
        symbols.push(SymbolResult {
            index: index + 1,
            code,
            letter,
            solution,
        });
    }
    Ok(RecoveryReport {
        scheme,
        share_count,
        symbols,
        word,
    })
}

pub fn recover_both(
    input: &VariantInput,
    share_count: usize,
) -> Result<[RecoveryReport; 2], ApplicationError> {
    let shamir = recover(input, Scheme::Shamir, share_count)?;
    let blakley = recover(input, Scheme::Blakley, share_count)?;
    if shamir.word != blakley.word {
        return Err(ApplicationError::SchemeMismatch);
    }
    Ok([shamir, blakley])
}

fn decode_uppercase_cp1251(code: &BigInt) -> Result<char, ApplicationError> {
    let byte = code
        .to_u32()
        .filter(|value| (192..=223).contains(value))
        .ok_or_else(|| ApplicationError::InvalidCharacterCode(code.to_string()))?;
    char::from_u32('А' as u32 + byte - 192)
        .ok_or_else(|| ApplicationError::InvalidCharacterCode(code.to_string()))
}

#[cfg(test)]
mod tests {
    use std::path::Path;

    use super::{Scheme, recover, recover_both};
    use crate::infrastructure::variants::{load_builtin, load_file};

    #[test]
    fn variant_11_matches_for_both_schemes_and_share_counts() {
        let input = load_builtin(11).unwrap();
        for share_count in [3, 5] {
            let [shamir, blakley] = recover_both(&input, share_count).unwrap();
            for report in [&shamir, &blakley] {
                assert_eq!(report.word, "ЕХИДНА");
                assert_eq!(
                    report
                        .symbols
                        .iter()
                        .map(|symbol| symbol.code.to_string())
                        .collect::<Vec<_>>(),
                    ["197", "213", "200", "196", "205", "192"]
                );
            }
            assert!(
                shamir
                    .symbols
                    .iter()
                    .all(|symbol| symbol.solution[1].to_string() == "9"
                        && symbol.solution[2].to_string() == "5")
            );
            assert!(
                blakley
                    .symbols
                    .iter()
                    .all(|symbol| symbol.solution[1].to_string() == "5"
                        && symbol.solution[2].to_string() == "8")
            );
        }
        assert!(recover(&input, Scheme::Shamir, 4).is_err());
    }

    #[test]
    fn every_builtin_variant_recovers_consistently() {
        for number in 1..=20 {
            let input = load_builtin(number).unwrap();
            let [shamir_three, blakley_three] = recover_both(&input, 3).unwrap();
            let [shamir_five, blakley_five] = recover_both(&input, 5).unwrap();
            assert_eq!(shamir_three.word, blakley_three.word, "вариант {number}");
            assert_eq!(shamir_three.word, shamir_five.word, "вариант {number}");
            assert_eq!(shamir_three.word, blakley_five.word, "вариант {number}");
            assert_eq!(shamir_three.symbols.len(), 6, "вариант {number}");
        }
    }

    #[test]
    fn custom_input_can_use_another_word_and_polynomial() {
        let path = Path::new(concat!(
            env!("CARGO_MANIFEST_DIR"),
            "/examples/custom_kot.json"
        ));
        let input = load_file(path).unwrap();
        for count in [3, 5] {
            let [shamir, blakley] = recover_both(&input, count).unwrap();
            assert_eq!(shamir.word, "КОТ");
            assert_eq!(blakley.word, "КОТ");
            assert_eq!(shamir.symbols[0].solution[1].to_string(), "4");
            assert_eq!(shamir.symbols[0].solution[2].to_string(), "3");
        }
    }
}
