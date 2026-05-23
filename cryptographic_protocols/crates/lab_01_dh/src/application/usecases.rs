//! Прикладные сценарии лабораторной 1.

use std::time::{Duration, Instant};

use num_bigint::BigUint;
use num_traits::One;
use tracing::{debug, info};

use crate::domain::dh::{Party, PublicParameters, shared_secret};
use crate::domain::errors::DomainError;
use crate::domain::prime::{
    PrimeGenStats, divisible_by_small_prime, generate_prime, is_probably_prime,
};
use crate::domain::primitive_root::first_primitive_roots;
use crate::domain::rng::RandomSource;

/// Результат генерации простого: само число, статистика и затраченное время.
#[derive(Debug, Clone)]
pub struct GenPrimeReport {
    pub prime: BigUint,
    pub bits: u32,
    pub stats: PrimeGenStats,
    pub elapsed: Duration,
}

/// Сценарий: сгенерировать одно простое число длиной `bits` бит.
pub fn generate_prime_uc<R: RandomSource>(
    bits: u32,
    rounds: u32,
    max_tries: u32,
    rng: &mut R,
) -> Result<GenPrimeReport, DomainError> {
    info!(bits, rounds, "генерация простого числа");
    let started = Instant::now();
    let (prime, stats) = generate_prime(bits, rounds, max_tries, rng)?;
    let elapsed = started.elapsed();
    info!(
        ?elapsed,
        iterations = stats.iterations,
        rejected_small = stats.rejected_by_small_primes,
        rejected_mr = stats.rejected_by_miller_rabin,
        "простое получено"
    );
    Ok(GenPrimeReport {
        prime,
        bits,
        stats,
        elapsed,
    })
}

/// Все простые в диапазоне [from; to). Возвращает список и общее время.
pub fn range_primes_uc<R: RandomSource>(
    from: BigUint,
    to: &BigUint,
    rounds: u32,
    rng: &mut R,
) -> (Vec<BigUint>, Duration) {
    let started = Instant::now();
    let mut out = Vec::new();
    let mut n = from;
    while n < *to {
        if !divisible_by_small_prime(&n) && is_probably_prime(&n, rounds, rng) {
            out.push(n.clone());
        }
        n += BigUint::one();
    }
    let elapsed = started.elapsed();
    debug!(found = out.len(), ?elapsed, "диапазон обработан");
    (out, elapsed)
}

/// Первые `count` первообразных корней по простому `p` и время на их поиск.
pub fn primitive_roots_uc(p: &BigUint, count: usize) -> (Vec<BigUint>, Duration) {
    let started = Instant::now();
    let roots = first_primitive_roots(p, count);
    let elapsed = started.elapsed();
    info!(found = roots.len(), ?elapsed, "первообразные корни найдены");
    (roots, elapsed)
}

/// Результат сеанса обмена ключами Диффи-Хеллмана.
#[derive(Debug, Clone)]
pub struct DhExchangeReport {
    pub params: PublicParameters,
    pub alice: Party,
    pub bob: Party,
    pub shared_alice: BigUint,
    pub shared_bob: BigUint,
}

impl DhExchangeReport {
    pub fn keys_match(&self) -> bool {
        self.shared_alice == self.shared_bob
    }
}

/// Сценарий «полный обмен»: оба секрета X_A, X_B заданы заранее.
pub fn dh_exchange_fixed(
    params: PublicParameters,
    x_alice: BigUint,
    x_bob: BigUint,
) -> Result<DhExchangeReport, DomainError> {
    let alice = Party::from_private(x_alice, &params)?;
    let bob = Party::from_private(x_bob, &params)?;
    let shared_alice = shared_secret(&alice.x, &bob.y, &params.n);
    let shared_bob = shared_secret(&bob.x, &alice.y, &params.n);
    Ok(DhExchangeReport {
        params,
        alice,
        bob,
        shared_alice,
        shared_bob,
    })
}

/// Сценарий «полный обмен»: секреты выбираются случайно.
pub fn dh_exchange_random<R: RandomSource>(
    params: PublicParameters,
    rng: &mut R,
) -> DhExchangeReport {
    let alice = Party::random(&params, rng);
    let bob = Party::random(&params, rng);
    let shared_alice = shared_secret(&alice.x, &bob.y, &params.n);
    let shared_bob = shared_secret(&bob.x, &alice.y, &params.n);
    DhExchangeReport {
        params,
        alice,
        bob,
        shared_alice,
        shared_bob,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::domain::rng::SeededRng;

    #[test]
    fn primitive_roots_for_41() {
        let (roots, _) = primitive_roots_uc(&BigUint::from(41u32), 4);
        assert_eq!(
            roots,
            vec![
                BigUint::from(6u32),
                BigUint::from(7u32),
                BigUint::from(11u32),
                BigUint::from(12u32),
            ]
        );
    }

    #[test]
    fn range_primes_under_30() {
        let mut rng = SeededRng::new(1);
        let (primes, _) = range_primes_uc(BigUint::from(2u32), &BigUint::from(30u32), 8, &mut rng);
        let nums: Vec<u32> = primes
            .iter()
            .map(|p| p.iter_u32_digits().next().unwrap_or(0))
            .collect();
        assert_eq!(nums, vec![2, 3, 5, 7, 11, 13, 17, 19, 23, 29]);
    }

    #[test]
    fn fixed_dh_matches_methodichka() {
        let report = dh_exchange_fixed(
            PublicParameters {
                n: BigUint::from(97u32),
                g: BigUint::from(5u32),
            },
            BigUint::from(36u32),
            BigUint::from(58u32),
        )
        .unwrap();
        assert!(report.keys_match());
        assert_eq!(report.shared_alice, BigUint::from(75u32));
    }
}
