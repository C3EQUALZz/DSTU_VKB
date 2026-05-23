//! Чтение последовательности из файла.
//!
//! Поддерживаются два формата:
//! - **ASCII-биты** — строка из `0` и `1` (с/без переводов строк и пробелов).
//!   Это то, что пишет `lab_03_prng --out-ascii`, а также то, что ест NIST STS.
//! - **Binary** — произвольные байты, каждый разворачивается в 8 бит
//!   (старший бит первым). Это `lab_03_prng --out-bin` или любой бинарный файл.

use std::fs;
use std::path::{Path, PathBuf};

use thiserror::Error;
use tracing::{debug, info};

#[derive(Debug, Error)]
pub enum LoaderError {
    #[error("не удалось прочитать {path}: {source}")]
    Read {
        path: PathBuf,
        #[source]
        source: std::io::Error,
    },
    #[error("в файле {path} нет ни одного бита")]
    Empty { path: PathBuf },
    #[error("в файле {path} ASCII-формат содержит недопустимый символ {ch:?}")]
    BadChar { path: PathBuf, ch: char },
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Format {
    Ascii,
    Binary,
}

/// Авто-детект формата по расширению / содержимому.
/// `.bits` или `.txt` → ASCII; `.bin` → Binary; иначе — по первому байту.
#[must_use]
pub fn detect_format(path: &Path) -> Format {
    match path.extension().and_then(|e| e.to_str()) {
        Some("bits" | "txt" | "ascii") => Format::Ascii,
        // `.bin` или любое незнакомое расширение трактуется как «сырые байты».
        _ => Format::Binary,
    }
}

/// Читает биты из файла.
///
/// # Errors
/// Если файл недоступен, пуст или содержит мусор в ASCII-формате.
pub fn load_bits(path: &Path, format: Format) -> Result<Vec<bool>, LoaderError> {
    let bytes = fs::read(path).map_err(|e| LoaderError::Read {
        path: path.to_path_buf(),
        source: e,
    })?;
    let bits = match format {
        Format::Ascii => parse_ascii(&bytes, path)?,
        Format::Binary => parse_binary(&bytes),
    };
    if bits.is_empty() {
        return Err(LoaderError::Empty {
            path: path.to_path_buf(),
        });
    }
    info!(
        path = %path.display(),
        format = ?format,
        bits = bits.len(),
        "sequence loaded"
    );
    Ok(bits)
}

fn parse_ascii(bytes: &[u8], path: &Path) -> Result<Vec<bool>, LoaderError> {
    let mut bits = Vec::with_capacity(bytes.len());
    for &b in bytes {
        match b {
            b'0' => bits.push(false),
            b'1' => bits.push(true),
            // Игнорируем привычные «пустые» символы.
            b' ' | b'\t' | b'\n' | b'\r' => {}
            _ => {
                return Err(LoaderError::BadChar {
                    path: path.to_path_buf(),
                    ch: b as char,
                });
            }
        }
    }
    debug!(parsed_bits = bits.len(), "parsed ASCII");
    Ok(bits)
}

fn parse_binary(bytes: &[u8]) -> Vec<bool> {
    let mut bits = Vec::with_capacity(bytes.len() * 8);
    for &byte in bytes {
        for i in (0..8).rev() {
            bits.push((byte >> i) & 1 == 1);
        }
    }
    bits
}

#[cfg(test)]
mod tests {
    use super::*;

    fn tmp(name: &str) -> PathBuf {
        let pid = std::process::id();
        let nanos = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .map(|d| d.subsec_nanos())
            .unwrap_or(0);
        std::env::temp_dir().join(format!("psia_lab04_{name}_{pid}_{nanos}"))
    }

    #[test]
    fn detect_known_extensions() {
        assert_eq!(detect_format(Path::new("a.bits")), Format::Ascii);
        assert_eq!(detect_format(Path::new("a.txt")), Format::Ascii);
        assert_eq!(detect_format(Path::new("a.bin")), Format::Binary);
        assert_eq!(detect_format(Path::new("noext")), Format::Binary);
    }

    #[test]
    fn loads_ascii_ignoring_whitespace() {
        let path = tmp("seq.bits");
        fs::write(&path, "01 10\n11 00 ").unwrap();
        let bits = load_bits(&path, Format::Ascii).unwrap();
        assert_eq!(
            bits,
            vec![false, true, true, false, true, true, false, false]
        );
        let _ = fs::remove_file(path);
    }

    #[test]
    fn ascii_rejects_garbage() {
        let path = tmp("bad.bits");
        fs::write(&path, "0101x").unwrap();
        let err = load_bits(&path, Format::Ascii).unwrap_err();
        assert!(matches!(err, LoaderError::BadChar { ch: 'x', .. }));
        let _ = fs::remove_file(path);
    }

    #[test]
    fn loads_binary_msb_first() {
        let path = tmp("seq.bin");
        fs::write(&path, [0b1010_0101u8, 0b1111_0000]).unwrap();
        let bits = load_bits(&path, Format::Binary).unwrap();
        assert_eq!(
            bits,
            vec![
                true, false, true, false, false, true, false, true, true, true, true, true, false,
                false, false, false
            ]
        );
        let _ = fs::remove_file(path);
    }

    #[test]
    fn empty_file_is_rejected() {
        let path = tmp("empty.bits");
        fs::write(&path, "").unwrap();
        let err = load_bits(&path, Format::Ascii).unwrap_err();
        assert!(matches!(err, LoaderError::Empty { .. }));
        let _ = fs::remove_file(path);
    }
}
