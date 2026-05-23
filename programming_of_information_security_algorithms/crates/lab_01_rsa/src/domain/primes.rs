//! Тестирование простоты по Миллеру-Рабину и генерация случайных простых чисел.

use tracing::{debug, info, trace};

use crate::domain::bigint::{self, BigUint, RandomSource, divrem, gcd, mod_pow, sub};

/// Небольшие простые — используем как быстрый отсев перед Миллером-Рабином.
const SMALL_PRIMES: &[u32] = &[
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
    101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193,
    197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307,
    311, 313, 317,
];

/// Тест Миллера-Рабина: возвращает `true`, если число *вероятно* простое.
///
/// `rounds` — количество раундов со случайным основанием. 20 даёт
/// вероятность ошибки ≤ 4^-20 ≈ 10^-12, чего более чем достаточно
/// для учебного RSA. Для `n < 318 665 857 834 031 151 167 461`
/// тест с свидетелями {2,3,5,7,11,13,17,19,23,29,31,37} детерминистичен.
pub fn is_probable_prime<R: RandomSource>(n: &BigUint, rounds: usize, rng: &mut R) -> bool {
    if n.bit_length() < 2 {
        // 0 и 1 — не простые.
        return false;
    }
    if n.is_one() {
        return false;
    }
    // Быстрый отсев по малым простым.
    for &p in SMALL_PRIMES {
        let bp = BigUint::from_u64(u64::from(p));
        if *n == bp {
            return true;
        }
        if divrem(n, &bp).1.is_zero() {
            trace!(divisor = p, "divisible by small prime");
            return false;
        }
    }

    // n - 1 = d · 2^s
    let one = BigUint::one();
    let two = BigUint::from_u64(2);
    let n_minus_one = sub(n, &one);
    let mut d = n_minus_one.clone();
    let mut s: u32 = 0;
    while d.is_even() {
        d = divrem(&d, &two).0;
        s += 1;
    }
    debug!(
        rounds,
        "Miller-Rabin starts with s={s}, d.bits={}",
        d.bit_length()
    );

    'rounds: for r in 0..rounds {
        // a ∈ [2, n - 2]. Берём rng-байт, приводим по модулю n-3 и сдвигаем.
        let n_minus_three = sub(&n_minus_one, &two);
        let a_raw = BigUint::random_with_exact_bits(n.bit_length(), rng);
        let a = bigint::add(&divrem(&a_raw, &n_minus_three).1, &two);

        let mut x = mod_pow(&a, &d, n);
        if x.is_one() || x == n_minus_one {
            trace!(round = r, "witness ok (x ∈ {{1, n-1}} immediately)");
            continue 'rounds;
        }
        for _ in 0..s - 1 {
            x = bigint::mul_mod(&x, &x, n);
            if x == n_minus_one {
                trace!(round = r, "witness ok after squaring");
                continue 'rounds;
            }
            if x.is_one() {
                trace!(round = r, "composite (x became 1 not via n-1)");
                return false;
            }
        }
        trace!(round = r, "composite witness");
        return false;
    }
    true
}

/// Генерирует случайное «вероятно простое» число с ровно `bits` значащими битами.
///
/// Сначала выставляет старший бит (длина) и младший бит (нечётность),
/// потом инкрементирует на 2, пока не пройдёт Миллер-Рабин.
pub fn generate_prime<R: RandomSource>(bits: usize, rng: &mut R) -> BigUint {
    assert!(bits >= 8, "слишком маленький размер простого (< 8 бит)");
    let mut tries: u64 = 0;
    loop {
        tries += 1;
        let mut candidate = BigUint::random_with_exact_bits(bits, rng);
        // Сделать нечётным.
        if candidate.is_even() {
            candidate = bigint::add(&candidate, &BigUint::one());
            // candidate теперь может иметь bit_length = bits или bits+1.
            if candidate.bit_length() > bits {
                continue;
            }
        }
        // Гарантируем, что второй с конца бит установлен — `n = p*q` тогда имеет
        // длину ровно `2*bits` бит (см. https://crypto.stackexchange.com/a/1812).
        let high_pair = (bits - 2).max(0);
        if !candidate.bit(high_pair) {
            // Установка бита не должна выходить за пределы.
            let two_to_high = {
                let mut t = BigUint::one();
                for _ in 0..high_pair {
                    t = bigint::add(&t, &t);
                }
                t
            };
            candidate = bigint::add(&candidate, &two_to_high);
        }

        let mut step: u32 = 0;
        loop {
            if candidate.bit_length() > bits {
                break; // переполнили размер — повторим попытку с нуля
            }
            // Проверка через 20 раундов Миллера-Рабина.
            if is_probable_prime(&candidate, 20, rng) {
                info!(bits = candidate.bit_length(), tries, step, "prime found");
                return candidate;
            }
            candidate = bigint::add(&candidate, &BigUint::from_u64(2));
            step += 1;
        }
    }
}

/// Проверка, что числа взаимно простые.
#[must_use]
pub fn is_coprime(a: &BigUint, b: &BigUint) -> bool {
    gcd(a, b).is_one()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::domain::rng::DeterministicRng;

    #[test]
    fn small_primes_are_recognized() {
        let mut rng = DeterministicRng::new(42);
        for p in [2u64, 3, 5, 7, 11, 13, 97, 257, 65537] {
            let n = BigUint::from_u64(p);
            assert!(is_probable_prime(&n, 8, &mut rng), "{p} should be prime");
        }
    }

    #[test]
    fn small_composites_are_rejected() {
        let mut rng = DeterministicRng::new(42);
        for c in [4u64, 9, 15, 21, 25, 100, 1024, 65535] {
            let n = BigUint::from_u64(c);
            assert!(
                !is_probable_prime(&n, 8, &mut rng),
                "{c} should be composite"
            );
        }
    }

    #[test]
    fn carmichael_561_is_rejected() {
        // 561 проходит Ферма для большинства оснований, но не Миллера-Рабина.
        let mut rng = DeterministicRng::new(123);
        let n = BigUint::from_u64(561);
        assert!(!is_probable_prime(&n, 16, &mut rng));
    }

    #[test]
    fn carmichael_8911_is_rejected() {
        let mut rng = DeterministicRng::new(7);
        let n = BigUint::from_u64(8911);
        assert!(!is_probable_prime(&n, 20, &mut rng));
    }

    #[test]
    fn generate_small_prime_returns_prime() {
        let mut rng = DeterministicRng::new(0xCAFE_BABE);
        let p = generate_prime(16, &mut rng);
        assert_eq!(p.bit_length(), 16);
        // Полноценная перепроверка.
        assert!(is_probable_prime(&p, 32, &mut rng));
    }

    #[test]
    fn is_coprime_basic() {
        assert!(is_coprime(&BigUint::from_u64(17), &BigUint::from_u64(31)));
        assert!(!is_coprime(&BigUint::from_u64(6), &BigUint::from_u64(9)));
    }
}
