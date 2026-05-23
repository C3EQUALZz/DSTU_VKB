//! Чтение/запись ключей и шифртекста.
//!
//! Формат намеренно простой и человекочитаемый — не PEM/DER, чтобы не тащить
//! `base64`/`asn1`. Поля — `key = value` в hex с префиксом `0x`. Это полностью
//! достаточно для лабораторной: записали → прочитали → сравнили побайтово.

use std::fs;
use std::path::{Path, PathBuf};

use thiserror::Error;
use tracing::{debug, info, instrument};

use crate::domain::bigint::BigUint;
use crate::domain::rsa::{PrivateKey, PublicKey};

#[derive(Debug, Error)]
pub enum StorageError {
    #[error("не удалось прочитать {path:?}: {source}")]
    Read {
        path: PathBuf,
        #[source]
        source: std::io::Error,
    },
    #[error("не удалось записать {path:?}: {source}")]
    Write {
        path: PathBuf,
        #[source]
        source: std::io::Error,
    },
    #[error("в файле {path:?} отсутствует обязательное поле {field}")]
    MissingField { path: PathBuf, field: &'static str },
    #[error("в файле {path:?} поле {field} не разобрано: {reason}")]
    InvalidField {
        path: PathBuf,
        field: &'static str,
        reason: String,
    },
}

const PUBLIC_HEADER: &str = "# RSA public key (lab 1, учебный формат)";
const PRIVATE_HEADER: &str = "# RSA private key (lab 1, учебный формат)";

/// Сохраняет открытый ключ в файл.
///
/// # Errors
/// Любые ошибки записи на диск.
#[instrument(level = "info", skip(key), fields(path = ?path.as_ref()))]
pub fn save_public_key(key: &PublicKey, path: impl AsRef<Path>) -> Result<(), StorageError> {
    let body = format_public_key(key);
    write_text(&body, path.as_ref())?;
    info!(bits = key.bits, "public key saved");
    Ok(())
}

/// Сохраняет закрытый ключ в файл.
///
/// # Errors
/// Любые ошибки записи на диск.
#[instrument(level = "info", skip(key), fields(path = ?path.as_ref()))]
pub fn save_private_key(key: &PrivateKey, path: impl AsRef<Path>) -> Result<(), StorageError> {
    let body = format_private_key(key);
    write_text(&body, path.as_ref())?;
    info!(bits = key.bits, "private key saved");
    Ok(())
}

/// Читает открытый ключ.
///
/// # Errors
/// Если файл недоступен или не соответствует ожидаемому формату.
#[instrument(level = "info", fields(path = ?path.as_ref()))]
pub fn load_public_key(path: impl AsRef<Path>) -> Result<PublicKey, StorageError> {
    let path = path.as_ref();
    let text = fs::read_to_string(path).map_err(|e| StorageError::Read {
        path: path.to_path_buf(),
        source: e,
    })?;
    let bits = parse_usize(&text, path, "bits")?;
    let n = parse_biguint(&text, path, "n")?;
    let e = parse_biguint(&text, path, "e")?;
    debug!(bits, "public key loaded");
    Ok(PublicKey { n, e, bits })
}

/// Читает закрытый ключ.
///
/// # Errors
/// Если файл недоступен или не соответствует ожидаемому формату.
#[instrument(level = "info", fields(path = ?path.as_ref()))]
pub fn load_private_key(path: impl AsRef<Path>) -> Result<PrivateKey, StorageError> {
    let path = path.as_ref();
    let text = fs::read_to_string(path).map_err(|e| StorageError::Read {
        path: path.to_path_buf(),
        source: e,
    })?;
    let bits = parse_usize(&text, path, "bits")?;
    let n = parse_biguint(&text, path, "n")?;
    let e = parse_biguint(&text, path, "e")?;
    let d = parse_biguint(&text, path, "d")?;
    let p = parse_biguint(&text, path, "p")?;
    let q = parse_biguint(&text, path, "q")?;
    debug!(bits, "private key loaded");
    Ok(PrivateKey {
        n,
        e,
        d,
        p,
        q,
        bits,
    })
}

/// Сохраняет произвольные байты (шифртекст) в файл.
///
/// # Errors
/// Ошибка ввода-вывода.
pub fn save_bytes(bytes: &[u8], path: impl AsRef<Path>) -> Result<(), StorageError> {
    let path = path.as_ref();
    if let Some(parent) = path.parent() {
        if !parent.as_os_str().is_empty() {
            fs::create_dir_all(parent).map_err(|e| StorageError::Write {
                path: parent.to_path_buf(),
                source: e,
            })?;
        }
    }
    fs::write(path, bytes).map_err(|e| StorageError::Write {
        path: path.to_path_buf(),
        source: e,
    })
}

/// Читает произвольные байты из файла.
///
/// # Errors
/// Ошибка ввода-вывода.
pub fn load_bytes(path: impl AsRef<Path>) -> Result<Vec<u8>, StorageError> {
    let path = path.as_ref();
    fs::read(path).map_err(|e| StorageError::Read {
        path: path.to_path_buf(),
        source: e,
    })
}

fn write_text(body: &str, path: &Path) -> Result<(), StorageError> {
    if let Some(parent) = path.parent() {
        if !parent.as_os_str().is_empty() {
            fs::create_dir_all(parent).map_err(|e| StorageError::Write {
                path: parent.to_path_buf(),
                source: e,
            })?;
        }
    }
    fs::write(path, body).map_err(|e| StorageError::Write {
        path: path.to_path_buf(),
        source: e,
    })
}

fn format_public_key(key: &PublicKey) -> String {
    format!(
        "{PUBLIC_HEADER}\nbits = {bits}\nn = 0x{n}\ne = 0x{e}\n",
        bits = key.bits,
        n = key.n.to_hex(),
        e = key.e.to_hex(),
    )
}

fn format_private_key(key: &PrivateKey) -> String {
    format!(
        "{PRIVATE_HEADER}\nbits = {bits}\nn = 0x{n}\ne = 0x{e}\nd = 0x{d}\np = 0x{p}\nq = 0x{q}\n",
        bits = key.bits,
        n = key.n.to_hex(),
        e = key.e.to_hex(),
        d = key.d.to_hex(),
        p = key.p.to_hex(),
        q = key.q.to_hex(),
    )
}

fn find_field<'a>(text: &'a str, field: &str) -> Option<&'a str> {
    for line in text.lines() {
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        if let Some((key, value)) = line.split_once('=') {
            if key.trim() == field {
                return Some(value.trim());
            }
        }
    }
    None
}

