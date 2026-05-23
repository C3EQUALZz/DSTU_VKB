//! Сохранение/загрузка ключей и шифртекста.

use std::fs;
use std::path::{Path, PathBuf};

use thiserror::Error;

use crate::domain::cipher::{RawPrivateKey, RawPublicKey};
use crate::domain::keys::{
    KeyFileError, pack_ciphertext, pack_private, pack_public, unpack_ciphertext, unpack_private,
    unpack_public,
};

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
    #[error("в файле {path} неверный формат: {source}")]
    Format {
        path: PathBuf,
        #[source]
        source: KeyFileError,
    },
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

/// # Errors
/// Ошибка IO.
pub fn save_public(key: &RawPublicKey, path: &Path) -> Result<(), StorageError> {
    ensure_parent(path)?;
    fs::write(path, pack_public(key)).map_err(|e| StorageError::Write {
        path: path.to_path_buf(),
        source: e,
    })
}

/// # Errors
/// Ошибка IO.
pub fn save_private(key: &RawPrivateKey, path: &Path) -> Result<(), StorageError> {
    ensure_parent(path)?;
    fs::write(path, pack_private(key)).map_err(|e| StorageError::Write {
        path: path.to_path_buf(),
        source: e,
    })
}

/// # Errors
/// Ошибка IO.
pub fn save_ciphertext(payload: &[u8], path: &Path) -> Result<(), StorageError> {
    ensure_parent(path)?;
    fs::write(path, pack_ciphertext(payload)).map_err(|e| StorageError::Write {
        path: path.to_path_buf(),
        source: e,
    })
}

/// # Errors
/// IO или формат файла.
pub fn load_public(path: &Path) -> Result<RawPublicKey, StorageError> {
    let bytes = fs::read(path).map_err(|e| StorageError::Read {
        path: path.to_path_buf(),
        source: e,
    })?;
    unpack_public(&bytes).map_err(|e| StorageError::Format {
        path: path.to_path_buf(),
        source: e,
    })
}

/// # Errors
/// IO или формат файла.
pub fn load_private(path: &Path) -> Result<RawPrivateKey, StorageError> {
    let bytes = fs::read(path).map_err(|e| StorageError::Read {
        path: path.to_path_buf(),
        source: e,
    })?;
    unpack_private(&bytes).map_err(|e| StorageError::Format {
        path: path.to_path_buf(),
        source: e,
    })
}

/// # Errors
/// IO или формат файла.
pub fn load_ciphertext(path: &Path) -> Result<Vec<u8>, StorageError> {
    let bytes = fs::read(path).map_err(|e| StorageError::Read {
        path: path.to_path_buf(),
        source: e,
    })?;
    unpack_ciphertext(&bytes).map_err(|e| StorageError::Format {
        path: path.to_path_buf(),
        source: e,
    })
}
