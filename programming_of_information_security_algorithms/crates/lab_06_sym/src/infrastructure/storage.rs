//! Чтение/запись ключа и шифртекста на диск.

use std::fs;
use std::path::{Path, PathBuf};

use thiserror::Error;

use crate::domain::key::{CIPHERTEXT_MAGIC, KeyFormatError, SymmetricKey};

#[derive(Debug, Error)]
pub enum StorageError {
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
    #[error("в файле {path} некорректный формат ключа: {source}")]
    KeyFormat {
        path: PathBuf,
        #[source]
        source: KeyFormatError,
    },
    #[error("в файле {path} неверный magic шифртекста")]
    BadCiphertextMagic { path: PathBuf },
}

fn ensure_parent(path: &Path) -> Result<(), StorageError> {
    if let Some(parent) = path.parent() {
        if !parent.as_os_str().is_empty() {
            fs::create_dir_all(parent).map_err(|e| StorageError::Write {
                path: parent.to_path_buf(),
                source: e,
            })?;
        }
    }
    Ok(())
}

/// Сохраняет ключ в файл (magic + 64 байта = 80 байт всего).
///
/// # Errors
/// Любая ошибка IO.
pub fn save_key(key: &SymmetricKey, path: &Path) -> Result<(), StorageError> {
    ensure_parent(path)?;
    fs::write(path, key.to_file_bytes()).map_err(|e| StorageError::Write {
        path: path.to_path_buf(),
        source: e,
    })
}

/// Читает ключ из файла.
///
/// # Errors
/// Если файл недоступен или не соответствует ожидаемому формату.
pub fn load_key(path: &Path) -> Result<SymmetricKey, StorageError> {
    let bytes = fs::read(path).map_err(|e| StorageError::Read {
        path: path.to_path_buf(),
        source: e,
    })?;
    SymmetricKey::from_file_bytes(&bytes).map_err(|e| StorageError::KeyFormat {
        path: path.to_path_buf(),
        source: e,
    })
}

/// Сохраняет шифртекст: `CIPHERTEXT_MAGIC || raw`.
///
/// `raw` — это вывод [`crate::domain::cipher::seal`].
///
/// # Errors
/// Любая ошибка IO.
pub fn save_ciphertext(raw: &[u8], path: &Path) -> Result<(), StorageError> {
    ensure_parent(path)?;
    let mut body = Vec::with_capacity(CIPHERTEXT_MAGIC.len() + raw.len());
    body.extend_from_slice(CIPHERTEXT_MAGIC);
    body.extend_from_slice(raw);
    fs::write(path, body).map_err(|e| StorageError::Write {
        path: path.to_path_buf(),
        source: e,
    })
}

/// Читает шифртекст и снимает magic-заголовок.
///
/// # Errors
/// Если magic не совпал или файл недоступен.
pub fn load_ciphertext(path: &Path) -> Result<Vec<u8>, StorageError> {
    let bytes = fs::read(path).map_err(|e| StorageError::Read {
        path: path.to_path_buf(),
        source: e,
    })?;
    if bytes.len() < CIPHERTEXT_MAGIC.len() || &bytes[..CIPHERTEXT_MAGIC.len()] != CIPHERTEXT_MAGIC
    {
        return Err(StorageError::BadCiphertextMagic {
            path: path.to_path_buf(),
        });
    }
    Ok(bytes[CIPHERTEXT_MAGIC.len()..].to_vec())
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
        std::env::temp_dir().join(format!("psia_lab06_storage_{name}_{pid}_{nanos}"))
    }

    #[test]
    fn key_round_trip_through_disk() {
        let path = tmp("key");
        let key = SymmetricKey::from_parts([0x11; 32], [0x22; 32]);
        save_key(&key, &path).unwrap();
        let loaded = load_key(&path).unwrap();
        assert_eq!(loaded, key);
        let _ = fs::remove_file(path);
    }

    #[test]
    fn ciphertext_round_trip_through_disk() {
        let path = tmp("ct");
        let raw = b"opaque body".to_vec();
        save_ciphertext(&raw, &path).unwrap();
        let loaded = load_ciphertext(&path).unwrap();
        assert_eq!(loaded, raw);
        let _ = fs::remove_file(path);
    }

    #[test]
    fn bad_ciphertext_magic_reported() {
        let path = tmp("bad_ct");
        fs::write(&path, b"not-a-psia-ciphertext").unwrap();
        let err = load_ciphertext(&path).unwrap_err();
        assert!(matches!(err, StorageError::BadCiphertextMagic { .. }));
        let _ = fs::remove_file(path);
    }
}
