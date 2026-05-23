//! CLI лаб 7.

use std::path::PathBuf;

use clap::{Parser, Subcommand};
use color_eyre::Result;

use crate::application::{DecryptUseCase, EncryptUseCase, GenerateKeysUseCase};
use crate::domain::cipher::AsymmetricCryptoProvider;
use crate::infrastructure::providers::active;

#[derive(Debug, Parser)]
#[command(
    name = "lab_07_asym",
    version,
    about = "Лаб 7 — асимметричное RSA-OAEP-2048 (SHA-256) через системный криптопровайдер ОС.",
    long_about = "\
Cross-platform: macOS — Security framework (SecKey), Linux — OpenSSL \
(системный libcrypto), Windows — CNG/NCrypt (каркас). Strategy pattern: \
один и тот же код use case'ов поверх trait'а AsymmetricCryptoProvider."
)]
pub struct Cli {
    #[command(subcommand)]
    pub command: Command,
}

#[derive(Debug, Subcommand)]
pub enum Command {
    /// Сгенерировать пару RSA-ключей.
    GenKeys {
        #[arg(long, default_value_t = 2048)]
        bits: usize,
        #[arg(long)]
        public: PathBuf,
        #[arg(long)]
        private: PathBuf,
    },
    /// Зашифровать файл открытым ключом (RSA-OAEP-SHA256, один блок).
    Encrypt {
        #[arg(long)]
        public: PathBuf,
        #[arg(long = "in")]
        input: PathBuf,
        #[arg(long = "out")]
        output: PathBuf,
    },
    /// Расшифровать файл закрытым ключом.
    Decrypt {
        #[arg(long)]
        private: PathBuf,
        #[arg(long = "in")]
        input: PathBuf,
        #[arg(long = "out")]
        output: PathBuf,
    },
}

/// # Errors
/// Любая ошибка IO или провайдера.
pub fn run(cli: Cli) -> Result<()> {
    let provider = active();
    match cli.command {
        Command::GenKeys {
            bits,
            public,
            private,
        } => {
            GenerateKeysUseCase::run(&provider, bits, &public, &private)?;
            println!(
                "✓ ключи RSA-{bits} сгенерированы провайдером «{}» → {} / {}",
                provider.name(),
                public.display(),
                private.display()
            );
        }
        Command::Encrypt {
            public,
            input,
            output,
        } => {
            let n = EncryptUseCase::run(&provider, &public, &input, &output)?;
            println!(
                "✓ зашифровано: provider = «{}», {} байт plaintext → {n} байт шифртекста",
                provider.name(),
                std::fs::metadata(&input).map(|m| m.len()).unwrap_or(0)
            );
        }
        Command::Decrypt {
            private,
            input,
            output,
        } => {
            let n = DecryptUseCase::run(&provider, &private, &input, &output)?;
            println!(
                "✓ расшифровано: provider = «{}», {n} байт plaintext → {}",
                provider.name(),
                output.display()
            );
        }
    }
    Ok(())
}
