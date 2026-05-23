//! Шифр простой замены: каждой букве сопоставляется уникальный код (число).
//!
//! В лаб 3 методички шифр представлен в виде потока чисел, разделённых пробелами,
//! где запятые и пробелы внутри текста сохранены. Программа здесь работает с
//! абстрактным «токеном» — числом, представляющим один символ.

use std::collections::HashMap;

use super::errors::DomainError;

#[derive(Debug, Clone, Default)]
pub struct Substitution {
    /// Карта код → символ открытого текста.
    pub map: HashMap<u32, char>,
}

impl Substitution {
    pub fn apply(&self, codes: &[u32]) -> String {
        codes
            .iter()
            .map(|c| self.map.get(c).copied().unwrap_or('?'))
            .collect()
    }
}

/// Распарсить шифртекст вида «47 39 42 27, 27 50» в массив чисел.
/// Запятые и точки сохраняются как маркеры (-1) — здесь мы их игнорируем.
pub fn parse_codes(text: &str) -> Result<Vec<u32>, DomainError> {
    text.split_whitespace()
        .filter(|t| !t.is_empty())
        .filter_map(|t| {
            let cleaned = t.trim_end_matches(&[',', '.', ';', ':', '!', '?'][..]);
            if cleaned.is_empty() {
                return None;
            }
            Some(
                cleaned
                    .parse::<u32>()
                    .map_err(|_| DomainError::InvalidToken { token: t.to_string() }),
            )
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_basic() {
        let codes = parse_codes("47 39 42, 27 27 50").unwrap();
        assert_eq!(codes, vec![47, 39, 42, 27, 27, 50]);
    }

    #[test]
    fn apply_with_partial_map() {
        let mut sub = Substitution::default();
        sub.map.insert(50, 'О');
        sub.map.insert(45, 'Е');
        let s = sub.apply(&[50, 45, 50, 99]);
        assert_eq!(s, "ОЕО?");
    }
}
