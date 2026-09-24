//! CLI запускает варианты таблицы 5.1 или пользовательский набор долей.

use std::path::PathBuf;

use clap::{Parser, ValueEnum};
use color_eyre::Result;

use crate::application::usecases::{RecoveryReport, Scheme, recover, recover_both};
use crate::infrastructure::variants::{load_builtin, load_file};

#[derive(Parser, Debug)]
#[command(
    name = "shamir_blakley",
    about = "Шамир и Блэкли: варианты 1–20",
    version
)]
struct Cli {
    /// Номер варианта таблицы 5.1 (по умолчанию 11).
    #[arg(long, conflicts_with = "input")]
    variant: Option<usize>,
    /// JSON-файл с произвольными долями того же формата.
    #[arg(long)]
    input: Option<PathBuf>,
    #[arg(long, value_enum, default_value_t = Method::All)]
    method: Method,
    #[arg(long, value_enum, default_value_t = Shares::Both)]
    shares: Shares,
}

#[derive(Clone, Copy, Debug, ValueEnum)]
enum Method {
    Shamir,
    Blakley,
    All,
}

#[derive(Clone, Copy, Debug, ValueEnum)]
enum Shares {
    #[value(name = "3")]
    Three,
    #[value(name = "5")]
    Five,
    Both,
}

pub fn run() -> Result<()> {
    let cli = Cli::parse();
    let input = if let Some(path) = cli.input.as_deref() {
        load_file(path)?
    } else {
        load_builtin(cli.variant.unwrap_or(11))?
    };
    let label = input.number.map_or_else(
        || "Пользовательские данные".to_owned(),
        |number| format!("Вариант {number}"),
    );
    let counts: &[usize] = match cli.shares {
        Shares::Three => &[3],
        Shares::Five => &[5],
        Shares::Both => &[3, 5],
    };
    for &count in counts {
        match cli.method {
            Method::Shamir => print_report(&label, &recover(&input, Scheme::Shamir, count)?),
            Method::Blakley => print_report(&label, &recover(&input, Scheme::Blakley, count)?),
            Method::All => {
                for report in recover_both(&input, count)? {
                    print_report(&label, &report);
                }
            }
        }
    }
    Ok(())
}

fn print_report(label: &str, report: &RecoveryReport) {
    let count_word = if report.share_count == 3 {
        "доли"
    } else {
        "долей"
    };
    println!(
        "=== {}: {}, {} {} ===",
        label,
        report.scheme.name(),
        report.share_count,
        count_word
    );
    for symbol in &report.symbols {
        let detail = match report.scheme {
            Scheme::Shamir => format!(
                "f(x) = {} + {}x + {}x²",
                symbol.solution[0], symbol.solution[1], symbol.solution[2]
            ),
            Scheme::Blakley => format!(
                "точка = ({}, {}, {})",
                symbol.solution[0], symbol.solution[1], symbol.solution[2]
            ),
        };
        println!(
            "X{}: код {} → {}; {detail}",
            symbol.index, symbol.code, symbol.letter
        );
    }
    println!("Восстановленное слово: {}", report.word);
}
