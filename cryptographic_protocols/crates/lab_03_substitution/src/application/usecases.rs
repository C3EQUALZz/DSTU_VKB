//! Сценарии лаб 3.

use shared::alphabet::ALPHABET;

use crate::domain::cipher::{Substitution, parse_codes};
use crate::domain::errors::DomainError;
use crate::domain::frequency::{count_codes, initial_substitution};
use crate::domain::solver;

#[derive(Debug, Clone)]
pub struct SolveReport {
    pub cipher_codes: Vec<u32>,
    pub plain: String,
    pub key_map: Vec<(u32, char)>,
    pub fitness: f64,
}

#[tracing::instrument(skip_all)]
pub fn solve_cipher(text: &str, rounds: usize, iters: usize) -> Result<SolveReport, DomainError> {
    tracing::info!("разбор числового шифртекста");
    let codes = parse_codes(text)?;
    tracing::info!(tokens = codes.len(), "шифртекст разобран");
    tracing::info!(rounds, iters, "начат подбор подстановки по биграммам");
    let sol = solver::solve(&codes, rounds, iters);
    let plain: String = codes.iter().map(|c| ALPHABET[sol.map[c]]).collect();
    let mut key_map: Vec<(u32, char)> = sol.map.iter().map(|(&c, &i)| (c, ALPHABET[i])).collect();
    key_map.sort_by_key(|(c, _)| *c);
    tracing::info!(
        fitness = sol.fitness,
        symbols = codes.len(),
        "подбор подстановки завершён"
    );
    Ok(SolveReport {
        cipher_codes: codes,
        plain,
        key_map,
        fitness: sol.fitness,
    })
}

#[derive(Debug, Clone)]
pub struct AnalysisReport {
    pub cipher_codes: Vec<u32>,
    pub frequencies: Vec<(u32, usize)>,
    pub initial_substitution: Substitution,
    pub initial_plain: String,
}

#[tracing::instrument(skip_all)]
pub fn analyze(text: &str) -> Result<AnalysisReport, DomainError> {
    tracing::info!("разбор числового шифртекста");
    let codes = parse_codes(text)?;
    tracing::info!(tokens = codes.len(), "шифртекст разобран");
    let freq = count_codes(&codes);
    let sub = initial_substitution(&codes);
    let plain = sub.apply(&codes);
    for (rank, &(code, count)) in freq.iter().enumerate() {
        tracing::info!(rank = rank+1, code, count, proposed_letter = ?sub.map.get(&code), "начальная частотная подстановка");
    }
    tracing::info!(unique_codes = freq.len(), "частотный анализ завершён");
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
