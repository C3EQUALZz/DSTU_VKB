//! Беззнаковая длинная арифметика для RSA.
//!
//! Хранение: little-endian вектор 32-битных limb'ов. Все операции пишутся
//! «руками» — стандарт условия запрещает сторонние криптографические
//! и числовые библиотеки (`num-bigint`, `rsa`, `num-prime` и т.п.).
//!
//! Реализованы только те операции, которые реально нужны RSA: сложение,
//! вычитание (`self ≥ other`), умножение, длинное деление, модульное
//! возведение в степень, расширенный алгоритм Евклида и обратный по модулю.
//! Скорость намеренно не «production»-уровня (`O(n^2)` для mul, побитное
//! длинное деление) — для учебного 1024-битного RSA этого достаточно.

use std::cmp::Ordering;
use std::fmt;

use thiserror::Error;

/// Беззнаковое длинное число.
#[derive(Clone, Debug, Default, PartialEq, Eq, Hash)]
pub struct BigUint {
    /// little-endian, ведущие нулевые limbs не хранятся; ноль — пустой вектор.
    limbs: Vec<u32>,
}

#[derive(Debug, Error, PartialEq, Eq)]
pub enum ParseError {
    #[error("пустая строка")]
    Empty,
    #[error("недопустимый символ {ch:?} в позиции {pos}")]
    BadChar { ch: char, pos: usize },
}

impl BigUint {
    #[must_use]
    pub const fn zero() -> Self {
        Self { limbs: Vec::new() }
    }

    #[must_use]
    pub fn one() -> Self {
        Self { limbs: vec![1] }
    }

    #[must_use]
    pub fn from_u64(v: u64) -> Self {
        let mut limbs = Vec::with_capacity(2);
        if (v & 0xFFFF_FFFF) != 0 || v != 0 {
            limbs.push(v as u32);
        }
        let high = (v >> 32) as u32;
        if high != 0 {
            limbs.push(high);
        }
        let mut n = Self { limbs };
        n.trim();
        n
    }

    /// Big-endian байты → BigUint.
    #[must_use]
    pub fn from_bytes_be(bytes: &[u8]) -> Self {
        let mut limbs: Vec<u32> = Vec::with_capacity(bytes.len().div_ceil(4));
        // Группируем по 4 байта с конца — младшие limbs первыми.
        let mut i = bytes.len();
        while i > 0 {
            let start = i.saturating_sub(4);
            let len = i - start;
            let mut chunk = [0u8; 4];
            chunk[4 - len..].copy_from_slice(&bytes[start..i]);
            limbs.push(u32::from_be_bytes(chunk));
            i = start;
        }
        let mut n = Self { limbs };
        n.trim();
        n
    }

    /// BigUint → big-endian байты длины не менее `min_len` (слева добиваются
    /// нулями). Полезно, когда RSA-блок должен иметь фиксированную длину
    /// в байтах модуля `n`.
    #[must_use]
    pub fn to_bytes_be(&self, min_len: usize) -> Vec<u8> {
        if self.is_zero() {
            return vec![0; min_len];
        }
        let mut bytes = Vec::with_capacity(self.limbs.len() * 4);
        for &limb in self.limbs.iter().rev() {
            bytes.extend_from_slice(&limb.to_be_bytes());
        }
        // Срезать ведущие нули.
        let leading = bytes.iter().position(|&b| b != 0).unwrap_or(bytes.len());
        let mut out = bytes[leading..].to_vec();
        if out.len() < min_len {
            let mut pad = vec![0u8; min_len - out.len()];
            pad.extend_from_slice(&out);
            out = pad;
        }
        out
    }

    /// Парсит число из десятичной или 16-ричной (с префиксом `0x`/`0X`) строки.
    ///
    /// # Errors
    /// — `ParseError::Empty` для пустой строки;
    /// — `ParseError::BadChar` для недопустимого символа.
    pub fn parse(s: &str) -> Result<Self, ParseError> {
        if s.is_empty() {
            return Err(ParseError::Empty);
        }
        let (base, body) = if let Some(b) = s.strip_prefix("0x").or_else(|| s.strip_prefix("0X")) {
            (16u32, b)
        } else {
            (10u32, s)
        };
        let mut n = Self::zero();
        let mut had = false;
        for (pos, ch) in body.char_indices() {
            if ch == '_' {
                continue;
            }
            let d = ch.to_digit(base).ok_or(ParseError::BadChar { ch, pos })?;
            n.mul_small_in_place(base);
            n.add_small_in_place(d);
            had = true;
        }
        if !had {
            return Err(ParseError::Empty);
        }
        Ok(n)
    }

