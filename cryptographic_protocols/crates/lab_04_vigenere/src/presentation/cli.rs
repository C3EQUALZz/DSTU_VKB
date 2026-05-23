//! CLI лаб 4.

use clap::{Parser, Subcommand};
use color_eyre::Result;

use crate::application::usecases::{run_cryptanalysis, run_decrypt, run_encrypt};

#[derive(Parser, Debug)]
#[command(name = "lab_04_vigenere", about = "Лаб 4 — шифр Виженера", version)]
struct Cli {
    #[command(subcommand)]
    cmd: Cmd,
}

#[derive(Subcommand, Debug)]
enum Cmd {
    Encrypt {
        text: String,
        #[arg(long)]
        key: String,
    },
    Decrypt {
        text: String,
        #[arg(long)]
        key: String,
    },
    /// Криптоанализ: восстановить ключ и расшифровать.
    Break {
        cipher: String,
        #[arg(long, default_value_t = 2)]
        min_key: usize,
        #[arg(long, default_value_t = 10)]
        max_key: usize,
    },
}

pub fn run() -> Result<()> {
    match Cli::parse().cmd {
        Cmd::Encrypt { text, key } => {
            let r = run_encrypt(&text, &key)?;
            println!("Открытый текст: {}", r.plain);
            println!("Ключ: {}", r.key);
            println!("Шифртекст: {}", r.cipher);
        }
        Cmd::Decrypt { text, key } => {
            let r = run_decrypt(&text, &key)?;
            println!("Шифртекст: {}", r.cipher);
            println!("Ключ: {}", r.key);
            println!("Открытый текст: {}", r.plain);
        }
        Cmd::Break {
            cipher,
            min_key,
            max_key,
        } => {
            let r = run_cryptanalysis(&cipher, min_key..=max_key)?;
            println!(
                "Шифртекст ({} симв.): {}",
                r.cipher.chars().count(),
                r.cipher
            );
            println!();
            println!("Индексы совпадения по длинам ключа:");
            for (l, ic) in &r.key_length_scores {
                println!("  L = {l}: IC = {ic:.5}");
            }
            println!();
            println!("Восстановленный ключ: «{}»", r.recovered_key);
            println!("Расшифрованный текст: {}", r.recovered_plain);
        }
    }
    Ok(())
}
