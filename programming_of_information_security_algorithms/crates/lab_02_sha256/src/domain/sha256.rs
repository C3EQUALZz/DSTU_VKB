//! Реализация **SHA-2-256** строго по
//! [FIPS 180-4](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf).
//!
//! Условие лаб 2 запрещает сторонние библиотеки, выполняющие вычисление
//! хеш-функций — поэтому здесь только `core` + битовые операции.
//!
//! Инкрементальный API: `Sha256::new()` → `update(...)` → `finalize() -> [u8; 32]`.

/// Размер хеша в байтах (256 бит).
pub const DIGEST_BYTES: usize = 32;

/// Длина блока сообщения в байтах (512 бит).
pub const BLOCK_BYTES: usize = 64;

/// Начальные значения хеша (FIPS 180-4 §5.3.3) — старшие 32 бита дробных частей
/// квадратных корней первых восьми простых.
const H0: [u32; 8] = [
    0x6a09_e667,
    0xbb67_ae85,
    0x3c6e_f372,
    0xa54f_f53a,
    0x510e_527f,
    0x9b05_688c,
    0x1f83_d9ab,
    0x5be0_cd19,
];

/// Раундовые константы (FIPS 180-4 §4.2.2) — старшие 32 бита дробных частей
/// кубических корней первых 64 простых.
const K: [u32; 64] = [
    0x428a_2f98,
    0x7137_4491,
    0xb5c0_fbcf,
    0xe9b5_dba5,
    0x3956_c25b,
    0x59f1_11f1,
    0x923f_82a4,
    0xab1c_5ed5,
    0xd807_aa98,
    0x1283_5b01,
    0x2431_85be,
    0x550c_7dc3,
    0x72be_5d74,
    0x80de_b1fe,
    0x9bdc_06a7,
    0xc19b_f174,
    0xe49b_69c1,
    0xefbe_4786,
    0x0fc1_9dc6,
    0x240c_a1cc,
    0x2de9_2c6f,
    0x4a74_84aa,
    0x5cb0_a9dc,
    0x76f9_88da,
    0x983e_5152,
    0xa831_c66d,
    0xb003_27c8,
    0xbf59_7fc7,
    0xc6e0_0bf3,
    0xd5a7_9147,
    0x06ca_6351,
    0x1429_2967,
    0x27b7_0a85,
    0x2e1b_2138,
    0x4d2c_6dfc,
    0x5338_0d13,
    0x650a_7354,
    0x766a_0abb,
    0x81c2_c92e,
    0x9272_2c85,
    0xa2bf_e8a1,
    0xa81a_664b,
    0xc24b_8b70,
    0xc76c_51a3,
    0xd192_e819,
    0xd699_0624,
    0xf40e_3585,
    0x106a_a070,
    0x19a4_c116,
    0x1e37_6c08,
    0x2748_774c,
    0x34b0_bcb5,
    0x391c_0cb3,
    0x4ed8_aa4a,
    0x5b9c_ca4f,
    0x682e_6ff3,
    0x748f_82ee,
    0x78a5_636f,
    0x84c8_7814,
    0x8cc7_0208,
    0x90be_fffa,
    0xa450_6ceb,
    0xbef9_a3f7,
    0xc671_78f2,
];

#[inline]
const fn ch(x: u32, y: u32, z: u32) -> u32 {
    (x & y) ^ (!x & z)
}

#[inline]
const fn maj(x: u32, y: u32, z: u32) -> u32 {
    (x & y) ^ (x & z) ^ (y & z)
}

#[inline]
const fn big_sigma0(x: u32) -> u32 {
    x.rotate_right(2) ^ x.rotate_right(13) ^ x.rotate_right(22)
}

#[inline]
const fn big_sigma1(x: u32) -> u32 {
    x.rotate_right(6) ^ x.rotate_right(11) ^ x.rotate_right(25)
}

#[inline]
const fn small_sigma0(x: u32) -> u32 {
    x.rotate_right(7) ^ x.rotate_right(18) ^ (x >> 3)
}

#[inline]
const fn small_sigma1(x: u32) -> u32 {
    x.rotate_right(17) ^ x.rotate_right(19) ^ (x >> 10)
}