    /// Шестнадцатеричное представление без префикса, lowercase, без ведущих нулей.
    /// Ноль — строка `"0"`.
    #[must_use]
    pub fn to_hex(&self) -> String {
        use std::fmt::Write as _;
        if self.is_zero() {
            return "0".into();
        }
        let mut s = String::with_capacity(self.limbs.len() * 8);
        let (top, rest) = self.limbs.split_last().expect("limbs not empty");
        // Старший limb — без выравнивания нулями (так короче).
        write!(s, "{top:x}").expect("write to String");
        for limb in rest.iter().rev() {
            write!(s, "{limb:08x}").expect("write to String");
        }
        s
    }

    #[must_use]
    pub fn is_zero(&self) -> bool {
        self.limbs.is_empty()
    }

    #[must_use]
    pub fn is_one(&self) -> bool {
        self.limbs == [1]
    }

    #[must_use]
    pub fn is_even(&self) -> bool {
        self.limbs.first().is_none_or(|l| l & 1 == 0)
    }

    /// Количество значащих битов; 0 для нуля.
    #[must_use]
    pub fn bit_length(&self) -> usize {
        match self.limbs.last() {
            None => 0,
            Some(top) => self.limbs.len() * 32 - (top.leading_zeros() as usize),
        }
    }

    /// Прочитать бит с индексом `i` (0 — младший).
    #[must_use]
    pub fn bit(&self, i: usize) -> bool {
        let limb_idx = i / 32;
        if limb_idx >= self.limbs.len() {
            return false;
        }
        (self.limbs[limb_idx] >> (i % 32)) & 1 == 1
    }

    fn set_bit(&mut self, i: usize) {
        let limb_idx = i / 32;
        while self.limbs.len() <= limb_idx {
            self.limbs.push(0);
        }
        self.limbs[limb_idx] |= 1u32 << (i % 32);
    }

    fn trim(&mut self) {
        while self.limbs.last() == Some(&0) {
            self.limbs.pop();
        }
    }

    fn add_small_in_place(&mut self, k: u32) {
        if k == 0 {
            return;
        }
        let mut carry = u64::from(k);
        for limb in &mut self.limbs {
            let v = u64::from(*limb) + carry;
            *limb = v as u32;
            carry = v >> 32;
            if carry == 0 {
                return;
            }
        }
        if carry != 0 {
            self.limbs.push(carry as u32);
        }
    }

    fn mul_small_in_place(&mut self, k: u32) {
        if k == 0 {
            self.limbs.clear();
            return;
        }
        if k == 1 || self.limbs.is_empty() {
            return;
        }
        let mut carry: u64 = 0;
        for limb in &mut self.limbs {
            let v = u64::from(*limb) * u64::from(k) + carry;
            *limb = v as u32;
            carry = v >> 32;
        }
        while carry > 0 {
            self.limbs.push(carry as u32);
            carry >>= 32;
        }
    }

    fn shl_in_place(&mut self, n: usize) {
        if n == 0 || self.is_zero() {
            return;
        }
        let limb_shift = n / 32;
        let bit_shift = n % 32;
        if bit_shift == 0 {
            let mut new_limbs = vec![0u32; limb_shift];
            new_limbs.extend_from_slice(&self.limbs);
            self.limbs = new_limbs;
            return;
        }
        let mut new_limbs = vec![0u32; self.limbs.len() + limb_shift + 1];
        let mut carry: u64 = 0;
        for (i, &limb) in self.limbs.iter().enumerate() {
            let v = (u64::from(limb) << bit_shift) | carry;
            new_limbs[i + limb_shift] = v as u32;
            carry = v >> 32;
        }
        new_limbs[self.limbs.len() + limb_shift] = carry as u32;
        self.limbs = new_limbs;
        self.trim();
    }

    /// Случайное число длиной ровно `bits` бит (старший бит установлен).
    #[must_use]
    pub fn random_with_exact_bits<R: RandomSource>(bits: usize, rng: &mut R) -> Self {
        assert!(bits > 0, "bits must be > 0");
        let limbs_count = bits.div_ceil(32);
        let mut limbs = vec![0u32; limbs_count];
        rng.fill_u32(&mut limbs);
        let extra = limbs_count * 32 - bits;
        if extra > 0 {
            let mask = u32::MAX >> extra;
            limbs[limbs_count - 1] &= mask;
        }
        // Установить старший бит, чтобы длина была ровно `bits`.
        let top_bit_index_in_top_limb = (bits - 1) % 32;
        limbs[limbs_count - 1] |= 1u32 << top_bit_index_in_top_limb;
        let mut n = Self { limbs };
        n.trim();
        n
    }
}

