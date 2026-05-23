//! Тест простоты Рабина-Миллера и генерация больших простых чисел.
//!
//! По методичке (Шнайер, «Прикладная криптография»):
//! 1. Сгенерировать случайное n-битное число p.
//! 2. Старший и младший биты = 1.
//! 3. Проверить делимость на малые простые (< 2000).
//! 4. Прогнать Рабина-Миллера t раз.

use num_bigint::BigUint;
use num_integer::Integer;
use num_traits::{One, Zero};
use tracing::{debug, trace, warn};

use super::errors::DomainError;
use super::rng::RandomSource;

/// Малые простые до 2000 — для предварительного отсева. По методичке отсекает ~80% составных.
pub const SMALL_PRIMES: &[u32] = &[
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
    101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193,
    197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307,
    311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421,
    431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547,
    557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659,
    661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797,
    809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929,
    937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039,
    1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153,
    1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279,
    1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409,
    1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471, 1481, 1483, 1487, 1489, 1493, 1499,
    1511, 1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1597, 1601, 1607, 1609, 1613,
    1619, 1621, 1627, 1637, 1657, 1663, 1667, 1669, 1693, 1697, 1699, 1709, 1721, 1723, 1733, 1741,
    1747, 1753, 1759, 1777, 1783, 1787, 1789, 1801, 1811, 1823, 1831, 1847, 1861, 1867, 1871, 1873,
    1877, 1879, 1889, 1901, 1907, 1913, 1931, 1933, 1949, 1951, 1973, 1979, 1987, 1993, 1997, 1999,
];

/// Делится ли `n` на любое из малых простых (не считая случая, когда n само равно этому простому).
pub fn divisible_by_small_prime(n: &BigUint) -> bool {
    for &p in SMALL_PRIMES {
        let p_big = BigUint::from(p);
        if n == &p_big {
            return false;
        }
        if (n % &p_big).is_zero() {
            return true;
        }
    }
    false
}

/// Тест простоты Рабина-Миллера с `t` раундами.
///
/// Гарантирует: если число составное, вероятность пройти проверку ≤ (1/4)^t.
/// Алгоритм по Шнайеру:
///   p − 1 = 2^b · m, m нечётно.
///   Для случайного 2 ≤ a < p − 1: z = a^m mod p.
///   Если z=1 или z=p−1 — возможно простое.
///   Иначе возводим z в квадрат до b−1 раз; если получаем p−1 — возможно простое,
///   если 1 при j>0 — составное.
pub fn is_probably_prime<R: RandomSource>(p: &BigUint, t: u32, rng: &mut R) -> bool {
    if *p < BigUint::from(2u32) {
        return false;
    }
    if *p == BigUint::from(2u32) || *p == BigUint::from(3u32) {
        return true;
    }
    if p.is_even() {
        return false;
    }

    // p − 1 = 2^b · m
    let one = BigUint::one();
    let p_minus_1 = p - &one;
    let (b, m) = decompose(&p_minus_1);
    trace!(b, m = %m, "Рабин-Миллер: разложение p-1 = 2^b · m");

    let two = BigUint::from(2u32);
    'witness: for round in 0..t {
        let a = rng.random_range(&two, &p_minus_1);
        trace!(round, a = %a, "новый свидетель");
        let mut z = a.modpow(&m, p);
        if z == one || z == p_minus_1 {
            continue 'witness;
        }
        for _ in 0..b - 1 {
            z = z.modpow(&two, p);
            if z == one {
                trace!(round, "z=1 при j>0 ⇒ составное");
                return false;
            }
            if z == p_minus_1 {
                continue 'witness;
            }
        }
        // Не достигли ни 1, ни p-1 → составное.
        trace!(round, "z ≠ p-1 после b шагов ⇒ составное");
        return false;
    }
    true
}

/// Раскладывает n = 2^b · m, где m нечётно.
fn decompose(n: &BigUint) -> (u32, BigUint) {
    let mut b = 0u32;
    let mut m = n.clone();
    while m.is_even() && !m.is_zero() {
        m >>= 1;
        b += 1;
    }
    (b, m)
}

/// Статистика, возвращаемая `generate_prime`.
#[derive(Debug, Clone)]
pub struct PrimeGenStats {
    /// Сколько итераций (попыток случайного p) потребовалось.
    pub iterations: u32,
    /// Сколько кандидатов отсеялось по малым делителям.
    pub rejected_by_small_primes: u32,
    /// Сколько кандидатов отсеял Рабин-Миллер.
    pub rejected_by_miller_rabin: u32,
}

