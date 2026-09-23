//! CLI обмена ключами Диффи–Хеллмана.
//!
//! Подкоманды:
//! - `gen-prime`     — сгенерировать одно простое заданной разрядности.
//! - `range-primes`  — найти все простые в [from; to).
//! - `roots`         — первые N первообразных корней по простому модулю.
//! - `dh`            — обмен ключами по Диффи-Хеллману (с фиксированными или случайными X).
//! - `serve`/`connect` — два процесса с зашифрованными сообщениями.

use std::io;
use std::net::{SocketAddr, TcpListener, TcpStream};

use clap::{Parser, Subcommand};
use color_eyre::Result;
use color_eyre::eyre::{Context, bail, eyre};
use num_bigint::BigUint;
use num_traits::Num;
use tracing::info;

use crate::application::channel::{self, SecureSession};
use crate::application::usecases::{
    DhExchangeReport, GenPrimeReport, dh_exchange_fixed, dh_exchange_generated, dh_exchange_random,
    generate_prime_uc, primitive_roots_uc, range_primes_uc,
};
use crate::domain::dh::PublicParameters;
use crate::domain::rng::{RandomSource, SeededRng};
use crate::infrastructure::tcp::TcpTransport;

#[derive(Parser, Debug)]
#[command(
    name = "diffie_hellman",
    about = "Диффи–Хеллман и учебный канал связи",
    version
)]
struct Cli {
    #[command(subcommand)]
    cmd: Cmd,

    /// Сид для RNG. Если не задан — берётся из энтропии ОС.
    #[arg(long, global = true)]
    seed: Option<u64>,
}

#[derive(Subcommand, Debug)]
enum Cmd {
    /// Сгенерировать одно простое n-битное число.
    GenPrime {
        /// Число бит (по условию ≥ 65, чтобы p > 2^64).
        #[arg(long, default_value_t = 128)]
        bits: u32,
        /// Число раундов Рабина-Миллера.
        #[arg(long, default_value_t = 32)]
        rounds: u32,
        /// Максимум попыток.
        #[arg(long, default_value_t = 10_000)]
        max_tries: u32,
    },

    /// Найти все простые в диапазоне [from; to).
    RangePrimes {
        #[arg(long)]
        from: String,
        #[arg(long)]
        to: String,
        #[arg(long, default_value_t = 16)]
        rounds: u32,
    },

    /// Первые `count` первообразных корней по простому модулю `n`.
    Roots {
        #[arg(long)]
        n: String,
        #[arg(long, default_value_t = 100)]
        count: usize,
    },

    /// Однопроцессный обмен ключами по Диффи–Хеллману.
    Dh {
        /// Простой модуль n. Если не задан — будет сгенерирован простой `bits`-битный.
        #[arg(long)]
        n: Option<String>,
        /// Первообразный корень g. Если не задан — берётся наименьший для n.
        #[arg(long)]
        g: Option<String>,
        /// Секрет Алисы (необязательно).
        #[arg(long)]
        xa: Option<String>,
        /// Секрет Боба (необязательно).
        #[arg(long)]
        xb: Option<String>,
        /// Разрядность авто-сгенерированного n (если n не задан).
        #[arg(long, default_value_t = 128)]
        bits: u32,
        #[arg(long, default_value_t = 32)]
        rounds: u32,
    },

    /// Запустить сервер учебного зашифрованного канала.
    Serve {
        #[arg(long, default_value = "127.0.0.1:7878")]
        bind: SocketAddr,
        #[arg(long, default_value_t = 128)]
        bits: u32,
        #[arg(long, default_value_t = 32)]
        rounds: u32,
        /// Завершить работу после одного сеанса (удобно для демонстрации).
        #[arg(long)]
        once: bool,
    },

    /// Подключиться к серверу и отправлять зашифрованные сообщения.
    Connect {
        #[arg(long, default_value = "127.0.0.1:7878")]
        addr: SocketAddr,
        #[arg(long, default_value_t = 32)]
        rounds: u32,
        /// Сообщение; можно повторить. Без флага включается ввод с клавиатуры.
        #[arg(long = "message")]
        messages: Vec<String>,
    },
}

