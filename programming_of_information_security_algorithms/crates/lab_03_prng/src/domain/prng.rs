//! Генератор псевдо-датчик случайных чисел (ПДСЧ).
//!
//! Алгоритм — **xorshift64\*** Marsaglia (2003): три xorshift'а + финальное
//! умножение на нечётную константу. Период `2^64 − 1`, скорость — несколько
//! циклов на 64-битное значение, прост в анализе и стабилен между версиями
//! компилятора. Не криптостойкий — по 2–3 последовательным выходам легко
//! восстанавливается состояние, поэтому для шифрования он не годится, но
//! полностью покрывает требования лаб 3 (≥ 200 значений, прогон через NIST STS).
//!
//! Плюсы / минусы подробно — в `docs/explanations/lab_03_prng/README.md`.

/// Магическая константа из работы Marsaglia (2003), «An experimental
/// exploration of Marsaglia's xorshift generators, scrambled».
const SCRAMBLE_MULTIPLIER: u64 = 0x2545_F491_4F6C_DD1D;

/// `0` — фиксированная точка xorshift'а, поэтому заменяется на запасной seed.
const SEED_FALLBACK: u64 = 0xDEAD_BEEF_CAFE_BABE;

/// 64-битный PRNG.
#[derive(Debug, Clone, Copy)]
pub struct Xorshift64Star {
    state: u64,
}

impl Xorshift64Star {
    /// Создаёт генератор. Если `seed == 0`, используется
    /// детерминированный «запасной» seed (`0xDEAD_BEEF_CAFE_BABE`), потому что
    /// иначе xorshift зациклится на нуле.
    #[must_use]
    pub const fn new(seed: u64) -> Self {
        Self {
            state: if seed == 0 { SEED_FALLBACK } else { seed },
        }
    }

    /// Выдаёт следующее 64-битное число.
    #[allow(clippy::should_implement_trait)] // мы намеренно не Iterator
    pub fn next_u64(&mut self) -> u64 {
        let mut x = self.state;
        x ^= x << 13;
        x ^= x >> 7;
        x ^= x << 17;
        self.state = x;
        x.wrapping_mul(SCRAMBLE_MULTIPLIER)
    }

    /// Заполняет буфер сгенерированными байтами (little-endian внутри слова).
    pub fn fill_bytes(&mut self, buf: &mut [u8]) {
        let mut i = 0;
        while i < buf.len() {
            let v = self.next_u64().to_le_bytes();
            let take = (buf.len() - i).min(8);
            buf[i..i + take].copy_from_slice(&v[..take]);
            i += take;
        }
    }
}

/// Сгенерированная последовательность: `count` 64-битных значений
/// + удобные представления.
#[derive(Debug, Clone)]
pub struct Sequence {
    pub seed: u64,
    pub words: Vec<u64>,
}

impl Sequence {
    /// Сколько 64-битных значений в последовательности.
    #[must_use]
    pub fn word_count(&self) -> usize {
        self.words.len()
    }

    /// Сколько бит всего.
    #[must_use]
    pub fn bit_count(&self) -> usize {
        self.words.len() * 64
    }

    /// Бинарное представление: каждое слово в big-endian 8 байт.
    #[must_use]
    pub fn to_binary_be(&self) -> Vec<u8> {
        let mut out = Vec::with_capacity(self.words.len() * 8);
        for w in &self.words {
            out.extend_from_slice(&w.to_be_bytes());
        }
        out
    }

    /// ASCII-битовый поток: '0'/'1', старший бит каждого u64 первым.
    /// Это формат, который ест NIST STS в режиме `0 — ASCII`.
    #[must_use]
    pub fn to_ascii_bits(&self) -> String {
        let mut s = String::with_capacity(self.words.len() * 64);
        for w in &self.words {
            for i in (0..64).rev() {
                s.push(if (*w >> i) & 1 == 1 { '1' } else { '0' });
            }
        }
        s
    }
}

