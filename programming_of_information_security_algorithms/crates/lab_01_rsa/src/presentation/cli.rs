//! CLI для лаб 1.

use std::io::Write;
use std::path::PathBuf;

use clap::{Parser, Subcommand};
use color_eyre::Result;
use tracing::info;

use crate::application::{DecryptUseCase, EncryptUseCase, GenerateKeysUseCase};
use crate::domain::rng::OsRng;

#[derive(Debug, Parser)]
#[command(
    name = "lab_01_rsa",
    version,
    about = "Лабораторная № 1: учебная реализация RSA (генерация ключей, шифрование, расшифрование) без сторонних крипто-библиотек.",
    long_about = "\
Алгоритм RSA реализован с нуля: длинная арифметика, Miller-Rabin, расширенный \
Евклид. CLI поддерживает три сценария — gen, encrypt, decrypt — каждый \
работает с файлами на диске."
)]
pub struct Cli {
    #[command(subcommand)]
    pub command: Command,
}

#[derive(Debug, Subcommand)]
pub enum Command {
    /// Сгенерировать пару ключей и записать в файлы.
    Gen {
        /// Длина модуля `n` в битах. Должна быть чётной, рекомендуется ≥ 512.
        #[arg(long, default_value_t = 1024)]
        bits: usize,
        /// Куда сохранить открытый ключ.
        #[arg(long)]
        public: PathBuf,
        /// Куда сохранить закрытый ключ.
        #[arg(long)]
        private: PathBuf,
    },
    /// Зашифровать файл открытым ключом.
    Encrypt {
        #[arg(long)]
        public: PathBuf,
        /// Исходный файл (любой — текст/бинарь).
        #[arg(long = "in")]
        input: PathBuf,
        /// Куда положить шифртекст.
        #[arg(long = "out")]
        output: PathBuf,
    },
    /// Расшифровать файл закрытым ключом и вывести результат.
    Decrypt {
        #[arg(long)]
        private: PathBuf,
        /// Шифртекст.
        #[arg(long = "in")]
        input: PathBuf,
        /// (опц.) Куда дополнительно записать восстановленный plaintext.
        #[arg(long = "out")]
        output: Option<PathBuf>,
    },
}

/// Запускает CLI с уже разобранными аргументами.
///
/// # Errors
/// Любые ошибки чтения/записи файлов или вычислений RSA.
pub fn run(cli: Cli) -> Result<()> {
    match cli.command {
        Command::Gen {
            bits,
            public,
            private,
        } => {
            let mut rng = OsRng::new()?;
            let kp = GenerateKeysUseCase { rng: &mut rng }.run(bits, &public, &private)?;
            println!(
                "✓ ключи сгенерированы: n = {} бит, e = {}, открытый ключ — {public:?}, закрытый — {private:?}",
                kp.public.n.bit_length(),
                kp.public.e
            );
        }
        Command::Encrypt {
            public,
            input,
            output,
        } => {
            let (key, ct) = EncryptUseCase::run(&public, &input, &output)?;
            println!(
                "✓ зашифровано: {} байт plaintext → {} байт шифртекста (n = {} бит)",
                std::fs::metadata(&input).map(|m| m.len()).unwrap_or(0),
                ct.len(),
                key.bits
            );
            info!("ciphertext written");
        }
        Command::Decrypt {
            private,
            input,
            output,
        } => {
            let (_, plaintext) = DecryptUseCase::run(&private, &input, output.as_deref())?;
            // Условие требует «вывести расшифрованное сообщение на экран».
            // Пишем как байты, чтобы корректно работало для бинарных сообщений.
            std::io::stdout()
                .lock()
                .write_all(&plaintext)
                .map_err(color_eyre::eyre::Report::from)?;
            // Завершающий перевод строки для удобства терминала.
            println!();
        }
    }
    Ok(())
}