impl Ord for BigUint {
    fn cmp(&self, other: &Self) -> Ordering {
        match self.limbs.len().cmp(&other.limbs.len()) {
            Ordering::Equal => self.limbs.iter().rev().cmp(other.limbs.iter().rev()),
            ord => ord,
        }
    }
}

impl PartialOrd for BigUint {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl fmt::Display for BigUint {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        if self.is_zero() {
            return f.write_str("0");
        }
        // Десятичный вывод через повторное деление на 10^9.
        const CHUNK: u32 = 1_000_000_000;
        let mut tmp = self.clone();
        let mut chunks: Vec<u32> = Vec::new();
        while !tmp.is_zero() {
            let rem = tmp.div_small_in_place(CHUNK);
            chunks.push(rem);
        }
        let (last, rest) = chunks
            .split_last()
            .expect("non-zero число имеет хотя бы один chunk");
        write!(f, "{last}")?;
        for c in rest.iter().rev() {
            write!(f, "{c:09}")?;
        }
        Ok(())
    }
}

impl BigUint {
    /// `self /= k`, возвращает остаток.
    fn div_small_in_place(&mut self, k: u32) -> u32 {
        debug_assert!(k != 0);
        let mut rem: u64 = 0;
        for limb in self.limbs.iter_mut().rev() {
            let cur = (rem << 32) | u64::from(*limb);
            *limb = (cur / u64::from(k)) as u32;
            rem = cur % u64::from(k);
        }
        self.trim();
        rem as u32
    }
}

// ───── арифметические операции ─────

#[must_use]
pub fn add(a: &BigUint, b: &BigUint) -> BigUint {
    let n = a.limbs.len().max(b.limbs.len());
    let mut limbs = Vec::with_capacity(n + 1);
    let mut carry: u64 = 0;
    for i in 0..n {
        let x = u64::from(a.limbs.get(i).copied().unwrap_or(0));
        let y = u64::from(b.limbs.get(i).copied().unwrap_or(0));
        let s = x + y + carry;
        limbs.push(s as u32);
        carry = s >> 32;
    }
    if carry != 0 {
        limbs.push(carry as u32);
    }
    let mut r = BigUint { limbs };
    r.trim();
    r
}

/// `a - b`. Требует `a ≥ b`, иначе паника.
#[must_use]
pub fn sub(a: &BigUint, b: &BigUint) -> BigUint {
    assert!(a >= b, "sub: a < b");
    let mut limbs = Vec::with_capacity(a.limbs.len());
    let mut borrow: i64 = 0;
    for i in 0..a.limbs.len() {
        let x = i64::from(a.limbs[i]);
        let y = i64::from(b.limbs.get(i).copied().unwrap_or(0));
        let mut diff = x - y - borrow;
        if diff < 0 {
            diff += 1i64 << 32;
            borrow = 1;
        } else {
            borrow = 0;
        }
        limbs.push(diff as u32);
    }
    debug_assert_eq!(borrow, 0);
    let mut r = BigUint { limbs };
    r.trim();
    r
}

#[must_use]
pub fn mul(a: &BigUint, b: &BigUint) -> BigUint {
    if a.is_zero() || b.is_zero() {
        return BigUint::zero();
    }
    let mut limbs = vec![0u32; a.limbs.len() + b.limbs.len()];
    for i in 0..a.limbs.len() {
        let mut carry: u64 = 0;
        let ai = u64::from(a.limbs[i]);
        for j in 0..b.limbs.len() {
            let cur = u64::from(limbs[i + j]) + ai * u64::from(b.limbs[j]) + carry;
            limbs[i + j] = cur as u32;
            carry = cur >> 32;
        }
        if carry != 0 {
            let mut k = i + b.limbs.len();
            while carry != 0 {
                let cur = u64::from(limbs[k]) + carry;
                limbs[k] = cur as u32;
                carry = cur >> 32;
                k += 1;
            }
        }
    }
    let mut r = BigUint { limbs };
    r.trim();
    r
}

