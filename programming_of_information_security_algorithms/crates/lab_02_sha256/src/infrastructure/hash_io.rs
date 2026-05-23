//! Чтение и запись `.sha256`-файлов в формате, совместимом с `shasum -a 256`:
//!
//! ```text
//! <64-hex-char digest>  <filename>
//! ```
//!
//! Два пробела между хешем и именем — это стандарт coreutils. Имя файла
//! может содержать пробелы и сохраняется как есть.

use std::fs;
use std::path::{Path, PathBuf};

use thiserror::Error;

use crate::domain::sha256::{DIGEST_BYTES, ParseDigestError, from_hex, to_hex};

#[derive(Debug, Error)]
pub enum HashIoError {
    #[error("не удалось прочитать {path}: {source}")]
    Read {
        path: PathBuf,
        #[source]
        source: std::io::Error,
    },
    #[error("не удалось записать {path}: {source}")]
    Write {
        path: PathBuf,
        #[source]
        source: std::io::Error,
    },
    #[error("в файле {path} не найден дайджест в формате shasum")]
    Empty { path: PathBuf },
    #[error("в файле {path} некорректный hex дайджест: {source}")]
    BadDigest {
        path: PathBuf,
        #[source]
        source: ParseDigestError,
    },
}

/// Сохраняет дайджест в файл в формате `shasum -a 256`.
///
/// # Errors
/// Любые ошибки IO.
pub fn save_digest(
    digest: &[u8; DIGEST_BYTES],
    source_file: &Path,
    target: &Path,
) -> Result<(), HashIoError> {
    if let Some(parent) = target.parent() {
        if !parent.as_os_str().is_empty() {
            fs::create_dir_all(parent).map_err(|e| HashIoError::Write {
                path: parent.to_path_buf(),
                source: e,
            })?;
        }
    }
    let name = source_file.file_name().map_or_else(
        || source_file.display().to_string(),
        |s| s.to_string_lossy().into_owned(),
    );
    let body = format!("{hex}  {name}\n", hex = to_hex(digest));
    fs::write(target, body).map_err(|e| HashIoError::Write {
        path: target.to_path_buf(),
        source: e,
    })?;
    Ok(())
}

/// Читает первый дайджест из shasum-файла.
///
/// # Errors
/// Не удалось открыть файл, пуст или дайджест нечитаемый.
pub fn load_digest(path: &Path) -> Result<[u8; DIGEST_BYTES], HashIoError> {
    let text = fs::read_to_string(path).map_err(|e| HashIoError::Read {
        path: path.to_path_buf(),
        source: e,
    })?;
    for line in text.lines() {
        let trimmed = line.trim();
        if trimmed.is_empty() || trimmed.starts_with('#') {
            continue;
        }
        // shasum: "<hex>  <filename>" — берём первый whitespace-разделитель.
        let hex_part = trimmed.split_whitespace().next().unwrap_or(trimmed);
        return from_hex(hex_part).map_err(|e| HashIoError::BadDigest {
            path: path.to_path_buf(),
            source: e,
        });
    }
    Err(HashIoError::Empty {
        path: path.to_path_buf(),
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::domain::sha256::digest;

    fn tmp(name: &str) -> PathBuf {
        let pid = std::process::id();
        let nanos = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .map(|d| d.subsec_nanos())
            .unwrap_or(0);
        std::env::temp_dir().join(format!("psia_lab02_{name}_{pid}_{nanos}"))
    }

    #[test]
    fn save_and_load_round_trip() {
        let source = tmp("input.txt");
        let target = tmp("input.sha256");
        fs::write(&source, b"hello").unwrap();
        let d = digest(b"hello");
        save_digest(&d, &source, &target).unwrap();
        let body = fs::read_to_string(&target).unwrap();
        assert!(body.starts_with(&to_hex(&d)));
        assert!(body.contains("  ")); // два пробела
        let loaded = load_digest(&target).unwrap();
        assert_eq!(loaded, d);
        let _ = fs::remove_file(source);
        let _ = fs::remove_file(target);
    }

    #[test]
    fn loads_from_shasum_compatible_file() {
        let target = tmp("manual.sha256");
        // Эталон, который сгенерировал бы coreutils `shasum -a 256 file`.
        let body = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad  file\n";
        fs::write(&target, body).unwrap();
        let loaded = load_digest(&target).unwrap();
        assert_eq!(
            to_hex(&loaded),
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        );
        let _ = fs::remove_file(target);
    }

    #[test]
    fn empty_file_is_rejected() {
        let target = tmp("empty.sha256");
        fs::write(&target, "").unwrap();
        let err = load_digest(&target).unwrap_err();
        assert!(matches!(err, HashIoError::Empty { .. }));
        let _ = fs::remove_file(target);
    }
}
