//! CLI лаб 6.

use clap::{Parser, Subcommand};
use color_eyre::Result;
use color_eyre::eyre::eyre;

use crate::application::usecases::{WordReport, process_word};
use crate::presentation::variants::VARIANTS;

#[derive(Parser, Debug)]
#[command(
    name = "lab_06_crt_sharing",
    about = "Лаб 6 — Миньотта + Асмут-Блум",
    version
)]
struct Cli {
    #[command(subcommand)]
    cmd: Cmd,
}

#[derive(Subcommand, Debug)]
enum Cmd {
    /// Запустить упражнение для одного варианта.
    Variant {
        #[arg(long)]
        variant: usize,
        #[arg(long, default_value_t = 3)]
        k: usize,
        #[arg(long, default_value_t = 5)]
        n: usize,
        /// Случайный множитель r для Асмут-Блума.
        #[arg(long, default_value_t = 7)]
        r: u64,
    },
    /// Прогнать все 20 вариантов.
    All {
        #[arg(long, default_value_t = 3)]
        k: usize,
        #[arg(long, default_value_t = 5)]
        n: usize,
        #[arg(long, default_value_t = 7)]
        r: u64,
    },
}

pub fn run() -> Result<()> {
    match Cli::parse().cmd {
        Cmd::Variant { variant, k, n, r } => {
            if k > n {
                return Err(eyre!("k > n"));
            }
            let word = VARIANTS
                .get(variant.checked_sub(1).ok_or_else(|| eyre!("variant ≥ 1"))?)
                .ok_or_else(|| eyre!("вариант {variant} вне 1..=20"))?;
            let report = process_word(word, k, n, r)?;
            print_report(variant, &report);
        }
        Cmd::All { k, n, r } => {
            for (i, &word) in VARIANTS.iter().enumerate() {
                let report = process_word(word, k, n, r)?;
                let restored = report.recovered_word_by_k();
                let ok = if restored == word { "OK" } else { "FAIL" };
                println!(
                    "Вар {:>2}: '{word}' → восстановлено '{restored}' ({ok})",
                    i + 1
                );
            }
        }
    }
    Ok(())
}

fn print_report(variant: usize, r: &WordReport) {
    println!(
        "=== Вариант {variant}: слово '{}' (k={}, n={}) ===",
        r.word, r.k, r.n
    );
    println!(
        "Каждая буква обрабатывается как отдельный секрет (индекс в алфавите + 50,\n\
         чтобы β < S < α выполнялось для малых простых)."
    );
    for l in &r.letters {
        println!();
        println!(
            "--- Буква {} ('{}'), секрет S = {} ---",
            l.letter_index + 1,
            l.letter,
            l.secret
        );
        println!("Миньотта:");
        println!("  базис p_1..p_n = {:?}", l.mignotte.basis);
        for (i, s) in l.mignotte.shares.iter().enumerate() {
            println!("  α_{} = S mod {} = {}", i + 1, l.mignotte.basis[i], s);
        }
        println!("  восстановление по k долям: {}", l.mignotte.recovered_by_k);
        println!("  восстановление по n долям: {}", l.mignotte.recovered_by_n);
        println!(
            "Асмут-Блум (q={}, r={}, S' = S + r·q):",
            l.asmuth_bloom.q, l.asmuth_bloom.r
        );
        println!("  базис p_1..p_n = {:?}", l.asmuth_bloom.basis);
        for (i, s) in l.asmuth_bloom.shares.iter().enumerate() {
            println!("  α_{} = S' mod {} = {}", i + 1, l.asmuth_bloom.basis[i], s);
        }
        println!(
            "  восстановление S по k долям: {}",
            l.asmuth_bloom.recovered_by_k
        );
        println!(
            "  восстановление S по n долям: {}",
            l.asmuth_bloom.recovered_by_n
        );
    }
    println!();
    println!(
        "Итог: восстановленное слово (по k долям, Миньотта): '{}'",
        r.recovered_word_by_k()
    );
}