fn parse_biguint(text: &str, path: &Path, field: &'static str) -> Result<BigUint, StorageError> {
    let value = find_field(text, field).ok_or(StorageError::MissingField {
        path: path.to_path_buf(),
        field,
    })?;
    BigUint::parse(value).map_err(|e| StorageError::InvalidField {
        path: path.to_path_buf(),
        field,
        reason: e.to_string(),
    })
}

fn parse_usize(text: &str, path: &Path, field: &'static str) -> Result<usize, StorageError> {
    let value = find_field(text, field).ok_or(StorageError::MissingField {
        path: path.to_path_buf(),
        field,
    })?;
    value
        .parse::<usize>()
        .map_err(|e| StorageError::InvalidField {
            path: path.to_path_buf(),
            field,
            reason: e.to_string(),
        })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::domain::rng::DeterministicRng;
    use crate::domain::rsa::KeyPair;

    #[test]
    fn public_key_round_trips_through_disk() {
        let mut rng = DeterministicRng::new(99);
        let kp = KeyPair::generate(128, &mut rng);
        let tmp = std::env::temp_dir().join("psia_lab01_pubkey.txt");
        save_public_key(&kp.public, &tmp).unwrap();
        let loaded = load_public_key(&tmp).unwrap();
        assert_eq!(loaded, kp.public);
        let _ = fs::remove_file(tmp);
    }

    #[test]
    fn private_key_round_trips_through_disk() {
        let mut rng = DeterministicRng::new(100);
        let kp = KeyPair::generate(128, &mut rng);
        let tmp = std::env::temp_dir().join("psia_lab01_privkey.txt");
        save_private_key(&kp.private, &tmp).unwrap();
        let loaded = load_private_key(&tmp).unwrap();
        assert_eq!(loaded, kp.private);
        let _ = fs::remove_file(tmp);
    }

    #[test]
    fn missing_field_is_reported() {
        let tmp = std::env::temp_dir().join("psia_lab01_bad_key.txt");
        fs::write(&tmp, "bits = 128\nn = 0x1\n").unwrap();
        let err = load_public_key(&tmp).unwrap_err();
        assert!(matches!(err, StorageError::MissingField { field: "e", .. }));
        let _ = fs::remove_file(tmp);
    }
}
