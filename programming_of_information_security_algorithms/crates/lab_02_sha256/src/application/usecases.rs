//! Сценарии: подсчитать хеш файла и проверить хеш файла против сохранённого.

use std::fs::File;
use std::io::{BufReader, Read};
use std::path::Path;

use color_eyre::Result;
use color_eyre::eyre::WrapErr;
use tracing::{debug, info, instrument};

use crate::domain::sha256::{self, DIGEST_BYTES, Sha256, to_hex};
use crate::infrastructure::hash_io;

const READ_BUFFER: usize = 64 * 1024;

/// Результат проверки.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Verdict {
    Match,
    Mismatch,
}

/// Подсчитывает SHA-256 файла стримом, без загрузки в память.
///
/// # Errors
/// Ошибки чтения файла.
#[instrument(level = "info", fields(path = ?path.as_ref()))]
pub fn hash_file_stream(path: impl AsRef<Path>) -> Result<[u8; DIGEST_BYTES]> {
    let path = path.as_ref();
    let file =
        File::open(path).wrap_err_with(|| format!("не удалось открыть файл {}", path.display()))?;
    let mut reader = BufReader::with_capacity(READ_BUFFER, file);
    let mut hasher = Sha256::new();
    let mut buf = vec![0u8; READ_BUFFER];
    let mut total: u64 = 0;
    loop {
        let n = reader
            .read(&mut buf)
            .wrap_err_with(|| format!("ошибка чтения {}", path.display()))?;
        if n == 0 {
            break;
        }
        hasher.update(&buf[..n]);
        total += n as u64;
        debug!(bytes_read = total, "fed chunk to hasher");
    }
    let d = hasher.finalize();
    info!(file_bytes = total, digest = to_hex(&d), "file hashed");
    Ok(d)
}

/// Сценарий: посчитать хеш файла и сохранить его в `<output>`.
pub struct HashFileUseCase;

impl HashFileUseCase {
    /// # Errors
    /// Ошибки чтения/записи файлов.
    pub fn run(input: &Path, output: Option<&Path>) -> Result<[u8; DIGEST_BYTES]> {
        let digest = hash_file_stream(input)?;
        if let Some(out_path) = output {
            hash_io::save_digest(&digest, input, out_path)
                .wrap_err_with(|| format!("запись хеша в {}", out_path.display()))?;
            info!(out = ?out_path, "digest written");
        }
        Ok(digest)
    }
}

/// Сценарий: посчитать хеш файла и сравнить с тем, что в `<expected_file>`.
pub struct VerifyHashUseCase;

impl VerifyHashUseCase {
    /// # Errors
    /// Любые ошибки IO или неверный формат файла с хешем.
    pub fn run(input: &Path, expected_file: &Path) -> Result<(Verdict, [u8; DIGEST_BYTES])> {
        let expected = hash_io::load_digest(expected_file)
            .wrap_err_with(|| format!("чтение хеша из {}", expected_file.display()))?;
        let actual = hash_file_stream(input)?;
        let verdict = if actual == expected {
            Verdict::Match
        } else {
            Verdict::Mismatch
        };
        info!(
            verdict = ?verdict,
            expected = to_hex(&expected),
            actual = to_hex(&actual),
            "verification finished"
        );
        Ok((verdict, actual))
    }
}

// Прокидываем для удобства внешних пользователей.
pub use sha256::digest as hash_bytes;