/// Стримовый SHA-256-хешер.
///
/// Использование:
/// ```
/// use lab_02_sha256::domain::sha256::Sha256;
/// let mut h = Sha256::new();
/// h.update(b"abc");
/// let digest = h.finalize();
/// ```
#[derive(Clone)]
pub struct Sha256 {
    state: [u32; 8],
    buffer: [u8; BLOCK_BYTES],
    buffer_len: usize,
    total_bits: u64,
}

impl Default for Sha256 {
    fn default() -> Self {
        Self::new()
    }
}

impl Sha256 {
    /// Новый хешер с начальными значениями FIPS 180-4 §5.3.3.
    #[must_use]
    pub const fn new() -> Self {
        Self {
            state: H0,
            buffer: [0; BLOCK_BYTES],
            buffer_len: 0,
            total_bits: 0,
        }
    }

    /// Подаёт следующий кусок сообщения. Можно вызывать сколько угодно раз.
    pub fn update(&mut self, mut data: &[u8]) {
        // Учёт длины — в битах, и здесь же ловим переполнение u64.
        self.total_bits = self
            .total_bits
            .checked_add((data.len() as u64) * 8)
            .expect("длина сообщения SHA-256 превысила 2^64 - 1 бит");

        // 1) Дозаполняем буфер до полного блока, если в нём уже что-то есть.
        if self.buffer_len > 0 {
            let need = BLOCK_BYTES - self.buffer_len;
            let take = need.min(data.len());
            self.buffer[self.buffer_len..self.buffer_len + take].copy_from_slice(&data[..take]);
            self.buffer_len += take;
            data = &data[take..];
            if self.buffer_len == BLOCK_BYTES {
                let block = self.buffer;
                self.process_block(&block);
                self.buffer_len = 0;
            }
        }

        // 2) Обрабатываем полные блоки напрямую из входа, минуя буфер.
        while data.len() >= BLOCK_BYTES {
            let (block, rest) = data.split_at(BLOCK_BYTES);
            let block_arr: &[u8; BLOCK_BYTES] = block.try_into().expect("split_at гарантирует");
            self.process_block(block_arr);
            data = rest;
        }

        // 3) Хвост — в буфер.
        if !data.is_empty() {
            self.buffer[..data.len()].copy_from_slice(data);
            self.buffer_len = data.len();
        }
    }

    /// Финализирует и возвращает 32-байтовый дайджест. Хешер далее непригоден.
    #[must_use]
    pub fn finalize(mut self) -> [u8; DIGEST_BYTES] {
        // Padding (FIPS 180-4 §5.1.1): добавить 0x80, затем нули, чтобы длина
        // блока, оставшаяся после длины-в-битах (8 байт), была кратна 64.
        let bits_before_len = self.buffer_len;
        self.buffer[bits_before_len] = 0x80;
        let idx = bits_before_len + 1;
        // Если до конца блока меньше 8 байт — текущий блок дополняем нулями
        // и обрабатываем, длину пишем уже в следующий блок.
        if idx > BLOCK_BYTES - 8 {
            for b in &mut self.buffer[idx..BLOCK_BYTES] {
                *b = 0;
            }
            let block = self.buffer;
            self.process_block(&block);
            // Под следующий (последний) блок — чистый буфер.
            self.buffer = [0u8; BLOCK_BYTES];
        } else {
            // В оставшейся части текущего блока всё, кроме хвоста под длину, — нули.
            for b in &mut self.buffer[idx..BLOCK_BYTES - 8] {
                *b = 0;
            }
        }
        // Длина в битах, big-endian, в последние 8 байт.
        self.buffer[BLOCK_BYTES - 8..].copy_from_slice(&self.total_bits.to_be_bytes());
        let block = self.buffer;
        self.process_block(&block);

        // Сериализация состояния.
        let mut out = [0u8; DIGEST_BYTES];
        for (i, word) in self.state.iter().enumerate() {
            out[i * 4..i * 4 + 4].copy_from_slice(&word.to_be_bytes());
        }
        out
    }

