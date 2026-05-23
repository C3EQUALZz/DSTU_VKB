//! CLI лаб 6.

use std::path::PathBuf;

use clap::{Parser, Subcommand};
use color_eyre::Result;

use crate::application::{DecryptUseCase, EncryptUseCase, GenerateKeyUseCase};
use crate::domain::cipher::SymmetricCryptoProvider;
use crate::infrastructure::providers::active;

#[derive(Debug, Parser)]
#[command(
    name = "lab_06_sym",
    version,
    about = "Лаб 6 — симметричное шифрование через встроенный криптопровайдер ОС (AES-256-CBC + HMAC-SHA-256, encrypt-then-MAC).",
    long_about = "\
Кросс-платформенная реализация: macOS — CommonCrypto, Linux — OpenSSL \
(системный libcrypto), Windows — CNG/BCrypt. Выбор провайдера компилируется \
по target_os: одна и та же логика usecase'ов поверх паттерна Strategy."
)]
pub struct Cli {
    #[command(subcommand)]
    pub command: Command,
}

#[derive(Debug, Subcommand)]
pub enum Command {
    /// Сгенерировать симметричный ключ и сохранить в файл.
    GenKey {
        #[arg(long = "out")]
        output: PathBuf,
    },
    /// Зашифровать файл сохранённым ключом.
    Encrypt {
        #[arg(long)]
        key: PathBuf,
        #[arg(long = "in")]
        input: PathBuf,
        #[arg(long = "out")]
        output: PathBuf,
    },
    /// Расшифровать файл.
    Decrypt {
        #[arg(long)]
        key: PathBuf,
        #[arg(long = "in")]
        input: PathBuf,
        #[arg(long = "out")]
        output: PathBuf,
    },
}

/// # Errors
/// Любые ошибки IO или криптопровайдера.
pub fn run(cli: Cli) -> Result<()> {
    let provider = active();
    match cli.command {
        Command::GenKey { output } => {
            GenerateKeyUseCase::run(&provider, &output)?;
            println!(
                "✓ ключ сгенерирован провайдером «{}» → {}",
                provider.name(),
                output.display()
            );
        }
        Command::Encrypt { key, input, output } => {
            let n = EncryptUseCase::run(&provider, &key, &input, &output)?;
            println!(
                "✓ зашифровано: provider = «{}», {} байт plaintext → {} байт шифртекста",
                provider.name(),
                std::fs::metadata(&input).map(|m| m.len()).unwrap_or(0),
                n
            );
        }
        Command::Decrypt { key, input, output } => {
            let n = DecryptUseCase::run(&provider, &key, &input, &output)?;
            println!(
                "✓ расшифровано: provider = «{}», {n} байт plaintext → {}",
                provider.name(),
                output.display()
            );
        }
    }
    Ok(())
}
