//! Формирование текстового отчёта по NIST-тестам.

use std::fmt::Write as _;
use std::fs;
use std::path::{Path, PathBuf};

use thiserror::Error;

use crate::domain::NistTestResult;

#[derive(Debug, Error)]
pub enum ReportError {
    #[error("не удалось записать отчёт в {path}: {source}")]
    Write {
        path: PathBuf,
        #[source]
        source: std::io::Error,
    },
}

/// Форматирует результат(ы) в человеко-читаемый отчёт.
#[must_use]
pub fn format_report(input: &Path, results: &[NistTestResult]) -> String {
    let mut s = String::new();
    let _ = writeln!(s, "Источник: {}", input.display());
    let _ = writeln!(s, "Всего тестов: {}", results.len());
    let _ = writeln!(s, "{}", "─".repeat(78));

    for r in results {
        let _ = writeln!(s, "{}", r.name);
        let _ = writeln!(s, "    n      = {}", r.n);
        let _ = writeln!(s, "    ones   = {}", r.ones);
        let _ = writeln!(s, "    zeros  = {}", r.zeros);
        for (k, v) in &r.details {
            let _ = writeln!(s, "    {k:<22} = {v}");
        }
        let _ = writeln!(s, "    P-value = {:.6}", r.p_value);
        let _ = writeln!(s, "    Verdict: {}", r.verdict.label());
        let _ = writeln!(s, "{}", "─".repeat(78));
    }
    s
}

/// Сохраняет отчёт в файл.
///
/// # Errors
/// Любая ошибка IO.
pub fn save_report(text: &str, target: &Path) -> Result<(), ReportError> {
    if let Some(parent) = target.parent() {
        if !parent.as_os_str().is_empty() {
            fs::create_dir_all(parent).map_err(|e| ReportError::Write {
                path: parent.to_path_buf(),
                source: e,
            })?;
        }
    }
    fs::write(target, text).map_err(|e| ReportError::Write {
        path: target.to_path_buf(),
        source: e,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::domain::monobit;

    #[test]
    fn report_contains_expected_fields() {
        let bits: Vec<bool> = (0..100).map(|i| i % 2 == 0).collect();
        let r = monobit(&bits);
        let report = format_report(Path::new("seq.bits"), &[r]);
        assert!(report.contains("Frequency"));
        assert!(report.contains("P-value"));
        assert!(report.contains("Verdict"));
        assert!(report.contains("RANDOM"));
    }
}
