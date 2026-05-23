//! CLI практики 1.

use clap::{Parser, Subcommand};
use color_eyre::Result;
use color_eyre::eyre::WrapErr;
use tracing::info;

use crate::application::{Operation, VerifyService};

#[derive(Debug, Parser)]
#[command(
    name = "practice_01",
    version,
    about = "Практика 1 — длинная арифметика (сложение и вычитание чисел ≥ 64 разрядов).",
    long_about = "\
Складывает и вычитает целые числа произвольной длины. При операндах, \
помещающихся в `i128`, дополнительно прогоняет вычисление через встроенную \
арифметику и сверяет результаты — это и есть «проверка обычного сложения и \
вычитания», которую требует условие практики."
)]
pub struct Cli {
    #[command(subcommand)]
    pub command: Command,
}

#[derive(Debug, Subcommand)]
pub enum Command {
    /// Сложить два числа `A + B`.
    Add { a: String, b: String },
    /// Вычесть второе число из первого `A - B`.
    Sub { a: String, b: String },
    /// Запустить демо: пара малых чисел (с проверкой по i128) + пара длинных.
    Demo,
}

/// Запускает CLI с уже разобранными аргументами.
///
/// # Errors
/// Любая ошибка парсинга операнда или печати результата.
pub fn run(cli: Cli) -> Result<()> {
    let service = VerifyService::new();
    match cli.command {
        Command::Add { a, b } => report(&service, Operation::Add, &a, &b)?,
        Command::Sub { a, b } => report(&service, Operation::Sub, &a, &b)?,
        Command::Demo => run_demo(&service)?,
    }
    Ok(())
}

fn report(service: &VerifyService, op: Operation, a: &str, b: &str) -> Result<()> {
    let r = service
        .run(op, a, b)
        .wrap_err_with(|| format!("операция {} {} {}", a, op.symbol(), b))?;
    println!("{r}");
    Ok(())
}

fn run_demo(service: &VerifyService) -> Result<()> {
    info!("demo: малые числа (i128-проверка должна сработать)");
    report(service, Operation::Add, "12345", "67890")?;
    report(service, Operation::Sub, "100", "200")?;

    info!("demo: длинные числа (≥ 64 десятичных цифр, i128-проверка невозможна)");
    let a = "123456789012345678901234567890123456789012345678901234567890123456789012345678";
    let b = "98765432109876543210987654321098765432109876543210987654321098765432109876543";
    report(service, Operation::Add, a, b)?;
    report(service, Operation::Sub, a, b)?;

    info!("demo: смешанные знаки и переход через ноль");
    report(service, Operation::Add, "-100", "30")?;
    report(
        service,
        Operation::Sub,
        "10",
        "10000000000000000000000000000000000000000000000",
    )?;
    Ok(())
}
