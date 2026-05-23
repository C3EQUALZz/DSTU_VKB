//! Абстракция источника случайности.
//!
//! Domain зависит только от этого trait; конкретный backend (ChaCha20, OsRng)
//! инжектится из presentation/application.

use num_bigint::BigUint;

/// Источник случайных больших чисел.
///
/// Реализации не должны блокироваться на длинных вычислениях; для тестов
/// можно использовать [`SeededRng`].
pub trait RandomSource {
    /// Случайное число ровно из `bits` бит (старший бит = 1).
    fn random_bits(&mut self, bits: u32) -> BigUint;

    /// Случайное число в диапазоне `[low; high)` (low включительно, high исключительно).
    fn random_range(&mut self, low: &BigUint, high: &BigUint) -> BigUint;
}

/// Детерминированный RNG для тестов и воспроизводимых демонстраций.
pub struct SeededRng {
    inner: rand_chacha::ChaCha20Rng,
}

impl SeededRng {
    pub fn new(seed: u64) -> Self {
        use rand::SeedableRng;
        Self {
            inner: rand_chacha::ChaCha20Rng::seed_from_u64(seed),
        }
    }

    pub fn from_entropy() -> Self {
        use rand::SeedableRng;
        Self {
            inner: rand_chacha::ChaCha20Rng::from_entropy(),
        }
    }
}

impl RandomSource for SeededRng {
    fn random_bits(&mut self, bits: u32) -> BigUint {
        use num_bigint::RandBigInt;
        // Случайное число ровно bits бит: гарантируем старший бит = 1.
        let mut n = self.inner.gen_biguint(u64::from(bits));
        // Установить старший бит:
        n.set_bit(u64::from(bits - 1), true);
        n
    }

    fn random_range(&mut self, low: &BigUint, high: &BigUint) -> BigUint {
        use num_bigint::RandBigInt;
        self.inner.gen_biguint_range(low, high)
    }
}
