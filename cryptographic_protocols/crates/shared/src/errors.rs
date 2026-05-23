//! Общие доменные ошибки для лабораторных.

use std::path::PathBuf;

use thiserror::Error;

#[derive(Debug, Error)]
pub enum InfraError {
    #[error("не удалось прочитать файл {path:?}: {source}")]
    Read {
        path: PathBuf,
        #[source]
        source: std::io::Error,
    },

    #[error("не удалось записать файл {path:?}: {source}")]
    Write {
        path: PathBuf,
        #[source]
        source: std::io::Error,
    },

    #[error("файл {path:?} имеет неверный формат: {reason}")]
    InvalidFormat { path: PathBuf, reason: String },
}

impl InfraError {
    pub fn read(path: impl Into<PathBuf>, source: std::io::Error) -> Self {
        Self::Read {
            path: path.into(),
            source,
        }
    }

    pub fn write(path: impl Into<PathBuf>, source: std::io::Error) -> Self {
        Self::Write {
            path: path.into(),
            source,
        }
    }

    pub fn invalid(path: impl Into<PathBuf>, reason: impl Into<String>) -> Self {
        Self::InvalidFormat {
            path: path.into(),
            reason: reason.into(),
        }
    }
}
