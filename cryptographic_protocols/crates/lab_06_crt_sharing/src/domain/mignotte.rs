//! Пороговая схема Миньотта на (k, n)-последовательности взаимно простых чисел.
//!
//! Условие на (k, n)-последовательность Миньотта (методичка, тема 6):
//!   p_1 < p_2 < ... < p_n,  попарно взаимно простые,
//!   β = ∏_{i=0..k-2} p_{n-i} < S < α = ∏_{i=1..k} p_i.
//!
//! Доли: a_i = S mod p_i. По любым k долям S восстанавливается через CRT.

use num_bigint::BigUint;
use num_traits::{One, Zero};
use tracing::debug;

use super::crt::crt;
use super::errors::DomainError;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Share {
    pub modulus: BigUint,
    pub value: BigUint,
}

/// Сгенерировать (k, n)-схему Миньотта поверх готового базиса.
///
/// `basis` должен быть отсортирован по возрастанию.
/// Условие α > S > β проверяется здесь.
pub fn split(secret: &BigUint, basis: &[BigUint], k: usize) -> Result<Vec<Share>, DomainError> {
    let n = basis.len();
    if k == 0 || k > n {
        return Err(DomainError::InvalidThreshold { k, n });
    }
    let alpha: BigUint = basis.iter().take(k).product();
    let beta: BigUint = basis.iter().skip(n - (k - 1)).take(k - 1).product();
    if !(secret > &beta && secret < &alpha) {
        return Err(DomainError::SequenceNotFound {
            k,
            n,
            secret: secret.to_string(),
        });
    }
    let shares = basis
        .iter()
        .map(|p| Share {
            modulus: p.clone(),
            value: secret % p,
        })
        .collect();
    Ok(shares)
}

/// Восстановить секрет по k долям через CRT.
pub fn reconstruct(shares: &[Share]) -> Result<BigUint, DomainError> {
    let moduli: Vec<BigUint> = shares.iter().map(|s| s.modulus.clone()).collect();
    let values: Vec<BigUint> = shares.iter().map(|s| s.value.clone()).collect();
    crt(&values, &moduli)
}

/// Подобрать (k, n)-последовательность Миньотта из набора кандидатов
/// (заранее заданные простые от заданного индекса).
///
/// Используем простой жадный поиск: берём `n` последовательных простых начиная
/// с `min_prime` и проверяем выполнение условия для секрета.
pub fn find_basis(
    secret: &BigUint,
    k: usize,
    n: usize,
    primes: &[u64],
) -> Result<Vec<BigUint>, DomainError> {
    if k == 0 || k > n {
        return Err(DomainError::InvalidThreshold { k, n });
    }
    for start in 0..primes.len().saturating_sub(n) {
        let candidate: Vec<BigUint> = primes[start..start + n]
            .iter()
            .map(|p| BigUint::from(*p))
            .collect();
        let alpha: BigUint = candidate.iter().take(k).product();
        let beta: BigUint = candidate.iter().skip(n - (k - 1)).take(k - 1).product();
        debug!(start, %alpha, %beta, "проверяем кандидата");
        if &beta < secret && secret < &alpha && is_pairwise_coprime(&candidate) {
            return Ok(candidate);
        }
    }
    Err(DomainError::SequenceNotFound {
        k,
        n,
        secret: secret.to_string(),
    })
}

fn is_pairwise_coprime(xs: &[BigUint]) -> bool {
    for i in 0..xs.len() {
        for j in (i + 1)..xs.len() {
            let mut a = xs[i].clone();
            let mut b = xs[j].clone();
            while !b.is_zero() {
                let r = a % &b;
                a = b;
                b = r;
            }
            if a != BigUint::one() {
                return false;
            }
        }
    }
    true
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Пример из методички: S=250, (k=3, n=5), basis = [5, 7, 11, 13, 17].
    /// β = 13·17 = 221, α = 5·7·11 = 385.  221 < 250 < 385.
    #[test]
    fn methodichka_example_splits_and_reconstructs() {
        let secret = BigUint::from(250u32);
        let basis: Vec<BigUint> = [5u32, 7, 11, 13, 17]
            .iter()
            .map(|&p| BigUint::from(p))
            .collect();
        let shares = split(&secret, &basis, 3).unwrap();
        assert_eq!(shares[0].value, BigUint::from(0u32));
        assert_eq!(shares[1].value, BigUint::from(5u32));
        assert_eq!(shares[2].value, BigUint::from(8u32));
        assert_eq!(shares[3].value, BigUint::from(3u32));
        assert_eq!(shares[4].value, BigUint::from(12u32));
        // Восстановим по {1, 3, 5} = индексы 0, 2, 4.
        let trio = vec![shares[0].clone(), shares[2].clone(), shares[4].clone()];
        assert_eq!(reconstruct(&trio).unwrap(), secret);
    }
}
