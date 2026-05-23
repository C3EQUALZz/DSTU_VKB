//! CLI лаб 3.

use clap::{Parser, Subcommand};
use color_eyre::Result;

use crate::application::usecases::analyze;

#[derive(Parser, Debug)]
#[command(name = "lab_03_substitution", about = "Лаб 3 — простая замена", version)]
struct Cli {
    #[command(subcommand)]
    cmd: Cmd,
}

#[derive(Subcommand, Debug)]
enum Cmd {
    /// Провести частотный анализ шифртекста (числа, разделённые пробелами).
    Analyze {
        /// Шифртекст одной строкой.
        text: String,
    },
}

pub fn run() -> Result<()> {
    match Cli::parse().cmd {
        Cmd::Analyze { text } => {
            let r = analyze(&text)?;
            println!("Кодов в шифртексте: {}", r.cipher_codes.len());
            println!();
            println!("Частоты шифрообразований (по убыванию):");
            for (code, n) in r.frequencies.iter().take(20) {
                println!("  {code}: {n} раз");
            }
            println!();
            println!(
                "Начальная подстановка (частотно): {:?}",
                r.initial_substitution.map
            );
            println!();
            println!("Расшифровка по начальной подстановке:");
            println!("{}", r.initial_plain);
        }
    }
    Ok(())
}
