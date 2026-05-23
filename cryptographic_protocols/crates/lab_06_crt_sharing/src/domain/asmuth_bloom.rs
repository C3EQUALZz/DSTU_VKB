//! Пороговая схема Асмут-Блума.
//!
//! По методичке: выбирается простое q > S, затем (k, n)-последовательность
//! взаимно простых чисел p_1 < ... < p_n с условиями q < p_1 и
//!   ∏_{i=1..k} p_i > q · ∏_{i=0..k-2} p_{n-i}.
//!
//! Случайное r, S' = S + r·q. Доли: a_i = S' mod p_i.
//! Восстановление: CRT по любым k долям даёт S', S = S' mod q.

use num_bigint::BigUint;

use super::crt::crt;
use super::errors::DomainError;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Share {
    pub modulus: BigUint,
    pub value: BigUint,
    pub q: BigUint, // q раздаётся открытым параметром
}

/// Параметры схемы.
#[derive(Debug, Clone)]
pub struct Params {
    pub q: BigUint,
    pub basis: Vec<BigUint>, // p_1 < p_2 < ... < p_n
    pub k: usize,
}

/// Разделить секрет: вернуть n долей по `params.basis`.
/// `r` — случайный множитель (должен быть > 0; в реальной системе берётся из RNG).
pub fn split(secret: &BigUint, params: &Params, r: &BigUint) -> Result<Vec<Share>, DomainError> {
    let n = params.basis.len();
    if params.k == 0 || params.k > n {
        return Err(DomainError::InvalidThreshold { k: params.k, n });
    }
    let s_prime = secret + r * &params.q;
    let shares = params
        .basis
        .iter()
        .map(|p| Share {
            modulus: p.clone(),
            value: &s_prime % p,
            q: params.q.clone(),
        })
        .collect();
    Ok(shares)
}

/// Восстановить секрет по k долям. CRT → S', затем S = S' mod q.
pub fn reconstruct(shares: &[Share]) -> Result<BigUint, DomainError> {
    if shares.is_empty() {
        return Err(DomainError::WrongShareCount {
            needed: 1,
            given: 0,
        });
    }
    let moduli: Vec<BigUint> = shares.iter().map(|s| s.modulus.clone()).collect();
    let values: Vec<BigUint> = shares.iter().map(|s| s.value.clone()).collect();
    let s_prime = crt(&values, &moduli)?;
    let q = &shares[0].q;
    Ok(s_prime % q)
}

/// Подобрать параметры (q, basis) по заданному секрету и порогам, перебирая список простых.
///
/// Жадно: q — первое простое > S, далее n последовательных простых > q.
pub fn find_params(
    secret: &BigUint,
    k: usize,
    n: usize,
    primes: &[u64],
) -> Result<Params, DomainError> {
    if k == 0 || k > n {
        return Err(DomainError::InvalidThreshold { k, n });
    }
    for (qi, &qcand) in primes.iter().enumerate() {
        let q = BigUint::from(qcand);
        if &q <= secret {
            continue;
        }
        // n последовательных простых после q.
        if qi + n >= primes.len() {
            break;
        }
        let basis: Vec<BigUint> = primes[qi + 1..qi + 1 + n]
            .iter()
            .map(|p| BigUint::from(*p))
            .collect();
        let alpha: BigUint = basis.iter().take(k).product();
        let beta: BigUint = basis.iter().skip(n - (k - 1)).take(k - 1).product();
        // условие: α > q · β  ⇔  ∏ p_1..p_k > q · ∏ p_{n-k+2}..p_n
        if alpha > &q * &beta {
            return Ok(Params { q, basis, k });
        }
    }
    Err(DomainError::SequenceNotFound {
        k,
        n,
        secret: secret.to_string(),
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Пример из методички: S=250, k=3, n=5, q=257, basis=[263, 269, 271, 277, 281], r=15.
    /// Восстановление по {269, 271, 281} (индексы 1, 2, 4).
    #[test]
    fn methodichka_example_recovers_250() {
        let secret = BigUint::from(250u32);
        let params = Params {
            q: BigUint::from(257u32),
            basis: [263u32, 269, 271, 277, 281]
                .iter()
                .map(|&p| BigUint::from(p))
                .collect(),
            k: 3,
        };
        let shares = split(&secret, &params, &BigUint::from(15u32)).unwrap();
        assert_eq!(shares[0].value, BigUint::from(160u32));
        assert_eq!(shares[1].value, BigUint::from(70u32));
        assert_eq!(shares[2].value, BigUint::from(40u32));
        assert_eq!(shares[3].value, BigUint::from(227u32));
        assert_eq!(shares[4].value, BigUint::from(171u32));
        let trio = vec![shares[1].clone(), shares[2].clone(), shares[4].clone()];
        assert_eq!(reconstruct(&trio).unwrap(), secret);
    }

    #[test]
    fn split_preserves_zero_check() {
        // Если r=0 — также работает, S' = S.
        let secret = BigUint::from(100u32);
        let params = Params {
            q: BigUint::from(101u32),
            basis: [103u32, 107, 109, 113, 127]
                .iter()
                .map(|&p| BigUint::from(p))
                .collect(),
            k: 3,
        };
        let shares = split(&secret, &params, &BigUint::from(0u32)).unwrap();
        let trio = vec![shares[0].clone(), shares[1].clone(), shares[2].clone()];
        assert_eq!(reconstruct(&trio).unwrap(), secret);
    }
}
