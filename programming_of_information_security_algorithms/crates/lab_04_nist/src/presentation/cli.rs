//! CLI лаб 4.

use std::path::PathBuf;
use std::process::ExitCode;

use clap::{Parser, Subcommand, ValueEnum};
use color_eyre::Result;

use crate::application::usecases::{AnalyseUseCase, Suite};
use crate::infrastructure::loader::Format;

#[derive(Debug, Parser)]
#[command(
    name = "lab_04_nist",
    version,
    about = "Лабораторная № 4: собственная реализация одного из тестов NIST SP 800-22.",
    long_about = "\
Реализован основной тест по условию — Monobit Frequency Test (§2.1). \
Бонусом — Runs Test (§2.3). erfc считается по аппроксимации \
Abramowitz-Stegun 7.1.26, без libm.

Входной файл — последовательность из lab_03_prng (бинарная или ASCII)."
)]
pub struct Cli {
    #[command(subcommand)]
    pub command: Command,
}

#[derive(Debug, Clone, Copy, ValueEnum)]
pub enum FormatArg {
    Auto,
    Ascii,
    Binary,
}

#[derive(Debug, Clone, Copy, ValueEnum)]
pub enum SuiteArg {
    /// Только Monobit Frequency.
    Monobit,
    /// Monobit + Runs.
    All,
}

#[derive(Debug, Subcommand)]
pub enum Command {
    /// Прогнать тесты на файле.
    Check {
        /// Входной файл — последовательность из lab_03_prng.
        #[arg(long = "input")]
        input: PathBuf,
        /// Формат входа. `auto` (по умолчанию) определяет по расширению.
        #[arg(long, value_enum, default_value_t = FormatArg::Auto)]
        format: FormatArg,
        /// Какие тесты запускать.
        #[arg(long, value_enum, default_value_t = SuiteArg::All)]
        suite: SuiteArg,
        /// Куда сохранить отчёт.
        #[arg(long = "out")]
        output: Option<PathBuf>,
    },
}

/// # Errors
/// Любые ошибки IO.
pub fn run(cli: Cli) -> Result<ExitCode> {
    match cli.command {
        Command::Check {
            input,
            format,
            suite,
            output,
        } => {
            let fmt = match format {
                FormatArg::Auto => None,
                FormatArg::Ascii => Some(Format::Ascii),
                FormatArg::Binary => Some(Format::Binary),
            };
            let suite = match suite {
                SuiteArg::Monobit => Suite::Monobit,
                SuiteArg::All => Suite::MonobitAndRuns,
            };
            let (results, report) = AnalyseUseCase::run(&input, fmt, suite, output.as_deref())?;
            print!("{report}");
            let all_pass = results.iter().all(crate::domain::NistTestResult::passed);
            Ok(if all_pass {
                ExitCode::SUCCESS
            } else {
                ExitCode::from(1)
            })
        }
    }
}