    fn process_block(&mut self, block: &[u8; BLOCK_BYTES]) {
        let mut w = [0u32; 64];
        // 1) Разбор блока в 16 u32 big-endian.
        for (i, chunk) in block.chunks_exact(4).enumerate() {
            w[i] = u32::from_be_bytes(chunk.try_into().expect("4-byte chunk"));
        }
        // 2) Расширение до 64 слов.
        for t in 16..64 {
            w[t] = small_sigma1(w[t - 2])
                .wrapping_add(w[t - 7])
                .wrapping_add(small_sigma0(w[t - 15]))
                .wrapping_add(w[t - 16]);
        }
        // 3) Основной цикл.
        let [mut a, mut b, mut c, mut d, mut e, mut f, mut g, mut h] = self.state;
        for t in 0..64 {
            let t1 = h
                .wrapping_add(big_sigma1(e))
                .wrapping_add(ch(e, f, g))
                .wrapping_add(K[t])
                .wrapping_add(w[t]);
            let t2 = big_sigma0(a).wrapping_add(maj(a, b, c));
            h = g;
            g = f;
            f = e;
            e = d.wrapping_add(t1);
            d = c;
            c = b;
            b = a;
            a = t1.wrapping_add(t2);
        }
        // 4) Накопление.
        self.state[0] = self.state[0].wrapping_add(a);
        self.state[1] = self.state[1].wrapping_add(b);
        self.state[2] = self.state[2].wrapping_add(c);
        self.state[3] = self.state[3].wrapping_add(d);
        self.state[4] = self.state[4].wrapping_add(e);
        self.state[5] = self.state[5].wrapping_add(f);
        self.state[6] = self.state[6].wrapping_add(g);
        self.state[7] = self.state[7].wrapping_add(h);
    }
}

/// Удобный однострочный API: `digest(b"abc") == hash("abc")`.
#[must_use]
pub fn digest(data: &[u8]) -> [u8; DIGEST_BYTES] {
    let mut h = Sha256::new();
    h.update(data);
    h.finalize()
}

/// Форматирует 32-байтовый дайджест в hex-lowercase (без префикса).
#[must_use]
pub fn to_hex(d: &[u8; DIGEST_BYTES]) -> String {
    use std::fmt::Write as _;
    let mut s = String::with_capacity(2 * DIGEST_BYTES);
    for b in d {
        write!(s, "{b:02x}").expect("write to String");
    }
    s
}

/// Парсит 32-байтовый дайджест из hex (любого регистра).
///
/// # Errors
/// — `Err(())` для неверной длины или недопустимых символов.
pub fn from_hex(s: &str) -> Result<[u8; DIGEST_BYTES], ParseDigestError> {
    let s = s.trim();
    if s.len() != 2 * DIGEST_BYTES {
        return Err(ParseDigestError::WrongLength {
            expected: 2 * DIGEST_BYTES,
            actual: s.len(),
        });
    }
    let mut out = [0u8; DIGEST_BYTES];
    for (i, byte_out) in out.iter_mut().enumerate() {
        let hi = hex_nibble(s.as_bytes()[i * 2])?;
        let lo = hex_nibble(s.as_bytes()[i * 2 + 1])?;
        *byte_out = (hi << 4) | lo;
    }
    Ok(out)
}

fn hex_nibble(b: u8) -> Result<u8, ParseDigestError> {
    match b {
        b'0'..=b'9' => Ok(b - b'0'),
        b'a'..=b'f' => Ok(b - b'a' + 10),
        b'A'..=b'F' => Ok(b - b'A' + 10),
        _ => Err(ParseDigestError::BadChar(b as char)),
    }
}

#[derive(Debug, thiserror::Error, PartialEq, Eq)]
pub enum ParseDigestError {
    #[error("ожидалось {expected} hex-символов, получено {actual}")]
    WrongLength { expected: usize, actual: usize },
    #[error("недопустимый символ {0:?}")]
    BadChar(char),
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Эталонные тестовые векторы NIST.
    /// Источник: FIPS 180-4 Annex B и публичная тестовая база CAVP.
    const VECTORS: &[(&str, &str)] = &[
        (
            "",
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        ),
        (
            "abc",
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
        ),
        (
            "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq",
            "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1",
        ),
    ];

    #[test]
    fn nist_test_vectors() {
        for (msg, expected) in VECTORS {
            let d = digest(msg.as_bytes());
            assert_eq!(to_hex(&d), *expected, "вход {msg:?}");
        }
    }

    /// Большой векторный тест из FIPS 180-4 Annex B: миллион символов 'a'.
    /// Эталон: `cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0`.
    #[test]
    fn one_million_a_single_shot() {
        let input = vec![b'a'; 1_000_000];
        let d = digest(&input);
        assert_eq!(
            to_hex(&d),
            "cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0"
        );
    }

