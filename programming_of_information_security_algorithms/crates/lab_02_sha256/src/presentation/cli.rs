//! CLI лаб 2.

use std::path::PathBuf;
use std::process::ExitCode;

use clap::{Parser, Subcommand};
use color_eyre::Result;

use crate::application::{HashFileUseCase, Verdict, VerifyHashUseCase};
use crate::domain::sha256::to_hex;

#[derive(Debug, Parser)]
#[command(
    name = "lab_02_sha256",
    version,
    about = "Лабораторная № 2: SHA-2-256 по FIPS 180-4 (без сторонних библиотек).",
    long_about = "\
Считает SHA-256 файла и проверяет файл против сохранённого хеша. \
Формат хеш-файла совместим с `shasum -a 256` (формат coreutils), поэтому \
проверить значение можно и сторонним инструментом."
)]
pub struct Cli {
    #[command(subcommand)]
    pub command: Command,
}

#[derive(Debug, Subcommand)]
pub enum Command {
    /// Посчитать SHA-256 файла. Если указан --out, записать его в shasum-формате.
    Hash {
        file: PathBuf,
        #[arg(long = "out")]
        output: Option<PathBuf>,
    },
    /// Сверить SHA-256 файла с заранее сохранённым.
    Verify {
        file: PathBuf,
        /// Файл, из которого читается ожидаемый хеш (формат shasum).
        #[arg(long = "against")]
        expected: PathBuf,
    },
}

/// Запускает CLI. Возвращает `ExitCode`, так как `verify` сигнализирует
/// о несоответствии не паникой, а ненулевым кодом возврата (1).
///
/// # Errors
/// Любые ошибки IO или формата файла-эталона.
pub fn run(cli: Cli) -> Result<ExitCode> {
    match cli.command {
        Command::Hash { file, output } => {
            let d = HashFileUseCase::run(&file, output.as_deref())?;
            println!("{hex}  {name}", hex = to_hex(&d), name = file.display());
            Ok(ExitCode::SUCCESS)
        }
        Command::Verify { file, expected } => {
            let (verdict, actual) = VerifyHashUseCase::run(&file, &expected)?;
            match verdict {
                Verdict::Match => {
                    println!(
                        "✓ OK  {name}: SHA-256 {hex}",
                        name = file.display(),
                        hex = to_hex(&actual)
                    );
                    Ok(ExitCode::SUCCESS)
                }
                Verdict::Mismatch => {
                    println!(
                        "✗ MISMATCH  {name}: actual = {hex}",
                        name = file.display(),
                        hex = to_hex(&actual)
                    );
                    Ok(ExitCode::from(1))
                }
            }
        }
    }
}
