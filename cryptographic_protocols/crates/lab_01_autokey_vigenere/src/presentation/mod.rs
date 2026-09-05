use crate::{
    application,
    domain::{Alphabet, Operation},
    infrastructure::Console,
};
use clap::{Parser, ValueEnum};

#[derive(Clone, Copy, ValueEnum)]
enum Language {
    En,
    Ru,
}

#[derive(Clone, Copy, ValueEnum)]
enum Action {
    Encrypt,
    Decrypt,
}

#[derive(Parser)]
#[command(about = "Виженер с самогенерирующимся ключом (лабораторная №1, 2026)")]
struct Args {
    #[arg(value_enum)]
    action: Action,
    #[arg(long, value_enum)]
    alphabet: Language,
    #[arg(long)]
    key: String,
    #[arg(long, allow_hyphen_values = true)]
    text: String,
}

pub fn run() -> color_eyre::Result<()> {
    let args = Args::parse();
    let alphabet = match args.alphabet {
        Language::En => Alphabet::Latin,
        Language::Ru => Alphabet::Russian,
    };
    let operation = match args.action {
        Action::Encrypt => Operation::Encrypt,
        Action::Decrypt => Operation::Decrypt,
    };
    application::execute(alphabet, &args.key, &args.text, operation, &mut Console)
}
