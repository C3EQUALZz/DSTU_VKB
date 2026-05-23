//! CLI лаб 2: запуск упражнений 2 и 3 для конкретного варианта.

use clap::{Parser, Subcommand};
use color_eyre::Result;
use color_eyre::eyre::eyre;

use crate::application::usecases::{
    BlakleyExerciseReport, ShamirExerciseReport, blakley_exercise3, shamir_exercise2,
};
use crate::presentation::variants::{blakley_variants, shamir_variants};

#[derive(Parser, Debug)]
#[command(
    name = "lab_02_secret_sharing",
    about = "Лаб 2 — Шамир и Блэкли",
    version
)]
struct Cli {
    #[command(subcommand)]
    cmd: Cmd,
}

#[derive(Subcommand, Debug)]
enum Cmd {
    /// Решить упражнение 2 (Шамир) для конкретного варианта.
    Shamir {
        #[arg(long)]
        variant: usize,
        /// x-координата генерируемой доли Дейва.
        #[arg(long, default_value_t = 2)]
        dave_x: i64,
    },
    /// Решить упражнение 3 (Блэкли) для конкретного варианта.
    Blakley {
        #[arg(long)]
        variant: usize,
    },
    /// Запустить все 28 вариантов обеих задач и распечатать секреты.
    All,
}

pub fn run() -> Result<()> {
    match Cli::parse().cmd {
        Cmd::Shamir { variant, dave_x } => {
            let variants = shamir_variants();
            let v = variants
                .get(
                    variant
                        .checked_sub(1)
                        .ok_or_else(|| eyre!("variant >= 1"))?,
                )
                .ok_or_else(|| eyre!("вариант {variant} вне диапазона 1..=28"))?;
            let left = shamir_exercise2(&v.left.shares, v.left.p, dave_x)?;
            let right = shamir_exercise2(&v.right.shares, v.right.p, dave_x)?;
            print_shamir(variant, "m=4, p=23", &left);
            print_shamir(variant, "m=3, p=31", &right);
        }
        Cmd::Blakley { variant } => {
            let variants = blakley_variants();
            let v = variants
                .get(
                    variant
                        .checked_sub(1)
                        .ok_or_else(|| eyre!("variant >= 1"))?,
                )
                .ok_or_else(|| eyre!("вариант {variant} вне диапазона 1..=28"))?;
            let left = blakley_exercise3(v.left_q, v.left_p, v.left_pairs)?;
            let right = blakley_exercise3(v.right_q, v.right_p, v.right_pairs)?;
            print_blakley(variant, "p=17", &left);
            print_blakley(variant, "p=31", &right);
        }
        Cmd::All => {
            for (i, v) in shamir_variants().iter().enumerate() {
                let l = shamir_exercise2(&v.left.shares, v.left.p, 2)?;
                let r = shamir_exercise2(&v.right.shares, v.right.p, 2)?;
                println!(
                    "Вар {:>2}: Шамир (p=23) секрет={}, полином={:?}; Шамир (p=31) секрет={}, полином={:?}",
                    i + 1,
                    l.secret,
                    l.polynomial.coeffs,
                    r.secret,
                    r.polynomial.coeffs
                );
            }
            for (i, v) in blakley_variants().iter().enumerate() {
                let l = blakley_exercise3(v.left_q, v.left_p, v.left_pairs)?;
                let r = blakley_exercise3(v.right_q, v.right_p, v.right_pairs)?;
                println!(
                    "Вар {:>2}: Блэкли (p=17) Q={:?} → восст={:?}; Блэкли (p=31) Q={:?} → восст={:?}",
                    i + 1,
                    l.q,
                    l.recovered_q,
                    r.q,
                    r.recovered_q
                );
            }
        }
    }
    Ok(())
}

fn print_shamir(variant: usize, label: &str, r: &ShamirExerciseReport) {
    println!("=== Вариант {variant}: Шамир, {label} ===");
    println!("Секрет: f(0) = {}", r.secret);
    println!(
        "Восстановленный полином (коэф. от a0 до a_{{m-1}}): {:?}",
        r.polynomial.coeffs
    );
    println!("Доля Дейва: (x={}, y={})", r.dave_share.x, r.dave_share.y);
}

fn print_blakley(variant: usize, label: &str, r: &BlakleyExerciseReport) {
    println!("=== Вариант {variant}: Блэкли, {label} ===");
    println!("Секретная точка Q: ({}, {}, {})", r.q.x0, r.q.y0, r.q.z0);
    for (i, s) in r.shares.iter().enumerate() {
        let name = ["A", "B", "D", "C"][i];
        println!(
            "  Доля {name}: a={}, b={}, c={} → плоскость z = {}x + {}y + {}",
            s.a, s.b, s.c, s.a, s.b, s.c
        );
    }
    println!(
        "Восстановленная Q по {{A, B, D}}: ({}, {}, {})",
        r.recovered_q.x0, r.recovered_q.y0, r.recovered_q.z0
    );
}
