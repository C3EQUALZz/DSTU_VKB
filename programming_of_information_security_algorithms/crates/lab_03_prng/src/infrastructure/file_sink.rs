//! Запись последовательности в два вида файлов:
//! бинарный (для STS-режима «1 — Binary») и ASCII (для «0 — ASCII»).

use std::fs;
use std::path::{Path, PathBuf};

use thiserror::Error;
use tracing::{info, instrument};

use crate::domain::Sequence;

#[derive(Debug, Error)]
pub enum SinkError {
    #[error("не удалось записать {path}: {source}")]
    Write {
        path: PathBuf,
        #[source]
        source: std::io::Error,
    },
}

fn write(bytes: &[u8], path: &Path) -> Result<(), SinkError> {
    if let Some(parent) = path.parent() {
        if !parent.as_os_str().is_empty() {
            fs::create_dir_all(parent).map_err(|e| SinkError::Write {
                path: parent.to_path_buf(),
                source: e,
            })?;
        }
    }
    fs::write(path, bytes).map_err(|e| SinkError::Write {
        path: path.to_path_buf(),
        source: e,
    })
}

/// Сохраняет бинарное представление (`Sequence::to_binary_be`) в файл.
///
/// # Errors
/// Любая ошибка IO.
#[instrument(level = "info", skip(seq), fields(path = %path.display()))]
pub fn save_binary(seq: &Sequence, path: &Path) -> Result<(), SinkError> {
    let bytes = seq.to_binary_be();
    write(&bytes, path)?;
    info!(bytes = bytes.len(), "binary sequence saved");
    Ok(())
}

/// Сохраняет ASCII-представление (`Sequence::to_ascii_bits`) с финальным `\n`.
/// Это именно тот формат, который NIST STS принимает в режиме «0 — ASCII».
///
/// # Errors
/// Любая ошибка IO.
#[instrument(level = "info", skip(seq), fields(path = %path.display()))]
pub fn save_ascii(seq: &Sequence, path: &Path) -> Result<(), SinkError> {
    let mut body = seq.to_ascii_bits();
    body.push('\n');
    write(body.as_bytes(), path)?;
    info!(bits = seq.bit_count(), "ascii sequence saved");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::domain::generate;

    fn tmp(name: &str) -> PathBuf {
        let pid = std::process::id();
        let nanos = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .map(|d| d.subsec_nanos())
            .unwrap_or(0);
        std::env::temp_dir().join(format!("psia_lab03_{name}_{pid}_{nanos}"))
    }

    #[test]
    fn save_binary_produces_correct_size() {
        let seq = generate(0x1234, 200);
        let path = tmp("seq.bin");
        save_binary(&seq, &path).unwrap();
        assert_eq!(fs::metadata(&path).unwrap().len(), 200 * 8);
        let _ = fs::remove_file(path);
    }

    #[test]
    fn save_ascii_produces_correct_size() {
        let seq = generate(0x1234, 200);
        let path = tmp("seq.bits");
        save_ascii(&seq, &path).unwrap();
        // 200 * 64 бит + терминирующий перевод строки.
        assert_eq!(fs::metadata(&path).unwrap().len(), 200 * 64 + 1);
        let body = fs::read_to_string(&path).unwrap();
        assert!(body.ends_with('\n'));
        assert!(
            body.chars()
                .take_while(|&c| c != '\n')
                .all(|c| c == '0' || c == '1')
        );
        let _ = fs::remove_file(path);
    }
}