/// Сгенерировать простое число длиной ровно `bits` бит, выполняя `t` раундов Рабина-Миллера.
///
/// `max_tries` — защита от зацикливания; для bits ≥ 32 практически никогда не достигается.
///
/// # Errors
/// - [`DomainError::TooFewBits`] если `bits < 3`.
/// - [`DomainError::NotLargeEnough`] если `bits < 65` (по условию: > 2^64).
/// - [`DomainError::PrimeGenExhausted`] если за `max_tries` не нашлось простого.
pub fn generate_prime<R: RandomSource>(
    bits: u32,
    t: u32,
    max_tries: u32,
    rng: &mut R,
) -> Result<(BigUint, PrimeGenStats), DomainError> {
    if bits < 3 {
        return Err(DomainError::TooFewBits { min: 3, got: bits });
    }
    if bits < 65 {
        return Err(DomainError::NotLargeEnough { got: bits });
    }

    let mut stats = PrimeGenStats {
        iterations: 0,
        rejected_by_small_primes: 0,
        rejected_by_miller_rabin: 0,
    };

    for tries in 1..=max_tries {
        stats.iterations = tries;
        let mut p = rng.random_bits(bits);
        // Старший и младший биты = 1 (по методичке).
        p.set_bit(u64::from(bits - 1), true);
        p.set_bit(0, true);
        debug!(tries, bits, "сгенерирован кандидат p");

        if divisible_by_small_prime(&p) {
            stats.rejected_by_small_primes += 1;
            trace!(%p, "отсеян по малым простым");
            continue;
        }
        if !is_probably_prime(&p, t, rng) {
            stats.rejected_by_miller_rabin += 1;
            trace!(%p, "отсеян Рабином-Миллером");
            continue;
        }
        return Ok((p, stats));
    }

    warn!(max_tries, "не нашли простое за лимит попыток");
    Err(DomainError::PrimeGenExhausted { tries: max_tries })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::domain::rng::SeededRng;

    #[test]
    fn known_primes_pass_miller_rabin() {
        let mut rng = SeededRng::new(42);
        for &p in &[3u32, 5, 7, 11, 13, 97, 101, 1009] {
            assert!(
                is_probably_prime(&BigUint::from(p), 8, &mut rng),
                "Рабин-Миллер ошибочно отверг простое {p}"
            );
        }
    }

    #[test]
    fn known_composites_fail_miller_rabin() {
        let mut rng = SeededRng::new(42);
        for &n in &[4u32, 6, 8, 9, 15, 25, 91, 121, 561, 1001] {
            assert!(
                !is_probably_prime(&BigUint::from(n), 16, &mut rng),
                "Рабин-Миллер ошибочно принял составное {n}"
            );
        }
    }

    #[test]
    fn divisibility_small_primes() {
        assert!(divisible_by_small_prime(&BigUint::from(15u32)));
        assert!(divisible_by_small_prime(&BigUint::from(35u32)));
        assert!(!divisible_by_small_prime(&BigUint::from(2003u32))); // простое > 2000
        assert!(!divisible_by_small_prime(&BigUint::from(7u32))); // совпадает с простым из таблицы
    }

    #[test]
    fn decompose_works() {
        // 24 = 2^3 · 3
        assert_eq!(decompose(&BigUint::from(24u32)), (3, BigUint::from(3u32)));
        // 96 = 2^5 · 3
        assert_eq!(decompose(&BigUint::from(96u32)), (5, BigUint::from(3u32)));
        // 17 = 2^0 · 17
        assert_eq!(decompose(&BigUint::from(17u32)), (0, BigUint::from(17u32)));
    }

    #[test]
    fn generate_prime_65_bits_yields_real_prime() {
        // 65 бит — минимальный размер по условию (> 2^64).
        let mut rng = SeededRng::new(7);
        let (p, stats) = generate_prime(65, 8, 5_000, &mut rng).unwrap();
        assert!(p.bits() == 65, "получили {} бит вместо 65", p.bits());
        assert!(is_probably_prime(&p, 32, &mut rng));
        // Малое количество итераций — индикатор корректности.
        assert!(stats.iterations >= 1);
    }

    #[test]
    fn generate_prime_rejects_too_few_bits() {
        let mut rng = SeededRng::new(7);
        let err = generate_prime(64, 4, 100, &mut rng).unwrap_err();
        assert!(matches!(err, DomainError::NotLargeEnough { got: 64 }));
    }
}