/// Парсит число: пробует hex (0x...), затем десятичное.
fn parse_big(s: &str) -> Result<BigUint> {
    if let Some(rest) = s.strip_prefix("0x").or_else(|| s.strip_prefix("0X")) {
        return BigUint::from_str_radix(rest, 16)
            .map_err(|e| eyre!("неверное hex-число '{s}': {e}"));
    }
    BigUint::from_str_radix(s, 10).map_err(|e| eyre!("неверное число '{s}': {e}"))
}

/// Точка входа.
///
/// Логгер должен быть инициализирован до вызова (в `main`).
pub fn run() -> Result<()> {
    let cli = Cli::parse();
    let mut rng = match cli.seed {
        Some(s) => SeededRng::new(s),
        None => SeededRng::from_entropy(),
    };

    match cli.cmd {
        Cmd::GenPrime {
            bits,
            rounds,
            max_tries,
        } => {
            let report = generate_prime_uc(bits, rounds, max_tries, &mut rng)
                .wrap_err("не удалось сгенерировать простое")?;
            print_gen_prime(&report);
        }
        Cmd::RangePrimes { from, to, rounds } => {
            if rounds < 5 {
                bail!("нужно минимум 5 раундов Рабина–Миллера");
            }
            let lo = parse_big(&from)?;
            let hi = parse_big(&to)?;
            if hi <= lo {
                return Err(eyre!("требуется to > from"));
            }
            let (primes, elapsed) = range_primes_uc(lo, &hi, rounds, &mut rng);
            // Прямой вывод результата (часть условия задания).
            println!("найдено простых: {}", primes.len());
            for p in &primes {
                println!("{p}");
            }
            println!("суммарное время: {elapsed:?}");
        }
        Cmd::Roots { n, count } => {
            let n_big = parse_big(&n)?;
            let (roots, elapsed) = primitive_roots_uc(&n_big, count);
            println!("найдено первообразных корней: {}", roots.len());
            for r in &roots {
                println!("{r}");
            }
            println!("суммарное время: {elapsed:?}");
        }
        Cmd::Dh {
            n,
            g,
            xa,
            xb,
            bits,
            rounds,
        } => run_dh(n, g, xa, xb, bits, rounds, &mut rng)?,
        Cmd::Serve {
            bind,
            bits,
            rounds,
            once,
        } => {
            if cli.seed.is_some() {
                bail!(
                    "--seed нельзя использовать в сетевом сеансе: приватные значения станут предсказуемыми"
                );
            }
            if !bind.ip().is_loopback() {
                bail!("учебный сервер принимает подключения только на localhost");
            }
            if !(67..=512).contains(&bits) || rounds < 5 {
                bail!("для сетевого сеанса нужны 67..=512 бит и минимум 5 раундов Рабина–Миллера");
            }
            run_server(bind, bits, rounds, once, &mut rng)?;
        }
        Cmd::Connect {
            addr,
            rounds,
            messages,
        } => {
            if cli.seed.is_some() {
                bail!(
                    "--seed нельзя использовать в сетевом сеансе: приватные значения станут предсказуемыми"
                );
            }
            if !addr.ip().is_loopback() {
                bail!("учебный клиент подключается только к localhost");
            }
            if rounds < 5 {
                bail!("нужно минимум 5 раундов Рабина–Миллера");
            }
            run_client(addr, rounds, messages, &mut rng)?;
        }
    }
    Ok(())
}

fn run_dh<R: RandomSource>(
    n: Option<String>,
    g: Option<String>,
    xa: Option<String>,
    xb: Option<String>,
    bits: u32,
    rounds: u32,
    rng: &mut R,
) -> Result<()> {
    if n.is_none() {
        if g.is_some() || xa.is_some() || xb.is_some() {
            bail!(
                "при автоматической генерации p, g и X не задавайте --g, --xa или --xb; для ручного примера задайте --n"
            );
        }
        let report = dh_exchange_generated(bits, rounds, rng)?;
        print_dh(&report);
        return Ok(());
    }
    let n_big = parse_big(&n.ok_or_else(|| eyre!("нужно указать --n"))?)?;
    let g_big = if let Some(s) = g {
        parse_big(&s)?
    } else {
        if n_big.bits() > 64 {
            bail!(
                "для большого заданного --n укажите --g; поиск корня факторизацией может занять слишком много времени"
            );
        }
        let (roots, _) = primitive_roots_uc(&n_big, 1);
        roots
            .into_iter()
            .next()
            .ok_or_else(|| eyre!("не нашли первообразный корень для n"))?
    };
    let params = PublicParameters { n: n_big, g: g_big };
    let report = match (xa, xb) {
        (Some(a), Some(b)) => dh_exchange_fixed(params, parse_big(&a)?, parse_big(&b)?)
            .wrap_err("обмен ключами не удался")?,
        _ => dh_exchange_random(params, rng),
    };
    print_dh(&report);
    Ok(())
}

