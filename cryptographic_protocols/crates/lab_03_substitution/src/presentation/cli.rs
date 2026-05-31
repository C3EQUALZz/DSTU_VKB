//! CLI лаб 3.

use clap::{Parser, Subcommand};
use color_eyre::Result;

use crate::application::usecases::{analyze, solve_cipher};

#[derive(Parser, Debug)]
#[command(
    name = "lab_03_substitution",
    about = "Лаб 3 — шифр простой замены",
    version
)]
struct Cli {
    #[command(subcommand)]
    cmd: Cmd,
}

#[derive(Subcommand, Debug)]
enum Cmd {
    /// Частотный анализ (начальная подстановка по таблице частот).
    Analyze { text: String },
    /// Автоматический взлом методом имитации отжига по биграммной модели.
    Solve {
        text: String,
        /// Число рестартов отжига.
        #[arg(long, default_value_t = 8)]
        rounds: usize,
        /// Итераций на рестарт.
        #[arg(long, default_value_t = 30000)]
        iters: usize,
    },
}

pub fn run() -> Result<()> {
    match Cli::parse().cmd {
        Cmd::Analyze { text } => {
            let r = analyze(&text)?;
            println!("Кодов: {}", r.cipher_codes.len());
            println!("Частоты (топ-20):");
            for (code, n) in r.frequencies.iter().take(20) {
                println!("  {code:>3}: {n}");
            }
            println!("\nРасшифровка (начальная):\n{}", r.initial_plain);
        }
        Cmd::Solve {
            text,
            rounds,
            iters,
        } => {
            let r = solve_cipher(&text, rounds, iters)?;
            println!("Расшифрованный текст:\n{}", r.plain);
            println!("\nТаблица подстановки (код → буква):");
            for (c, ch) in &r.key_map {
                println!("  {c:>3} → {ch}");
            }
            println!("\nПриспособленность: {:.1}", r.fitness);
        }
    }
    Ok(())
}
