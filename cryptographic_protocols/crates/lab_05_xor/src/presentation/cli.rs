//! CLI лаб 5: шифрование/дешифрование произвольного текста.

use clap::{Parser, Subcommand};
use color_eyre::Result;
use color_eyre::eyre::eyre;

use crate::application::usecases::xor_apply;

#[derive(Parser, Debug)]
#[command(name = "lab_05_xor", about = "Лаб 5 — XOR-шифрование", version)]
struct Cli {
    #[command(subcommand)]
    cmd: Cmd,
}

#[derive(Subcommand, Debug)]
enum Cmd {
    /// Зашифровать UTF-8 текст однобайтовым или многобайтовым ключом.
    Encrypt {
        /// Открытый текст.
        text: String,
        /// Ключ: одно число 0..255 (например 70) или строка (например "KEY").
        #[arg(long)]
        key: String,
    },
    /// Расшифровать байты, заданные как разделённые пробелами десятичные числа.
    Decrypt {
        /// Шифртекст в виде "139 168 ..." (десятичные коды байтов).
        cipher: String,
        #[arg(long)]
        key: String,
    },
    /// Прогнать пример из методички: стих Блока с ключом 70.
    Demo,
}

fn parse_key(s: &str) -> Vec<u8> {
    if let Ok(n) = s.parse::<u8>() {
        return vec![n];
    }
    s.as_bytes().to_vec()
}

fn parse_decimal_bytes(s: &str) -> Result<Vec<u8>> {
    s.split_whitespace()
        .map(|t| t.parse::<u8>().map_err(|e| eyre!("не байт '{t}': {e}")))
        .collect()
}

pub fn run() -> Result<()> {
    match Cli::parse().cmd {
        Cmd::Encrypt { text, key } => {
            let k = parse_key(&key);
            let report = xor_apply(text.as_bytes(), &k);
            println!("Открытый текст: {text}");
            println!("Ключ (байты): {:?}", report.key);
            println!("Шифртекст (HEX): {}", report.output_hex());
            println!("Шифртекст (DEC): {}", report.output_decimal());
        }
        Cmd::Decrypt { cipher, key } => {
            let cipher_bytes = parse_decimal_bytes(&cipher)?;
            let k = parse_key(&key);
            let report = xor_apply(&cipher_bytes, &k);
            let text = String::from_utf8_lossy(&report.output);
            println!(
                "Шифртекст (DEC): {}",
                report
                    .input
                    .iter()
                    .map(u8::to_string)
                    .collect::<Vec<_>>()
                    .join(" ")
            );
            println!("Ключ (байты): {:?}", report.key);
            println!("Расшифрованный текст: {text}");
        }
        Cmd::Demo => {
            let stanza = "Ночь, улица, фонарь, аптека,\n\
                          Бессмысленный и тусклый свет.\n\
                          Живи ещё хоть четверть века —\n\
                          Всё будет так. Исхода нет.";
            let key = [70u8];
            let enc = xor_apply(stanza.as_bytes(), &key);
            println!("=== Пример из методички (стих А. Блока, K=70) ===");
            println!("Открытый текст:");
            println!("{stanza}");
            println!();
            println!("Шифртекст (DEC): {}", enc.output_decimal());
            let dec = xor_apply(&enc.output, &key);
            println!();
            println!(
                "Дешифровка применением того же ключа: {}",
                String::from_utf8_lossy(&dec.output)
            );
            println!("Совпадает с исходным: {}", dec.output == stanza.as_bytes());
        }
    }
    Ok(())
}