/// Длинное деление `a` на `b`. Возвращает `(частное, остаток)`. Паника при `b == 0`.
#[must_use]
pub fn divrem(a: &BigUint, b: &BigUint) -> (BigUint, BigUint) {
    assert!(!b.is_zero(), "деление на 0");
    if a < b {
        return (BigUint::zero(), a.clone());
    }
    let n = a.bit_length();
    let mut q = BigUint::zero();
    let mut r = BigUint::zero();
    for i in (0..n).rev() {
        // r <<= 1
        r.shl_in_place(1);
        if a.bit(i) {
            r.set_bit(0);
        }
        if r >= *b {
            r = sub(&r, b);
            q.set_bit(i);
        }
    }
    q.trim();
    r.trim();
    (q, r)
}

/// `(a * b) mod m`. Стандартная реализация — `mul` затем `divrem`.
#[must_use]
pub fn mul_mod(a: &BigUint, b: &BigUint, m: &BigUint) -> BigUint {
    divrem(&mul(a, b), m).1
}

/// `base ^ exp mod m` методом left-to-right binary exponentiation.
#[must_use]
pub fn mod_pow(base: &BigUint, exp: &BigUint, m: &BigUint) -> BigUint {
    assert!(!m.is_zero(), "modulus = 0");
    if m.is_one() {
        return BigUint::zero();
    }
    let mut result = BigUint::one();
    let mut b = divrem(base, m).1;
    let bits = exp.bit_length();
    for i in 0..bits {
        if exp.bit(i) {
            result = mul_mod(&result, &b, m);
        }
        b = mul_mod(&b, &b, m);
    }
    result
}

/// НОД через классический алгоритм Евклида.
#[must_use]
pub fn gcd(a: &BigUint, b: &BigUint) -> BigUint {
    let mut x = a.clone();
    let mut y = b.clone();
    while !y.is_zero() {
        let r = divrem(&x, &y).1;
        x = y;
        y = r;
    }
    x
}

/// Знаковое число для расширенного Евклида.
/// Внутренний тип — наружу не выставляется.
#[derive(Clone, Debug, PartialEq, Eq)]
struct SignedBig {
    negative: bool,
    mag: BigUint,
}

impl SignedBig {
    fn zero() -> Self {
        Self {
            negative: false,
            mag: BigUint::zero(),
        }
    }
    fn pos(mag: BigUint) -> Self {
        Self {
            negative: false,
            mag,
        }
    }
    fn from_u64(v: u64) -> Self {
        Self::pos(BigUint::from_u64(v))
    }
    fn is_zero(&self) -> bool {
        self.mag.is_zero()
    }
    fn neg(&self) -> Self {
        if self.is_zero() {
            self.clone()
        } else {
            Self {
                negative: !self.negative,
                mag: self.mag.clone(),
            }
        }
    }
    fn add(&self, other: &Self) -> Self {
        if self.negative == other.negative {
            return Self {
                negative: self.negative && !self.is_zero(),
                mag: add(&self.mag, &other.mag),
            };
        }
        match self.mag.cmp(&other.mag) {
            Ordering::Equal => Self::zero(),
            Ordering::Greater => Self {
                negative: self.negative,
                mag: sub(&self.mag, &other.mag),
            },
            Ordering::Less => Self {
                negative: other.negative,
                mag: sub(&other.mag, &self.mag),
            },
        }
    }
    fn sub(&self, other: &Self) -> Self {
        self.add(&other.neg())
    }
    fn mul_unsigned(&self, k: &BigUint) -> Self {
        if k.is_zero() {
            return Self::zero();
        }
        Self {
            negative: self.negative,
            mag: mul(&self.mag, k),
        }
    }
}

/// Расширенный алгоритм Евклида.
///
/// Возвращает `(g, x, y)` такие, что `a*x + b*y = g`, где `g = gcd(a, b)`.
/// `x` и `y` могут быть отрицательными — для удобства возвращается
/// каноническая форма `x mod m` отдельно через [`mod_inverse`].
#[must_use]
fn ext_gcd_signed(a: &BigUint, b: &BigUint) -> (BigUint, SignedBig, SignedBig) {
    // Итеративный алгоритм. См. https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    let mut old_r = a.clone();
    let mut r = b.clone();
    let mut old_s = SignedBig::from_u64(1);
    let mut s = SignedBig::zero();
    let mut old_t = SignedBig::zero();
    let mut t = SignedBig::from_u64(1);

    while !r.is_zero() {
        let (q, new_r) = divrem(&old_r, &r);
        old_r = r;
        r = new_r;

        let new_s = old_s.sub(&s.mul_unsigned(&q));
        old_s = s;
        s = new_s;

        let new_t = old_t.sub(&t.mul_unsigned(&q));
        old_t = t;
        t = new_t;
    }
    (old_r, old_s, old_t)
}

