//! Консольные команды; вывод результатов — явная функция калькулятора.

use clap::{Parser, Subcommand};
use color_eyre::Result;

use crate::application::{Calculator, Operation, PointInput};

#[derive(Debug, Clone, Copy, Parser)]
#[command(
    version,
    about = "Практика 2 — калькулятор на эллиптических кривых",
    after_help = "По умолчанию: y² = x³ + 2x + 2 mod 17.\nТочка: x,y или O. Пример: practice_02 add 5,1 6,3\nОтрицательные скаляры: mul -- -3 5,1. RUST_LOG=off отключает логи."
)]
pub struct Cli {
    /// Простой модуль поля > 3 (десятичная запись, u64).
    #[arg(id = "field_modulus", long = "p", global = true, default_value_t = 17)]
    pub p: u64,
    /// Коэффициент a (целое со знаком).
    #[arg(long, global = true, default_value_t = 2, allow_hyphen_values = true)]
    pub a: i128,
    /// Коэффициент b (целое со знаком).
    #[arg(long, global = true, default_value_t = 2, allow_hyphen_values = true)]
    pub b: i128,
    #[command(subcommand)]
    pub command: Command,
}

#[derive(Debug, Clone, Copy, Subcommand)]
pub enum Command {
    /// Проверить параметры и вывести дискриминант кривой.
    Info,
    /// Проверить принадлежность точки (непринадлежность — результат false).
    Check {
        #[arg(value_parser = parse_point, allow_hyphen_values = true)]
        point: PointInput,
    },
    /// Противоположная точка −P.
    Neg {
        #[arg(value_parser = parse_point, allow_hyphen_values = true)]
        point: PointInput,
    },
    /// Сложение P + Q.
    Add {
        #[arg(value_parser = parse_point, allow_hyphen_values = true)]
        p: PointInput,
        #[arg(value_parser = parse_point, allow_hyphen_values = true)]
        q: PointInput,
    },
    /// Вычитание P − Q.
    Sub {
        #[arg(value_parser = parse_point, allow_hyphen_values = true)]
        p: PointInput,
        #[arg(value_parser = parse_point, allow_hyphen_values = true)]
        q: PointInput,
    },
    /// Удвоение 2P.
    Double {
        #[arg(value_parser = parse_point, allow_hyphen_values = true)]
        point: PointInput,
    },
    /// Скалярное умножение kP; k — знаковое целое i128.
    Mul {
        #[arg(allow_negative_numbers = true)]
        k: i128,
        #[arg(value_parser = parse_point, allow_hyphen_values = true)]
        point: PointInput,
    },
    /// Линейная комбинация kP + mQ.
    Linear {
        #[arg(allow_negative_numbers = true)]
        k: i128,
        #[arg(value_parser = parse_point, allow_hyphen_values = true)]
        p: PointInput,
        #[arg(allow_negative_numbers = true)]
        m: i128,
        #[arg(value_parser = parse_point, allow_hyphen_values = true)]
        q: PointInput,
    },
    /// Перечислить все точки, включая O (p ≤ 10000).
    Points,
    /// Посчитать все точки, включая O (p ≤ 10000).
    Count,
    /// Порядок точки (≤ 100000 сложений).
    Order {
        #[arg(value_parser = parse_point, allow_hyphen_values = true)]
        point: PointInput,
    },
    /// Кратные точки — элементы её циклической подгруппы.
    Subgroup {
        #[arg(value_parser = parse_point, allow_hyphen_values = true)]
        point: PointInput,
    },
    /// Таблица сложения всей группы (≤ 32 точки).
    Table,
    /// Найти минимальное k ≥ 0 из Q = kP перебором (≤ 100000 сложений).
    Dlog {
        #[arg(value_parser = parse_point, allow_hyphen_values = true)]
        p: PointInput,
        #[arg(value_parser = parse_point, allow_hyphen_values = true)]
        q: PointInput,
    },
    /// Учебный ECDH: заданные a,b; общий результат — точка, без KDF.
    Ecdh {
        #[arg(value_parser = parse_point, allow_hyphen_values = true)]
        generator: PointInput,
        secret_a: u64,
        secret_b: u64,
    },
    /// Обратный элемент числа в поле.
    Inverse {
        #[arg(allow_negative_numbers = true)]
        value: i128,
    },
    /// Воспроизводимое демо на фиксированной кривой y²=x³+2x+2 mod 17.
    Demo,
}

fn parse_point(input: &str) -> Result<PointInput, String> {
    let input = input.trim();
    if input.eq_ignore_ascii_case("o") || input.eq_ignore_ascii_case("inf") {
        return Ok(PointInput::Infinity);
    }
    let (x, y) = input.split_once(',').ok_or("ожидается точка x,y или O")?;
    let x = x
        .trim()
        .parse::<i128>()
        .map_err(|_| "координата x должна помещаться в i128")?;
    let y = y
        .trim()
        .parse::<i128>()
        .map_err(|_| "координата y должна помещаться в i128")?;
    Ok(PointInput::Affine(x, y))
}

pub fn run(cli: Cli) -> Result<()> {
    if matches!(cli.command, Command::Demo) {
        return demo();
    }
    let service = Calculator::new(cli.p, cli.a, cli.b)?;
    let operation = to_operation(cli.command);
    println!("{}", service.description());
    for line in service.execute(operation)? {
        println!("{line}");
    }
    Ok(())
}

fn to_operation(command: Command) -> Operation {
    match command {
        Command::Info | Command::Demo => Operation::Info,
        Command::Check { point } => Operation::Check(point),
        Command::Neg { point } => Operation::Neg(point),
        Command::Add { p, q } => Operation::Add(p, q),
        Command::Sub { p, q } => Operation::Sub(p, q),
        Command::Double { point } => Operation::Double(point),
        Command::Mul { k, point } => Operation::Mul(k, point),
        Command::Linear { k, p, m, q } => Operation::Linear(k, p, m, q),
        Command::Points => Operation::Points,
        Command::Count => Operation::Count,
        Command::Order { point } => Operation::Order(point),
        Command::Subgroup { point } => Operation::Subgroup(point),
        Command::Table => Operation::Table,
        Command::Dlog { p, q } => Operation::Dlog(p, q),
        Command::Ecdh {
            generator,
            secret_a,
            secret_b,
        } => Operation::Ecdh(generator, secret_a, secret_b),
        Command::Inverse { value } => Operation::Inverse(value),
    }
}

fn demo() -> Result<()> {
    let service = Calculator::new(17, 2, 2)?;
    let p = PointInput::Affine(5, 1);
    let q = PointInput::Affine(6, 3);
    println!("Демонстрационная кривая: {}", service.description());
    for operation in [
        Operation::Info,
        Operation::Check(p),
        Operation::Check(PointInput::Affine(1, 1)),
        Operation::Neg(p),
        Operation::Add(p, q),
        Operation::Sub(p, q),
        Operation::Double(p),
        Operation::Mul(7, p),
        Operation::Mul(-3, p),
        Operation::Mul(0, p),
        Operation::Linear(2, p, 3, q),
        Operation::Add(p, PointInput::Affine(5, 16)),
        Operation::Count,
        Operation::Order(p),
        Operation::Dlog(p, PointInput::Affine(0, 6)),
        Operation::Inverse(2),
        Operation::Ecdh(p, 5, 7),
    ] {
        for line in service.execute(operation)? {
            println!("{line}");
        }
    }
    Ok(())
}
