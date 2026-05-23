//! Источники случайных байт для RSA.
//!
//! Никаких сторонних `rand` крейтов — на Unix читаем `/dev/urandom`.
//! Для тестов есть детерминированный xorshift.

use std::fs::File;
use std::io::Read;

use thiserror::Error;
use tracing::debug;

use crate::domain::bigint::RandomSource;

#[derive(Debug, Error)]
pub enum RngError {
    #[error("не удалось открыть /dev/urandom: {0}")]
    Open(#[source] std::io::Error),
    #[error("не удалось прочитать из /dev/urandom: {0}")]
    Read(#[source] std::io::Error),
}

/// Безопасный системный RNG. Открывает `/dev/urandom` лениво при первом
/// обращении и держит файл открытым до конца программы.
pub struct OsRng {
    file: File,
}

impl OsRng {
    /// Открывает `/dev/urandom`.
    ///
    /// # Errors
    /// Если устройство недоступно (нестандартная среда, sandbox).
    pub fn new() -> Result<Self, RngError> {
        let file = File::open("/dev/urandom").map_err(RngError::Open)?;
        debug!("opened /dev/urandom as system RNG");
        Ok(Self { file })
    }
}

impl RandomSource for OsRng {
    fn fill(&mut self, buf: &mut [u8]) {
        // /dev/urandom не блокируется и не возвращает короткие чтения для
        // запросов разумного размера, но всё равно читаем циклом.
        let mut filled = 0;
        while filled < buf.len() {
            let n = self
                .file
                .read(&mut buf[filled..])
                .expect("чтение из /dev/urandom");
            assert!(n > 0, "/dev/urandom вернул 0 байт");
            filled += n;
        }
    }
}

/// Детерминированный xorshift64* RNG для unit-тестов.
/// **Не использовать в проде** — не криптостойкий.
pub struct DeterministicRng {
    state: u64,
}

impl DeterministicRng {
    #[must_use]
    pub const fn new(seed: u64) -> Self {
        Self {
            // 0 — фиксированная точка для xorshift, заменяем.
            state: if seed == 0 {
                0xDEAD_BEEF_CAFE_BABE
            } else {
                seed
            },
        }
    }

    fn next_u64(&mut self) -> u64 {
        let mut x = self.state;
        x ^= x << 13;
        x ^= x >> 7;
        x ^= x << 17;
        self.state = x;
        x.wrapping_mul(0x2545_F491_4F6C_DD1D)
    }
}

impl RandomSource for DeterministicRng {
    fn fill(&mut self, buf: &mut [u8]) {
        let mut i = 0;
        while i < buf.len() {
            let v = self.next_u64().to_le_bytes();
            let take = (buf.len() - i).min(8);
            buf[i..i + take].copy_from_slice(&v[..take]);
            i += take;
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn deterministic_rng_is_reproducible() {
        let mut a = DeterministicRng::new(42);
        let mut b = DeterministicRng::new(42);
        let mut buf_a = [0u8; 32];
        let mut buf_b = [0u8; 32];
        a.fill(&mut buf_a);
        b.fill(&mut buf_b);
        assert_eq!(buf_a, buf_b);
    }

    #[test]
    fn deterministic_rng_varies_by_seed() {
        let mut a = DeterministicRng::new(1);
        let mut b = DeterministicRng::new(2);
        let mut buf_a = [0u8; 16];
        let mut buf_b = [0u8; 16];
        a.fill(&mut buf_a);
        b.fill(&mut buf_b);
        assert_ne!(buf_a, buf_b);
    }

    #[test]
    fn os_rng_provides_non_zero_bytes() {
        let mut rng = OsRng::new().expect("на любой Unix-системе есть /dev/urandom");
        let mut buf = [0u8; 64];
        rng.fill(&mut buf);
        assert!(buf.iter().any(|&b| b != 0), "OsRng вернул только нули");
    }
}
