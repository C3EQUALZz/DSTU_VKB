//! Сценарий: сгенерировать `count` 64-битных значений с заданным seed
//! и записать в два формата (binary и ASCII).

use std::path::Path;

use color_eyre::Result;
use color_eyre::eyre::WrapErr;
use tracing::{info, instrument};

use crate::domain::{Sequence, generate};
use crate::infrastructure::file_sink;

/// Минимум по условию лаб 3.
pub const MIN_COUNT_BY_CONDITION: usize = 200;

pub struct GenerateSequenceUseCase;

impl GenerateSequenceUseCase {
    /// # Errors
    /// Любые ошибки записи в файлы.
    #[instrument(level = "info", fields(seed, count))]
    pub fn run(
        seed: u64,
        count: usize,
        out_binary: Option<&Path>,
        out_ascii: Option<&Path>,
    ) -> Result<Sequence> {
        assert!(
            count >= MIN_COUNT_BY_CONDITION,
            "по условию лаб 3 требуется ≥ {MIN_COUNT_BY_CONDITION} значений; запрошено {count}"
        );
        info!(seed, count, "generating PRNG sequence");
        let seq = generate(seed, count);
        if let Some(p) = out_binary {
            file_sink::save_binary(&seq, p)
                .wrap_err_with(|| format!("сохранение бинарного файла {}", p.display()))?;
        }
        if let Some(p) = out_ascii {
            file_sink::save_ascii(&seq, p)
                .wrap_err_with(|| format!("сохранение ASCII-файла {}", p.display()))?;
        }
        info!(
            words = seq.word_count(),
            bits = seq.bit_count(),
            "sequence ready"
        );
        Ok(seq)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;
    use std::path::PathBuf;

    fn tmp(name: &str) -> PathBuf {
        let pid = std::process::id();
        let nanos = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .map(|d| d.subsec_nanos())
            .unwrap_or(0);
        std::env::temp_dir().join(format!("psia_lab03_uc_{name}_{pid}_{nanos}"))
    }

    #[test]
    fn generates_both_files() {
        let bin = tmp("a.bin");
        let asc = tmp("a.bits");
        let seq = GenerateSequenceUseCase::run(0x42, 200, Some(&bin), Some(&asc)).unwrap();
        assert_eq!(seq.word_count(), 200);
        assert_eq!(fs::metadata(&bin).unwrap().len(), 200 * 8);
        assert_eq!(fs::metadata(&asc).unwrap().len(), 200 * 64 + 1);
        let _ = fs::remove_file(bin);
        let _ = fs::remove_file(asc);
    }

    #[test]
    #[should_panic(expected = "по условию")]
    fn rejects_count_below_minimum() {
        let _ = GenerateSequenceUseCase::run(1, 100, None, None);
    }
}