/// Создаёт `count` значений на основе seed.
#[must_use]
pub fn generate(seed: u64, count: usize) -> Sequence {
    let mut rng = Xorshift64Star::new(seed);
    let mut words = Vec::with_capacity(count);
    for _ in 0..count {
        words.push(rng.next_u64());
    }
    Sequence { seed, words }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn same_seed_yields_same_sequence() {
        let a = generate(42, 200);
        let b = generate(42, 200);
        assert_eq!(a.words, b.words);
    }

    #[test]
    fn different_seeds_diverge_quickly() {
        let a = generate(1, 32);
        let b = generate(2, 32);
        // На разном seed первое же значение должно отличаться.
        assert_ne!(a.words[0], b.words[0]);
    }

    #[test]
    fn zero_seed_is_replaced_with_fallback() {
        // generate(0, …) не должно зацикливаться на нуле.
        let s = generate(0, 16);
        assert!(s.words.iter().any(|&w| w != 0));
    }

    #[test]
    fn binary_representation_has_expected_length() {
        let s = generate(0xCAFE, 200);
        let bin = s.to_binary_be();
        assert_eq!(bin.len(), 200 * 8);
    }

    #[test]
    fn ascii_representation_has_expected_length_and_alphabet() {
        let s = generate(0xCAFE, 200);
        let ascii = s.to_ascii_bits();
        assert_eq!(ascii.len(), 200 * 64);
        assert!(ascii.chars().all(|c| c == '0' || c == '1'));
    }

    #[test]
    fn ascii_matches_binary_bitwise() {
        let s = generate(0xBEEF, 50);
        let bin = s.to_binary_be();
        let ascii = s.to_ascii_bits();
        for (i, byte) in bin.iter().enumerate() {
            for bit in 0..8 {
                let expected = (byte >> (7 - bit)) & 1;
                let got = ascii.as_bytes()[i * 8 + bit] - b'0';
                assert_eq!(got, expected, "несовпадение бита {i}.{bit}");
            }
        }
    }

    /// На 12 800 битах от хорошего PRNG ожидаем число единиц в пределах
    /// ~50% ± 3σ. Простая «sanity check», не криптостатистика.
    #[test]
    fn ones_ratio_is_near_half_on_12800_bits() {
        let s = generate(0xDEAD_BEEF_CAFE_BABE, 200);
        let ones = s.to_ascii_bits().chars().filter(|&c| c == '1').count();
        let n = s.bit_count();
        // 3σ для биномиального p=0.5 на n=12800 ≈ 169.7
        let lo = (n / 2).saturating_sub(180);
        let hi = (n / 2) + 180;
        assert!(
            (lo..=hi).contains(&ones),
            "ones = {ones} вне диапазона [{lo}; {hi}] для n = {n}"
        );
    }

    #[test]
    fn fill_bytes_round_trips_with_next_u64() {
        let mut a = Xorshift64Star::new(7);
        let mut b = Xorshift64Star::new(7);
        let mut buf = [0u8; 16];
        a.fill_bytes(&mut buf);
        let expected = [b.next_u64().to_le_bytes(), b.next_u64().to_le_bytes()];
        let mut concat = [0u8; 16];
        concat[..8].copy_from_slice(&expected[0]);
        concat[8..].copy_from_slice(&expected[1]);
        assert_eq!(buf, concat);
    }
}

#[cfg(test)]
mod property_tests {
    use proptest::prelude::*;

    use super::*;

    proptest! {
        #[test]
        fn same_seed_property(seed: u64, count in 1usize..1000) {
            let a = generate(seed, count);
            let b = generate(seed, count);
            prop_assert_eq!(a.words, b.words);
        }

        #[test]
        fn ascii_and_binary_are_consistent(seed: u64, count in 1usize..200) {
            let s = generate(seed, count);
            let bin = s.to_binary_be();
            let ascii = s.to_ascii_bits();
            prop_assert_eq!(ascii.len(), bin.len() * 8);
            for (i, byte) in bin.iter().enumerate() {
                for bit in 0..8 {
                    let expected = (byte >> (7 - bit)) & 1;
                    let got = ascii.as_bytes()[i * 8 + bit] - b'0';
                    prop_assert_eq!(got, expected);
                }
            }
        }
    }
}
