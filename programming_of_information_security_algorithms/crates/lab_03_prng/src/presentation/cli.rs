//! CLI лаб 3.

use std::path::PathBuf;

use clap::{Parser, Subcommand};
use color_eyre::Result;
use color_eyre::eyre::eyre;

use crate::application::GenerateSequenceUseCase;

#[derive(Debug, Parser)]
#[command(
    name = "lab_03_prng",
    version,
    about = "Лабораторная № 3: генерация ПДСЧ (xorshift64*) с записью в файлы для NIST STS.",
    long_about = "\
Алгоритм — xorshift64* Marsaglia. По условию записываются ≥ 200 64-битных \
значений (12 800 бит — стандартный размер блока для большинства NIST-тестов). \
Сразу пишутся два варианта: бинарный (для STS-режима «1 — Binary») \
и ASCII (для «0 — ASCII»). Один и тот же seed даёт одну и ту же \
последовательность — это важно для воспроизводимости в лаб 4."
)]
pub struct Cli {
    #[command(subcommand)]
    pub command: Command,
}

#[derive(Debug, Subcommand)]
pub enum Command {
    /// Сгенерировать последовательность и записать в файлы.
    Gen {
        /// Сколько 64-битных значений сгенерировать. Не меньше 200 (условие лаб 3).
        #[arg(long, default_value_t = 200)]
        count: usize,
        /// Seed как hex (с префиксом `0x`) или dec.
        #[arg(long, default_value = "0xDEADBEEFCAFEBABE")]
        seed: String,
        /// Путь для бинарного представления (по 8 байт big-endian на значение).
        #[arg(long = "out-bin")]
        out_binary: Option<PathBuf>,
        /// Путь для ASCII-битового представления (символы '0'/'1', одна строка).
        #[arg(long = "out-ascii")]
        out_ascii: Option<PathBuf>,
    },
}

fn parse_seed(s: &str) -> Result<u64> {
    let s = s.trim().replace('_', "");
    if let Some(hex) = s.strip_prefix("0x").or_else(|| s.strip_prefix("0X")) {
        u64::from_str_radix(hex, 16).map_err(|e| eyre!("seed (hex) не разобран: {e}"))
    } else {
        s.parse::<u64>()
            .map_err(|e| eyre!("seed (dec) не разобран: {e}"))
    }
}

/// # Errors
/// Ошибки парсинга аргументов или записи файлов.
pub fn run(cli: Cli) -> Result<()> {
    match cli.command {
        Command::Gen {
            count,
            seed,
            out_binary,
            out_ascii,
        } => {
            let seed_u64 = parse_seed(&seed)?;
            let seq = GenerateSequenceUseCase::run(
                seed_u64,
                count,
                out_binary.as_deref(),
                out_ascii.as_deref(),
            )?;
            println!(
                "✓ сгенерировано {n} 64-битных значений ({bits} бит), seed = 0x{seed_u64:016X}",
                n = seq.word_count(),
                bits = seq.bit_count()
            );
            if let Some(p) = out_binary {
                println!("  binary → {}", p.display());
            }
            if let Some(p) = out_ascii {
                println!("  ascii  → {}", p.display());
            }
            Ok(())
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_seed_accepts_hex_and_dec() {
        assert_eq!(parse_seed("0xCAFEBABE").unwrap(), 0xCAFE_BABE);
        assert_eq!(parse_seed("0XCAFEBABE").unwrap(), 0xCAFE_BABE);
        assert_eq!(parse_seed("42").unwrap(), 42);
        assert_eq!(parse_seed("1_000").unwrap(), 1000);
    }

    #[test]
    fn parse_seed_rejects_bad_input() {
        assert!(parse_seed("0xZZ").is_err());
        assert!(parse_seed("abc").is_err());
    }
}
