//! Сценарии лаб 3.

use crate::domain::cipher::{Substitution, parse_codes};
use crate::domain::errors::DomainError;
use crate::domain::frequency::{count_codes, initial_substitution};

#[derive(Debug, Clone)]
pub struct AnalysisReport {
    pub cipher_codes: Vec<u32>,
    pub frequencies: Vec<(u32, usize)>,
    pub initial_substitution: Substitution,
    pub initial_plain: String,
}

pub fn analyze(text: &str) -> Result<AnalysisReport, DomainError> {
    let codes = parse_codes(text)?;
    let freq = count_codes(&codes);
    let sub = initial_substitution(&codes);
    let plain = sub.apply(&codes);
    Ok(AnalysisReport {
        cipher_codes: codes,
        frequencies: freq,
        initial_substitution: sub,
        initial_plain: plain,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn analyze_short_text() {
        let r = analyze("50 50 50 45 45 42").unwrap();
        assert_eq!(r.cipher_codes.len(), 6);
        // 50 — наиболее частый, должен быть '_'.
        assert_eq!(r.initial_substitution.map.get(&50), Some(&'_'));
    }
}
