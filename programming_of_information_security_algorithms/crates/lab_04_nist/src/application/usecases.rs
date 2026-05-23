//! Сценарий: загрузить последовательность, прогнать выбранные тесты,
//! сохранить отчёт.

use std::path::Path;

use color_eyre::Result;
use color_eyre::eyre::WrapErr;
use tracing::{info, instrument};

use crate::domain::{NistTestResult, monobit, runs};
use crate::infrastructure::loader::{Format, detect_format, load_bits};
use crate::infrastructure::report::{format_report, save_report};

/// Какие тесты запускать.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Suite {
    /// Только основной — Monobit Frequency.
    Monobit,
    /// Monobit + Runs.
    MonobitAndRuns,
}

pub struct AnalyseUseCase;

impl AnalyseUseCase {
    /// # Errors
    /// Ошибки чтения входного файла или записи отчёта.
    #[instrument(level = "info", skip(suite), fields(input = %input.display()))]
    pub fn run(
        input: &Path,
        format: Option<Format>,
        suite: Suite,
        out_report: Option<&Path>,
    ) -> Result<(Vec<NistTestResult>, String)> {
        let format = format.unwrap_or_else(|| detect_format(input));
        let bits = load_bits(input, format)
            .wrap_err_with(|| format!("чтение последовательности из {}", input.display()))?;
        info!(n = bits.len(), ?format, ?suite, "starting NIST tests");

        let mut results = Vec::new();
        results.push(monobit(&bits));
        if matches!(suite, Suite::MonobitAndRuns) {
            results.push(runs(&bits));
        }

        let report = format_report(input, &results);
        if let Some(p) = out_report {
            save_report(&report, p).wrap_err_with(|| format!("запись отчёта в {}", p.display()))?;
            info!(out = %p.display(), "report saved");
        }
        Ok((results, report))
    }
}

#[cfg(test)]
mod tests {
    use std::fs;
    use std::path::PathBuf;

    use super::*;

    fn tmp(name: &str) -> PathBuf {
        let pid = std::process::id();
        let nanos = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .map(|d| d.subsec_nanos())
            .unwrap_or(0);
        std::env::temp_dir().join(format!("psia_lab04_uc_{name}_{pid}_{nanos}"))
    }

    #[test]
    fn analyse_accepts_alternating_bits_with_monobit() {
        let path = tmp("alt.bits");
        let body: String = (0..1000)
            .map(|i| if i % 2 == 0 { '0' } else { '1' })
            .collect();
        fs::write(&path, body).unwrap();
        let (results, _) =
            AnalyseUseCase::run(&path, Some(Format::Ascii), Suite::Monobit, None).unwrap();
        assert_eq!(results.len(), 1);
        assert!(results[0].passed());
        let _ = fs::remove_file(path);
    }

    #[test]
    fn analyse_rejects_constant_bits() {
        let path = tmp("zeros.bits");
        fs::write(&path, "0".repeat(1000)).unwrap();
        let (results, _) =
            AnalyseUseCase::run(&path, Some(Format::Ascii), Suite::MonobitAndRuns, None).unwrap();
        assert_eq!(results.len(), 2);
        for r in &results {
            assert!(!r.passed(), "{} прошёл, но не должен", r.name);
        }
        let _ = fs::remove_file(path);
    }

    #[test]
    fn writes_report_file() {
        let path = tmp("seq.bits");
        let report_path = tmp("report.txt");
        let body: String = (0..200)
            .map(|i| if i % 2 == 0 { '0' } else { '1' })
            .collect();
        fs::write(&path, body).unwrap();
        AnalyseUseCase::run(
            &path,
            Some(Format::Ascii),
            Suite::Monobit,
            Some(&report_path),
        )
        .unwrap();
        let report = fs::read_to_string(&report_path).unwrap();
        assert!(report.contains("Frequency"));
        let _ = fs::remove_file(path);
        let _ = fs::remove_file(report_path);
    }
}
