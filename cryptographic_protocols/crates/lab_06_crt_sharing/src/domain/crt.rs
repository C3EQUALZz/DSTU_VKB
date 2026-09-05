//! Восстановление целого по системе остатков (CRT) и модулярная инверсия.

use num_bigint::{BigInt, BigUint, Sign};
use num_traits::{One, Zero};

use super::errors::DomainError;

/// Расширенный алгоритм Евклида для `BigInt`: (gcd, x, y), a·x + b·y = gcd.
pub fn ext_gcd(a: &BigInt, b: &BigInt) -> (BigInt, BigInt, BigInt) {
    if b.is_zero() {
        (a.clone(), BigInt::one(), BigInt::zero())
    } else {
        tracing::info!(step = "crt.euclid", a = %a, b = %b, quotient = %a/b, remainder = %a%b, "деление с остатком в алгоритме Евклида");
        let (g, x1, y1) = ext_gcd(b, &(a % b));
        (g, y1.clone(), x1 - (a / b) * y1)
    }
}

/// Модулярный обратный по модулю m: a^{-1} mod m.
pub fn mod_inv(a: &BigUint, m: &BigUint) -> Result<BigUint, DomainError> {
    let ai = BigInt::from_biguint(Sign::Plus, a.clone());
    let mi = BigInt::from_biguint(Sign::Plus, m.clone());
    let (g, x, _) = ext_gcd(&ai, &mi);
    if g != BigInt::one() {
        return Err(DomainError::NoModularInverse {
            a: a.to_string(),
            p: m.to_string(),
        });
    }
    let r = ((x % &mi) + &mi) % &mi;
    tracing::info!(step = "crt.inverse", a = %a, m = %m, r = %r, "вычислен обратный элемент CRT");
    r.to_biguint().ok_or_else(|| DomainError::NoModularInverse {
        a: a.to_string(),
        p: m.to_string(),
    })
}

/// Восстановить число S, такое что S ≡ a_i (mod m_i) для всех i, через CRT
/// (Китайская теорема об остатках). Возвращает S в диапазоне [0, ∏ m_i).
pub fn crt(remainders: &[BigUint], moduli: &[BigUint]) -> Result<BigUint, DomainError> {
    if remainders.len() != moduli.len() {
        return Err(DomainError::WrongShareCount {
            needed: moduli.len(),
            given: remainders.len(),
        });
    }
    let big_p: BigUint = moduli.iter().product();
    tracing::info!(step = "crt.product", moduli = ?moduli, big_p = %big_p, "вычислен общий модуль M = произведение модулей");
    let mut result = BigUint::zero();
    for (i, (a, m)) in remainders.iter().zip(moduli.iter()).enumerate() {
        let pi = &big_p / m;
        let inv = mod_inv(&(pi.clone() % m), m)?;
        let term = a * &pi * &inv;
        tracing::info!(step = "crt.term", share = %i+1, a = %a, m = %m, partial_modulus = %pi, inverse = %inv, term = %term, "слагаемое CRT = residue * M_i * inverse");
        result = (result + term) % &big_p;
        tracing::info!(step = "crt.accumulate", share = %i+1, result = %result, big_p = %big_p, "накоплена сумма CRT по модулю M");
    }
    Ok(result)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn crt_from_methodichka_mignotte_example() {
        // n=250 mod {5, 11, 17} = {0, 8, 12} → CRT по [5,11,17] = 250.
        let r = crt(
            &[
                BigUint::from(0u32),
                BigUint::from(8u32),
                BigUint::from(12u32),
            ],
            &[
                BigUint::from(5u32),
                BigUint::from(11u32),
                BigUint::from(17u32),
            ],
        )
        .unwrap();
        assert_eq!(r, BigUint::from(250u32));
    }

    #[test]
    fn mod_inv_small() {
        assert_eq!(
            mod_inv(&BigUint::from(3u32), &BigUint::from(11u32)).unwrap(),
            BigUint::from(4u32)
        );
    }
}
