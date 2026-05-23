//! Поиск первообразных корней по модулю n.
//!
//! По теореме Эйлера для взаимно простых a и n: a^φ(n) ≡ 1 (mod n).
//! Число a называется первообразным корнем, если оно принадлежит показателю φ(n).
//!
//! Свойство 5 (методичка): a — первообразный корень ⇔ a^(c/q_i) ≢ 1 (mod n)
//! для всех простых делителей q_i числа c = φ(n).
//!
//! Для простого p: φ(p) = p − 1. Дальше нужно факторизовать p − 1.

use num_bigint::BigUint;
use num_integer::Integer;
use num_traits::{One, Zero};
use tracing::trace;

/// Простая факторизация методом пробных делителей.
///
/// Для p − 1 при 65-битном p размер ≈ 64 бита, что вполне ловится trial division
/// до √n за разумное время на демо-данных. Для боевого кода нужен Pollard ρ.
pub fn factorize(mut n: BigUint) -> Vec<BigUint> {
    let mut factors = Vec::new();
    if n < BigUint::from(2u32) {
        return factors;
    }
    let two = BigUint::from(2u32);
    while n.is_even() {
        if factors.last() != Some(&two) {
            factors.push(two.clone());
        }
        n >>= 1;
    }
    let mut d = BigUint::from(3u32);
    while &d * &d <= n {
        if (&n % &d).is_zero() {
            if factors.last() != Some(&d) {
                factors.push(d.clone());
            }
            n /= &d;
        } else {
            d += 2u32;
        }
    }
    if n > BigUint::one() && Some(&n) != factors.last() {
        factors.push(n);
    }
    factors
}

/// Проверка: a — первообразный корень по простому модулю p?
///
/// Алгоритм по свойству 5 методички:
///   c = p − 1; для каждого простого q | c проверяем a^(c/q) ≢ 1 (mod p).
pub fn is_primitive_root(a: &BigUint, p: &BigUint, c_factors: &[BigUint]) -> bool {
    let one = BigUint::one();
    if a.is_zero() || a >= p {
        return false;
    }
    let c = p - &one;
    for q in c_factors {
        let exp = &c / q;
        if a.modpow(&exp, p) == one {
            trace!(%a, %q, "не первообразный: a^(c/q) ≡ 1");
            return false;
        }
    }
    true
}

/// Найти первые `count` первообразных корней по модулю простого `p`, перебирая a = 2, 3, …
pub fn first_primitive_roots(p: &BigUint, count: usize) -> Vec<BigUint> {
    let factors = factorize(p - BigUint::one());
    trace!(?factors, %p, "факторизация p-1");
    let mut roots = Vec::with_capacity(count);
    let mut a = BigUint::from(2u32);
    while roots.len() < count && a < *p {
        if is_primitive_root(&a, p, &factors) {
            roots.push(a.clone());
        }
        a += 1u32;
    }
    roots
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn factorize_basic() {
        assert_eq!(
            factorize(BigUint::from(40u32)),
            vec![BigUint::from(2u32), BigUint::from(5u32)]
        );
        assert_eq!(factorize(BigUint::from(17u32)), vec![BigUint::from(17u32)]);
        assert_eq!(factorize(BigUint::from(1u32)), vec![]);
    }

    #[test]
    fn primitive_root_mod_41_is_6() {
        // Из методички: для p=41, первообразный корень — 6.
        let p = BigUint::from(41u32);
        let factors = factorize(p.clone() - BigUint::one());
        // p-1 = 40 = 2^3·5, простые делители: {2, 5}.
        assert_eq!(factors, vec![BigUint::from(2u32), BigUint::from(5u32)]);
        // 6 — первообразный, 2/3/4/5 — нет (по методичке).
        for &a in &[2u32, 3, 4, 5] {
            assert!(
                !is_primitive_root(&BigUint::from(a), &p, &factors),
                "ожидали что {a} не первообразный по mod 41"
            );
        }
        assert!(is_primitive_root(&BigUint::from(6u32), &p, &factors));
    }

    #[test]
    fn first_primitive_roots_mod_41_starts_with_6() {
        let roots = first_primitive_roots(&BigUint::from(41u32), 4);
        // По таблице первообразных корней mod 41: {6, 7, 11, 12, ...}.
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
    fn primitive_root_mod_97_is_5() {
        // По методичке (пример обмена): для p=97 g=5 используется как первообразный корень.
        let p = BigUint::from(97u32);
        let factors = factorize(p.clone() - BigUint::one());
        assert!(is_primitive_root(&BigUint::from(5u32), &p, &factors));
    }
}