/// Обратный по модулю: возвращает `x` такой, что `a*x ≡ 1 (mod m)`.
///
/// Возвращает `None`, если `gcd(a, m) != 1`.
#[must_use]
pub fn mod_inverse(a: &BigUint, m: &BigUint) -> Option<BigUint> {
    let (g, x_signed, _) = ext_gcd_signed(a, m);
    if !g.is_one() {
        return None;
    }
    // Приводим x в диапазон [0, m).
    let reduced = if x_signed.negative {
        let q = divrem(&x_signed.mag, m);
        // x_signed = -mag; mag mod m = q.1; результат = m - (mag mod m) если q.1 != 0
        if q.1.is_zero() {
            BigUint::zero()
        } else {
            sub(m, &q.1)
        }
    } else {
        divrem(&x_signed.mag, m).1
    };
    Some(reduced)
}

// ───── источник случайных байт ─────

/// Поставщик случайных байт для алгоритмов RSA.
pub trait RandomSource {
    fn fill(&mut self, buf: &mut [u8]);

    fn fill_u32(&mut self, out: &mut [u32]) {
        let mut bytes = vec![0u8; out.len() * 4];
        self.fill(&mut bytes);
        for (i, slot) in out.iter_mut().enumerate() {
            *slot = u32::from_le_bytes([
                bytes[i * 4],
                bytes[i * 4 + 1],
                bytes[i * 4 + 2],
                bytes[i * 4 + 3],
            ]);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Простой детерминированный RNG для тестов (xorshift64).
    pub struct TestRng(pub u64);
    impl RandomSource for TestRng {
        fn fill(&mut self, buf: &mut [u8]) {
            for b in buf {
                let mut x = self.0;
                x ^= x << 13;
                x ^= x >> 7;
                x ^= x << 17;
                self.0 = x;
                *b = x as u8;
            }
        }
    }

    #[test]
    fn add_and_sub_round_trip() {
        let a = BigUint::from_u64(1_234_567_890);
        let b = BigUint::from_u64(987_654_321);
        let s = add(&a, &b);
        assert_eq!(s.to_string(), "2222222211");
        let d = sub(&s, &b);
        assert_eq!(d, a);
    }

    #[test]
    fn mul_matches_u128_for_small() {
        for (a, b) in [
            (0u64, 0u64),
            (1, 1),
            (10, 20),
            (12_345, 67_890),
            (u32::MAX as u64, u32::MAX as u64),
        ] {
            let r = mul(&BigUint::from_u64(a), &BigUint::from_u64(b));
            assert_eq!(r.to_string(), (u128::from(a) * u128::from(b)).to_string());
        }
    }

    #[test]
    fn divrem_basic() {
        let a = BigUint::from_u64(1_000_000);
        let b = BigUint::from_u64(7);
        let (q, r) = divrem(&a, &b);
        assert_eq!(q, BigUint::from_u64(142_857));
        assert_eq!(r, BigUint::from_u64(1));
    }

    #[test]
    fn divrem_when_a_less_than_b() {
        let a = BigUint::from_u64(3);
        let b = BigUint::from_u64(7);
        let (q, r) = divrem(&a, &b);
        assert!(q.is_zero());
        assert_eq!(r, a);
    }

    #[test]
    fn mod_pow_known_value() {
        // 7^560 mod 561 = 1 (561 = 3·11·17 — число Кармайкла).
        let r = mod_pow(
            &BigUint::from_u64(7),
            &BigUint::from_u64(560),
            &BigUint::from_u64(561),
        );
        assert_eq!(r, BigUint::one());
    }

    #[test]
    fn mod_pow_with_modulus_one_is_zero() {
        let r = mod_pow(
            &BigUint::from_u64(7),
            &BigUint::from_u64(3),
            &BigUint::one(),
        );
        assert!(r.is_zero());
    }

    #[test]
    fn gcd_known() {
        assert_eq!(
            gcd(&BigUint::from_u64(252), &BigUint::from_u64(105)),
            BigUint::from_u64(21)
        );
        assert_eq!(
            gcd(&BigUint::from_u64(17), &BigUint::from_u64(31)),
            BigUint::one()
        );
    }

    #[test]
    fn mod_inverse_known() {
        // 3 · 4 = 12 ≡ 1 (mod 11)
        let inv = mod_inverse(&BigUint::from_u64(3), &BigUint::from_u64(11)).unwrap();
        assert_eq!(inv, BigUint::from_u64(4));
    }

    #[test]
    fn mod_inverse_textbook_rsa_params() {
        // p=61, q=53 → n=3233, phi=3120, e=17, d=2753.
        let d = mod_inverse(&BigUint::from_u64(17), &BigUint::from_u64(3120)).unwrap();
        assert_eq!(d, BigUint::from_u64(2753));
    }

    #[test]
    fn mod_inverse_none_when_not_coprime() {
        assert!(mod_inverse(&BigUint::from_u64(6), &BigUint::from_u64(9)).is_none());
    }

    #[test]
    fn bytes_round_trip() {
        let n = BigUint::parse("0xdeadbeefcafebabe1234567890abcdef").unwrap();
        let bytes = n.to_bytes_be(0);
        assert_eq!(bytes.len(), 16);
        let n2 = BigUint::from_bytes_be(&bytes);
        assert_eq!(n2, n);
    }

    #[test]
    fn to_bytes_be_pads() {
        let n = BigUint::from_u64(0xFF);
        assert_eq!(n.to_bytes_be(4), vec![0, 0, 0, 0xFF]);
        // pad с нулём — отдельный случай.
        assert_eq!(BigUint::zero().to_bytes_be(2), vec![0, 0]);
    }

    #[test]
    fn parse_dec_and_hex() {
        let dec: BigUint = BigUint::parse("1234567890").unwrap();
        let hex: BigUint = BigUint::parse("0x499602D2").unwrap();
        assert_eq!(dec, hex);
        assert_eq!(dec.to_hex(), "499602d2");
    }

    #[test]
    fn random_with_exact_bits_has_right_length() {
        let mut rng = TestRng(0xDEAD_BEEF_CAFE_BABE);
        for bits in [1usize, 8, 32, 33, 100, 512] {
            let n = BigUint::random_with_exact_bits(bits, &mut rng);
            assert_eq!(n.bit_length(), bits, "bits = {bits}, n = {n}");
        }
    }
}

#[cfg(test)]
mod property_tests {
    use proptest::prelude::*;

    use super::*;

    proptest! {
        #[test]
        fn add_matches_u128(a: u64, b: u64) {
            let r = add(&BigUint::from_u64(a), &BigUint::from_u64(b));
            prop_assert_eq!(r.to_string(), (u128::from(a) + u128::from(b)).to_string());
        }

        #[test]
        fn mul_matches_u128(a: u64, b: u64) {
            let r = mul(&BigUint::from_u64(a), &BigUint::from_u64(b));
            prop_assert_eq!(r.to_string(), (u128::from(a) * u128::from(b)).to_string());
        }

        #[test]
        fn divrem_matches_u128(a: u64, b in 1u64..=u64::MAX) {
            let (q, r) = divrem(&BigUint::from_u64(a), &BigUint::from_u64(b));
            prop_assert_eq!(q.to_string(), (a / b).to_string());
            prop_assert_eq!(r.to_string(), (a % b).to_string());
        }

        #[test]
        fn mod_pow_matches_u128(base: u32, exp: u16, m in 1u32..=u32::MAX) {
            let actual = mod_pow(
                &BigUint::from_u64(u64::from(base)),
                &BigUint::from_u64(u64::from(exp)),
                &BigUint::from_u64(u64::from(m)),
            );
            // Эталон через 64-битное mod-exp.
            let mut expected: u64 = 1;
            let mut b = u64::from(base) % u64::from(m);
            let mut e = u64::from(exp);
            while e > 0 {
                if e & 1 == 1 {
                    expected = (expected * b) % u64::from(m);
                }
                b = (b * b) % u64::from(m);
                e >>= 1;
            }
            prop_assert_eq!(actual.to_string(), expected.to_string());
        }

        #[test]
        fn mod_inverse_matches_definition(a in 1u32..=10_000, m in 2u32..=10_000) {
            let bi_a = BigUint::from_u64(u64::from(a));
            let bi_m = BigUint::from_u64(u64::from(m));
            if let Some(inv) = mod_inverse(&bi_a, &bi_m) {
                let product = mul_mod(&bi_a, &inv, &bi_m);
                prop_assert_eq!(product, BigUint::one());
            } else {
                // gcd(a,m) != 1
                prop_assert_ne!(gcd(&bi_a, &bi_m), BigUint::one());
            }
        }
    }
}
