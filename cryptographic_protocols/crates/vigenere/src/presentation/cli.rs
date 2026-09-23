//! CLI трёх схем Виженера и их статистического криптоанализа.

use clap::{Parser, Subcommand, ValueEnum};
use color_eyre::Result;

use crate::application::{autokey, progressive, standard};
use crate::domain::attack::AttackResult;
use crate::domain::scheme::{Alphabet, Operation, Scheme};
use crate::infrastructure::Console;

#[derive(Clone, Copy, Debug, ValueEnum)]
enum AlphabetOption {
    En,
    RuYo,
    RuNoYo,
}

impl From<AlphabetOption> for Alphabet {
    fn from(value: AlphabetOption) -> Self {
        match value {
            AlphabetOption::En => Self::Latin,
            AlphabetOption::RuYo => Self::RussianWithYo,
            AlphabetOption::RuNoYo => Self::RussianNoYo,
        }
    }
}

#[derive(Clone, Copy, Debug, ValueEnum)]
enum SchemeOption {
    Standard,
    Progressive,
    Autokey,
}

impl From<SchemeOption> for Scheme {
    fn from(value: SchemeOption) -> Self {
        match value {
            SchemeOption::Standard => Self::Standard,
            SchemeOption::Progressive => Self::Progressive,
            SchemeOption::Autokey => Self::Autokey,
        }
    }
}

#[derive(Parser, Debug)]
#[command(
    name = "vigenere",
    about = "Три схемы Виженера и их криптоанализ",
    version
)]
struct Cli {
    #[command(subcommand)]
    command: Command,
}

#[derive(Subcommand, Debug)]
enum Command {
    Encrypt {
        #[arg(long, value_enum)]
        scheme: SchemeOption,
        #[arg(long, value_enum)]
        alphabet: AlphabetOption,
        #[arg(long)]
        key: String,
        #[arg(long, allow_hyphen_values = true)]
        text: String,
    },
    Decrypt {
        #[arg(long, value_enum)]
        scheme: SchemeOption,
        #[arg(long, value_enum)]
        alphabet: AlphabetOption,
        #[arg(long)]
        key: String,
        #[arg(long, allow_hyphen_values = true)]
        text: String,
    },
    /// Найти наиболее вероятные ключ и открытый текст.
    Break {
        text: String,
        #[arg(long, value_enum)]
        scheme: SchemeOption,
        #[arg(long, value_enum)]
        alphabet: AlphabetOption,
        #[arg(long, default_value_t = 2)]
        min_key: usize,
        #[arg(long, default_value_t = 10)]
        max_key: usize,
    },
}

fn execute(
    scheme: Scheme,
    alphabet: Alphabet,
    key: &str,
    text: &str,
    operation: Operation,
) -> Result<()> {
    let output = &mut Console;
    match scheme {
        Scheme::Standard => standard::execute(alphabet, key, text, operation, output)?,
        Scheme::Progressive => progressive::execute(alphabet, key, text, operation, output)?,
        Scheme::Autokey => autokey::execute(alphabet, key, text, operation, output)?,
    }
    Ok(())
}

fn analyze(
    scheme: Scheme,
    alphabet: Alphabet,
    text: &str,
    min_key: usize,
    max_key: usize,
) -> Result<AttackResult> {
    Ok(match scheme {
        Scheme::Standard => standard::analyze(alphabet, text, min_key..=max_key)?,
        Scheme::Progressive => progressive::analyze(alphabet, text, min_key..=max_key)?,
        Scheme::Autokey => autokey::analyze(alphabet, text, min_key..=max_key)?,
    })
}

pub fn run() -> Result<()> {
    match Cli::parse().command {
        Command::Encrypt {
            scheme,
            alphabet,
            key,
            text,
        } => {
            execute(
                scheme.into(),
                alphabet.into(),
                &key,
                &text,
                Operation::Encrypt,
            )?;
        }
        Command::Decrypt {
            scheme,
            alphabet,
            key,
            text,
        } => {
            execute(
                scheme.into(),
                alphabet.into(),
                &key,
                &text,
                Operation::Decrypt,
            )?;
        }
        Command::Break {
            text,
            scheme,
            alphabet,
            min_key,
            max_key,
        } => {
            let result = analyze(scheme.into(), alphabet.into(), &text, min_key, max_key)?;
            println!("Длина ключа: {}", result.key_length);
            println!("Восстановленный ключ: {}", result.key);
            println!("Оценка: {:.5}", result.score);
            println!("Расшифрованный текст: {}", result.plain);
        }
    }
    Ok(())
}