fn run_server<R: RandomSource>(
    bind: SocketAddr,
    bits: u32,
    rounds: u32,
    once: bool,
    rng: &mut R,
) -> Result<()> {
    let listener = TcpListener::bind(bind).wrap_err("не удалось открыть порт сервера")?;
    info!(address = %listener.local_addr()?, "сервер ожидает подключения");
    loop {
        let (stream, peer) = listener.accept().wrap_err("ошибка ожидания клиента")?;
        info!(%peer, "клиент подключился");
        let transport = TcpTransport::new(stream)?;
        let mut session = channel::accept(transport, bits, rounds, rng)?;
        channel::serve_messages(&mut session)?;
        info!(%peer, "сеанс клиента завершён");
        if once {
            return Ok(());
        }
    }
}

fn run_client<R: RandomSource>(
    addr: SocketAddr,
    rounds: u32,
    messages: Vec<String>,
    rng: &mut R,
) -> Result<()> {
    let stream = TcpStream::connect(addr).wrap_err("не удалось подключиться к серверу")?;
    info!(%addr, "клиент подключился к серверу");
    let transport = TcpTransport::new(stream)?;
    let mut session = channel::connect(transport, rounds, rng)?;
    if messages.is_empty() {
        interactive_client(&mut session)?;
    } else {
        for message in messages {
            let answer = channel::send_text(&mut session, message)?;
            println!("Ответ сервера: {answer}");
        }
    }
    channel::close(&mut session)
}

fn interactive_client(session: &mut SecureSession<TcpTransport>) -> Result<()> {
    println!("Введите сообщение; /quit завершает сеанс.");
    let mut line = String::new();
    loop {
        line.clear();
        if io::stdin().read_line(&mut line)? == 0 || line.trim() == "/quit" {
            return Ok(());
        }
        let answer = channel::send_text(session, line.trim_end_matches(['\r', '\n']).to_owned())?;
        println!("Ответ сервера: {answer}");
    }
}

fn print_gen_prime(r: &GenPrimeReport) {
    println!("Простое число ({} бит):", r.bits);
    println!("{}", r.prime);
    println!("итераций алгоритма: {}", r.stats.iterations);
    println!(
        "отсеяно малыми простыми: {}",
        r.stats.rejected_by_small_primes
    );
    println!(
        "отсеяно Рабином-Миллером: {}",
        r.stats.rejected_by_miller_rabin
    );
    println!("время: {:?}", r.elapsed);
}

fn print_dh(r: &DhExchangeReport) {
    println!("=== Диффи-Хеллман ===");
    println!("Открытые параметры:");
    println!("  n = {}", r.params.n);
    println!("  g = {}", r.params.g);
    println!();
    println!("Абонент A:");
    println!("  X_A = {}", r.alice.x);
    println!("  Y_A = g^X_A mod n = {}", r.alice.y);
    println!();
    println!("Абонент B:");
    println!("  X_B = {}", r.bob.x);
    println!("  Y_B = g^X_B mod n = {}", r.bob.y);
    println!();
    println!("Общий ключ A: Y_B^X_A mod n = {}", r.shared_alice);
    println!("Общий ключ B: Y_A^X_B mod n = {}", r.shared_bob);
    println!(
        "Ключи совпадают: {}",
        if r.keys_match() { "ДА" } else { "НЕТ" }
    );
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_big_decimal() {
        assert_eq!(parse_big("12345").unwrap(), BigUint::from(12345u32));
    }

    #[test]
    fn parse_big_hex() {
        assert_eq!(parse_big("0xff").unwrap(), BigUint::from(255u32));
        assert_eq!(parse_big("0XFF").unwrap(), BigUint::from(255u32));
    }
}