    #[test]
    fn one_million_a_streamed_in_chunks() {
        let mut h = Sha256::new();
        let chunk = [b'a'; 1024];
        for _ in 0..(1_000_000 / chunk.len()) {
            h.update(&chunk);
        }
        let tail = 1_000_000 % chunk.len();
        h.update(&chunk[..tail]);
        let d = h.finalize();
        assert_eq!(
            to_hex(&d),
            "cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0"
        );
    }

    /// Реперный тест на 64-байтное входное сообщение (ровно один блок).
    /// Эталон взят из shasum -a 256 на 64 байтах 'a'.
    #[test]
    fn sixty_four_a_bytes() {
        let input = vec![b'a'; 64];
        let d = digest(&input);
        assert_eq!(
            to_hex(&d),
            "ffe054fe7ae0cb6dc65c3af9b61d5209f439851db43d0ba5997337df154668eb"
        );
    }

    #[test]
    fn streaming_matches_one_shot() {
        let input = b"The quick brown fox jumps over the lazy dog. Just testing 1234567890.";
        let one_shot = digest(input);
        // Подаём по одному байту.
        let mut h = Sha256::new();
        for b in input {
            h.update(std::slice::from_ref(b));
        }
        assert_eq!(h.finalize(), one_shot);
    }

    #[test]
    fn empty_input_yields_known_digest() {
        let d = digest(&[]);
        assert_eq!(
            to_hex(&d),
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        );
    }

    /// Сообщение длиной ровно 55 байт — крайний случай, когда длина-в-битах
    /// помещается в текущий блок без переноса в следующий.
    #[test]
    fn message_of_55_bytes() {
        let input = vec![0xAA; 55];
        // Эталон — собственная реализация в двух режимах.
        let one_shot = digest(&input);
        let mut h = Sha256::new();
        for b in &input {
            h.update(std::slice::from_ref(b));
        }
        assert_eq!(h.finalize(), one_shot);
    }

    /// Сообщение длиной ровно 56 байт — переключение на следующий блок.
    #[test]
    fn message_of_56_bytes() {
        let input = vec![0xBB; 56];
        let one_shot = digest(&input);
        let mut h = Sha256::new();
        for b in &input {
            h.update(std::slice::from_ref(b));
        }
        assert_eq!(h.finalize(), one_shot);
    }

    #[test]
    fn hex_round_trip() {
        let d = digest(b"hello");
        let hex = to_hex(&d);
        assert_eq!(from_hex(&hex).unwrap(), d);
        // Регистр не важен.
        assert_eq!(from_hex(&hex.to_uppercase()).unwrap(), d);
    }

    #[test]
    fn from_hex_rejects_bad_input() {
        assert!(matches!(
            from_hex("abc"),
            Err(ParseDigestError::WrongLength { .. })
        ));
        // 64 символа, но один недопустимый.
        let mut s = "0".repeat(64);
        s.replace_range(0..1, "g");
        assert!(matches!(from_hex(&s), Err(ParseDigestError::BadChar('g'))));
    }
}

#[cfg(test)]
mod property_tests {
    use proptest::prelude::*;

    use super::*;

    proptest! {
        /// Любая разбивка входа на куски даёт один и тот же хеш.
        #[test]
        fn streaming_equals_oneshot(
            data in proptest::collection::vec(any::<u8>(), 0..2048),
            split_points in proptest::collection::vec(0usize..2048, 0..20),
        ) {
            let one_shot = digest(&data);
            let mut h = Sha256::new();
            let mut prev = 0;
            let mut points: Vec<usize> = split_points
                .into_iter()
                .map(|p| p.min(data.len()))
                .collect();
            points.sort_unstable();
            for p in &points {
                if *p > prev {
                    h.update(&data[prev..*p]);
                    prev = *p;
                }
            }
            h.update(&data[prev..]);
            prop_assert_eq!(h.finalize(), one_shot);
        }

        /// Длина дайджеста всегда 32 байта.
        #[test]
        fn digest_is_32_bytes(data in proptest::collection::vec(any::<u8>(), 0..4096)) {
            let d = digest(&data);
            prop_assert_eq!(d.len(), 32);
        }

        /// Hex round-trip.
        #[test]
        fn hex_round_trips(data in proptest::collection::vec(any::<u8>(), 0..128)) {
            let d = digest(&data);
            let hex = to_hex(&d);
            prop_assert_eq!(hex.len(), 64);
            prop_assert_eq!(from_hex(&hex).unwrap(), d);
        }
    }
}
