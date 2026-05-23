//! Знаковая длинная арифметика для практики 1.
//!
//! Реализация — без сторонних библиотек. Хранение: модуль числа в виде
//! вектора 32-битных `u32`-limbs в little-endian (limb с индексом 0 — младший),
//! плюс отдельный знак. Ноль — `limbs.is_empty()`. Канонизация (`trim`)
//! поддерживается на каждой записи: ведущих нулевых limb'ов не бывает.

use std::cmp::Ordering;
use std::fmt;

use thiserror::Error;

/// Знак длинного числа.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Sign {
    Negative,
    Zero,
    Positive,
}

impl Sign {
    /// Меняет знак на противоположный.
    pub const fn flip(self) -> Self {
        match self {
            Self::Positive => Self::Negative,
            Self::Negative => Self::Positive,
            Self::Zero => Self::Zero,
        }
    }
}

#[derive(Debug, Error, PartialEq, Eq)]
pub enum ParseError {
    #[error("пустая строка")]
    Empty,
    #[error("недопустимый символ {ch:?} в позиции {pos}")]
    BadChar { ch: char, pos: usize },
    #[error("незнакомый префикс основания {prefix:?}")]
    BadPrefix { prefix: String },
}

/// Длинное знаковое целое.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BigInt {
    sign: Sign,
    /// little-endian, без ведущих нулей; для нуля — пусто.
    limbs: Vec<u32>,
}

impl BigInt {
    /// Ноль.
    #[must_use]
    pub const fn zero() -> Self {
        Self {
            sign: Sign::Zero,
            limbs: Vec::new(),
        }
    }

    /// Создаёт число из `i128` (любого знака).
    #[must_use]
    pub fn from_i128(v: i128) -> Self {
        if v == 0 {
            return Self::zero();
        }
        let (sign, mag) = if v < 0 {
            // Особый случай: `i128::MIN.unsigned_abs()` нельзя посчитать
            // через `(-v) as u128`, потому что `-i128::MIN` переполняет.
            // Используем `unsigned_abs`.
            (Sign::Negative, v.unsigned_abs())
        } else {
            (Sign::Positive, v as u128)
        };
        Self {
            sign,
            limbs: limbs_from_u128(mag),
        }
    }

    /// Возвращает `Some(i128)`, если число помещается в знаковый 128-битный
    /// тип, иначе `None`. Используется CLI'ем для «проверки обычным сложением».
    pub fn to_i128(&self) -> Option<i128> {
        // Канонизация гарантирует, что limbs.len() ≤ 4 ⇒ число влезает в u128.
        if self.limbs.len() > 4 {
            return None;
        }
        let mut m: u128 = 0;
        for (i, limb) in self.limbs.iter().enumerate() {
            m |= u128::from(*limb) << (32 * i);
        }
        match self.sign {
            Sign::Zero => Some(0),
            Sign::Positive => i128::try_from(m).ok(),
            Sign::Negative => {
                // |i128::MIN| = 2^127 = m, кодируется как минимум напрямую.
                if m == 1u128 << 127 {
                    Some(i128::MIN)
                } else {
                    i128::try_from(m).ok().map(|x| -x)
                }
            }
        }
    }

    /// Парсит число из десятичной или 16-ричной (с префиксом `0x` или `0X`)
    /// записи, допускается ведущий знак `+`/`-` и нижние подчёркивания
    /// `1_000_000` для удобства.
    ///
    /// # Errors
    /// — `ParseError::Empty`, если строка пустая;
    /// — `ParseError::BadChar`, если найден недопустимый символ;
    /// — `ParseError::BadPrefix`, если префикс не `0x`/`0X`.
    pub fn parse(s: &str) -> Result<Self, ParseError> {
        if s.is_empty() {
            return Err(ParseError::Empty);
        }
        let (sign_explicit, rest) = match s.as_bytes()[0] {
            b'+' => (Sign::Positive, &s[1..]),
            b'-' => (Sign::Negative, &s[1..]),
            _ => (Sign::Positive, s),
        };
        if rest.is_empty() {
            return Err(ParseError::Empty);
        }

        let (base, body) =
            if let Some(stripped) = rest.strip_prefix("0x").or_else(|| rest.strip_prefix("0X")) {
                (16u32, stripped)
            } else if let Some(prefix) = rest.get(..2) {
                // Запретим случайные «0b», «0o» — лаба требует только dec/hex.
                if prefix.starts_with('0')
                    && prefix.len() == 2
                    && !prefix.as_bytes()[1].is_ascii_digit()
                {
                    return Err(ParseError::BadPrefix {
                        prefix: prefix.to_string(),
                    });
                }
                (10u32, rest)
            } else {
                (10u32, rest)
            };

        let mut limbs: Vec<u32> = Vec::new();
        let mut had_digits = false;
        for (pos, ch) in body.char_indices() {
            if ch == '_' {
                continue;
            }
            let digit = ch.to_digit(base).ok_or(ParseError::BadChar { ch, pos })?;
            mul_small(&mut limbs, base);
            add_small(&mut limbs, digit);
            had_digits = true;
        }
        if !had_digits {
            return Err(ParseError::Empty);
        }

        let sign = if limbs.is_empty() {
            Sign::Zero
        } else {
            sign_explicit
        };
        Ok(Self { sign, limbs })
    }

    /// Текущий знак.
    #[must_use]
    pub const fn sign(&self) -> Sign {
        self.sign
    }

    /// Количество битов в модуле (0 для нуля).
    #[must_use]
    pub fn bit_length(&self) -> usize {
        match self.limbs.last() {
            None => 0,
            Some(top) => self.limbs.len() * 32 - (top.leading_zeros() as usize),
        }
    }

    /// Количество десятичных цифр в модуле (1 для нуля).
    #[must_use]
    pub fn decimal_digits(&self) -> usize {
        if matches!(self.sign, Sign::Zero) {
            return 1;
        }
        // Длина строки без знака.
        self.to_string().trim_start_matches('-').chars().count()
    }

    /// Возвращает число с противоположным знаком.
    #[must_use]
    pub fn negate(&self) -> Self {
        Self {
            sign: self.sign.flip(),
            limbs: self.limbs.clone(),
        }
    }

    /// Сравнение по модулю (знак игнорируется).
    fn cmp_abs(&self, other: &Self) -> Ordering {
        match self.limbs.len().cmp(&other.limbs.len()) {
            Ordering::Equal => self.limbs.iter().rev().cmp(other.limbs.iter().rev()),
            ord => ord,
        }
    }

    fn is_zero(&self) -> bool {
        matches!(self.sign, Sign::Zero)
    }
}

/// Сложение длинных чисел.
///
/// Знак определяется по правилам школьной алгебры:
/// — одинаковые знаки → знак сохраняется, модули складываются;
/// — разные знаки     → результат имеет знак большего модуля, модули вычитаются.
#[must_use]
pub fn add(a: &BigInt, b: &BigInt) -> BigInt {
    if a.is_zero() {
        return b.clone();
    }
    if b.is_zero() {
        return a.clone();
    }
    if a.sign == b.sign {
        let limbs = add_abs(&a.limbs, &b.limbs);
        BigInt {
            sign: a.sign,
            limbs,
        }
    } else {
        match a.cmp_abs(b) {
            Ordering::Equal => BigInt::zero(),
            Ordering::Greater => BigInt {
                sign: a.sign,
                limbs: sub_abs(&a.limbs, &b.limbs),
            },
            Ordering::Less => BigInt {
                sign: b.sign,
                limbs: sub_abs(&b.limbs, &a.limbs),
            },
        }
    }
}

/// Вычитание: `a - b = a + (-b)`.
#[must_use]
pub fn sub(a: &BigInt, b: &BigInt) -> BigInt {
    add(a, &b.negate())
}

// ───── представление в строке ─────

impl fmt::Display for BigInt {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        if matches!(self.sign, Sign::Zero) {
            return f.write_str("0");
        }
        // Десятичное представление: повторное деление модуля на 10⁹.
        // Используем «большие» цифры по 10⁹ — за итерацию извлекаем сразу 9
        // десятичных цифр; это сильно быстрее, чем деление на 10.
        const CHUNK: u32 = 1_000_000_000;
        let mut limbs = self.limbs.clone();
        let mut chunks: Vec<u32> = Vec::new();
        while !limbs.is_empty() {
            let rem = div_small(&mut limbs, CHUNK);
            chunks.push(rem);
        }

        if matches!(self.sign, Sign::Negative) {
            f.write_str("-")?;
        }
        // Последний chunk — самый старший разряд: печатается без ведущих нулей.
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

impl std::str::FromStr for BigInt {
    type Err = ParseError;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Self::parse(s)
    }
}

// ───── низкоуровневые операции над limbs ─────

/// Конвертирует беззнаковую `u128` величину в little-endian limbs.
fn limbs_from_u128(mut v: u128) -> Vec<u32> {
    let mut out = Vec::with_capacity(4);
    while v != 0 {
        out.push(v as u32);
        v >>= 32;
    }
    out
}

/// `limbs += k` (как 32-битное число), in-place. Поддерживает переполнение.
fn add_small(limbs: &mut Vec<u32>, k: u32) {
    if k == 0 {
        return;
    }
    let mut carry: u64 = u64::from(k);
    for limb in limbs.iter_mut() {
        let v = u64::from(*limb) + carry;
        *limb = v as u32;
        carry = v >> 32;
        if carry == 0 {
            return;
        }
    }
    if carry > 0 {
        limbs.push(carry as u32);
    }
}

/// `limbs *= k`, in-place. Распространяет перенос до старшего limb'а.
fn mul_small(limbs: &mut Vec<u32>, k: u32) {
    if k == 0 {
        limbs.clear();
        return;
    }
    if k == 1 || limbs.is_empty() {
        return;
    }
    let mut carry: u64 = 0;
    for limb in limbs.iter_mut() {
        let v = u64::from(*limb) * u64::from(k) + carry;
        *limb = v as u32;
        carry = v >> 32;
    }
    while carry > 0 {
        limbs.push(carry as u32);
        carry >>= 32;
    }
}

/// `limbs /= k`, возвращает остаток. Работает с старшего limb'а вниз.
fn div_small(limbs: &mut Vec<u32>, k: u32) -> u32 {
    debug_assert!(k != 0, "деление на 0");
    let mut rem: u64 = 0;
    for limb in limbs.iter_mut().rev() {
        let cur = (rem << 32) | u64::from(*limb);
        *limb = (cur / u64::from(k)) as u32;
        rem = cur % u64::from(k);
    }
    while limbs.last() == Some(&0) {
        limbs.pop();
    }
    rem as u32
}

/// Сложение модулей: вектор limbs `a + b`. Учитывается перенос между limb'ами.
fn add_abs(a: &[u32], b: &[u32]) -> Vec<u32> {
    let n = a.len().max(b.len());
    let mut out = Vec::with_capacity(n + 1);
    let mut carry: u64 = 0;
    for i in 0..n {
        let x = u64::from(a.get(i).copied().unwrap_or(0));
        let y = u64::from(b.get(i).copied().unwrap_or(0));
        let s = x + y + carry;
        out.push(s as u32);
        carry = s >> 32;
    }
    if carry != 0 {
        out.push(carry as u32);
    }
    trim(&mut out);
    out
}

/// Вычитание модулей: предполагается, что `a ≥ b`. Учитывается заём.
fn sub_abs(a: &[u32], b: &[u32]) -> Vec<u32> {
    debug_assert!(cmp_slices(a, b).is_ge(), "sub_abs: a < b");
    let mut out = Vec::with_capacity(a.len());
    let mut borrow: i64 = 0;
    for i in 0..a.len() {
        let x = i64::from(a[i]);
        let y = i64::from(b.get(i).copied().unwrap_or(0));
        let mut diff = x - y - borrow;
        if diff < 0 {
            diff += 1i64 << 32;
            borrow = 1;
        } else {
            borrow = 0;
        }
        out.push(diff as u32);
    }
    debug_assert_eq!(borrow, 0, "sub_abs: финальный заём не должен оставаться");
    trim(&mut out);
    out
}

fn cmp_slices(a: &[u32], b: &[u32]) -> Ordering {
    match a.len().cmp(&b.len()) {
        Ordering::Equal => a.iter().rev().cmp(b.iter().rev()),
        ord => ord,
    }
}

fn trim(v: &mut Vec<u32>) {
    while v.last() == Some(&0) {
        v.pop();
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn zero_displays_as_zero() {
        assert_eq!(BigInt::zero().to_string(), "0");
    }

    #[test]
    fn parse_and_display_round_trip() {
        for s in [
            "0",
            "1",
            "-1",
            "12345",
            "-12345",
            "100000000000000000000", // > u64
            "-100000000000000000000",
            "12345678901234567890123456789012345678901234567890123456789012345678901234567890",
        ] {
            let n: BigInt = s.parse().unwrap();
            assert_eq!(n.to_string(), s, "round-trip для {s}");
        }
    }

    #[test]
    fn parse_hex() {
        let n: BigInt = "0xFF".parse().unwrap();
        assert_eq!(n.to_string(), "255");
        let n: BigInt = "-0x100".parse().unwrap();
        assert_eq!(n.to_string(), "-256");
    }

    #[test]
    fn parse_with_underscores() {
        let n: BigInt = "1_000_000_000_000_000_000_000".parse().unwrap();
        assert_eq!(n.to_string(), "1000000000000000000000");
    }

    #[test]
    fn parse_rejects_bad_input() {
        assert_eq!(BigInt::parse(""), Err(ParseError::Empty));
        assert_eq!(BigInt::parse("-"), Err(ParseError::Empty));
        assert!(matches!(
            BigInt::parse("12a3"),
            Err(ParseError::BadChar { ch: 'a', .. })
        ));
        assert!(matches!(
            BigInt::parse("0b101"),
            Err(ParseError::BadPrefix { .. })
        ));
    }

    #[test]
    fn add_same_sign() {
        let a: BigInt = "100000000000000000000".parse().unwrap();
        let b: BigInt = "1".parse().unwrap();
        assert_eq!(add(&a, &b).to_string(), "100000000000000000001");

        let a: BigInt = "-100000000000000000000".parse().unwrap();
        let b: BigInt = "-1".parse().unwrap();
        assert_eq!(add(&a, &b).to_string(), "-100000000000000000001");
    }

    #[test]
    fn add_mixed_sign() {
        let a: BigInt = "100".parse().unwrap();
        let b: BigInt = "-30".parse().unwrap();
        assert_eq!(add(&a, &b).to_string(), "70");
        assert_eq!(add(&b, &a).to_string(), "70");
    }

    #[test]
    fn add_cancels_to_zero() {
        let a: BigInt = "123456789012345678901234567890".parse().unwrap();
        let b: BigInt = "-123456789012345678901234567890".parse().unwrap();
        assert_eq!(add(&a, &b).to_string(), "0");
        assert_eq!(add(&a, &b).sign(), Sign::Zero);
    }

    #[test]
    fn sub_basic() {
        let a: BigInt = "1000000000000000000000".parse().unwrap();
        let b: BigInt = "1".parse().unwrap();
        assert_eq!(sub(&a, &b).to_string(), "999999999999999999999");
    }

    #[test]
    fn sub_negative_result() {
        let a: BigInt = "1".parse().unwrap();
        let b: BigInt = "1000000000000000000000".parse().unwrap();
        assert_eq!(sub(&a, &b).to_string(), "-999999999999999999999");
    }

    #[test]
    fn to_i128_round_trip() {
        for v in [0i128, 1, -1, i128::MAX, i128::MIN, 12345, -12345] {
            let n = BigInt::from_i128(v);
            assert_eq!(n.to_i128(), Some(v), "for {v}");
        }
    }

    #[test]
    fn to_i128_returns_none_when_too_big() {
        let n: BigInt = "1000000000000000000000000000000000000000".parse().unwrap();
        assert!(n.to_i128().is_none());
    }

    #[test]
    fn bit_length_basic() {
        assert_eq!(BigInt::zero().bit_length(), 0);
        assert_eq!(BigInt::from_i128(1).bit_length(), 1);
        assert_eq!(BigInt::from_i128(255).bit_length(), 8);
        assert_eq!(BigInt::from_i128(256).bit_length(), 9);
    }

    #[test]
    fn decimal_digits_basic() {
        assert_eq!(BigInt::zero().decimal_digits(), 1);
        assert_eq!(BigInt::from_i128(999).decimal_digits(), 3);
        let big: BigInt =
            "12345678901234567890123456789012345678901234567890123456789012345678901234567890"
                .parse()
                .unwrap();
        assert_eq!(big.decimal_digits(), 80);
    }
}

#[cfg(test)]
mod property_tests {
    use proptest::prelude::*;

    use super::*;

    proptest! {
        /// Для случайных `i128 a, b`:
        /// — если `a + b` помещается в `i128`, наш `BigInt` даёт тот же результат;
        /// — иначе наш результат заведомо не влезает в `i128` (но всё ещё валиден).
        #[test]
        fn add_matches_i128(a: i128, b: i128) {
            let actual = add(&BigInt::from_i128(a), &BigInt::from_i128(b));
            match a.checked_add(b) {
                Some(expected) => prop_assert_eq!(actual.to_i128(), Some(expected)),
                None => prop_assert!(actual.to_i128().is_none()),
            }
        }

        #[test]
        fn sub_matches_i128(a: i128, b: i128) {
            let actual = sub(&BigInt::from_i128(a), &BigInt::from_i128(b));
            match a.checked_sub(b) {
                Some(expected) => prop_assert_eq!(actual.to_i128(), Some(expected)),
                None => prop_assert!(actual.to_i128().is_none()),
            }
        }

        /// `(a + b) - b == a` без потерь, даже когда промежуточный результат
        /// не помещается в `i128`.
        #[test]
        fn add_sub_round_trip(a: i128, b: i128) {
            let bi_a = BigInt::from_i128(a);
            let bi_b = BigInt::from_i128(b);
            let result = sub(&add(&bi_a, &bi_b), &bi_b);
            prop_assert_eq!(result, bi_a);
        }

        #[test]
        fn negate_is_involution(a: i128) {
            let n = BigInt::from_i128(a);
            prop_assert_eq!(n.negate().negate(), n);
        }

        /// Сложение коммутативно.
        #[test]
        fn add_is_commutative(a: i128, b: i128) {
            let bi_a = BigInt::from_i128(a);
            let bi_b = BigInt::from_i128(b);
            prop_assert_eq!(add(&bi_a, &bi_b), add(&bi_b, &bi_a));
        }

        /// Сложение ассоциативно (промежуточная сумма может выходить за i128 —
        /// важно, что наш BigInt с этим справляется).
        #[test]
        fn add_is_associative(a: i128, b: i128, c: i128) {
            let bi_a = BigInt::from_i128(a);
            let bi_b = BigInt::from_i128(b);
            let bi_c = BigInt::from_i128(c);
            prop_assert_eq!(
                add(&add(&bi_a, &bi_b), &bi_c),
                add(&bi_a, &add(&bi_b, &bi_c))
            );
        }

        /// Ноль — нейтральный элемент сложения.
        #[test]
        fn zero_is_additive_identity(a: i128) {
            let n = BigInt::from_i128(a);
            prop_assert_eq!(add(&n, &BigInt::zero()), n.clone());
            prop_assert_eq!(add(&BigInt::zero(), &n), n);
        }

        /// `a - a = 0`.
        #[test]
        fn subtracting_self_is_zero(a: i128) {
            let n = BigInt::from_i128(a);
            prop_assert_eq!(sub(&n, &n), BigInt::zero());
        }

        /// `a - b == -(b - a)`.
        #[test]
        fn sub_anti_commutes(a: i128, b: i128) {
            let bi_a = BigInt::from_i128(a);
            let bi_b = BigInt::from_i128(b);
            prop_assert_eq!(sub(&bi_a, &bi_b), sub(&bi_b, &bi_a).negate());
        }

        /// Парсинг ↔ форматирование стабильны: `parse(format(n)) == n`.
        #[test]
        fn parse_format_round_trip(a: i128) {
            let n = BigInt::from_i128(a);
            let s = n.to_string();
            let reparsed: BigInt = s.parse().unwrap();
            prop_assert_eq!(reparsed, n);
        }

        /// Парсинг строк из произвольных десятичных цифр устойчив
        /// и форматирование возвращает ту же строку (после нормализации ведущих нулей).
        #[test]
        fn parse_random_decimal_string(
            // от 1 до 200 цифр, первая ненулевая
            head in 1u32..=9,
            tail in proptest::collection::vec(0u32..=9, 0..=199),
            sign_neg: bool,
        ) {
            let body: String = std::iter::once(char::from_digit(head, 10).unwrap())
                .chain(tail.into_iter().map(|d| char::from_digit(d, 10).unwrap()))
                .collect();
            let input = if sign_neg { format!("-{body}") } else { body.clone() };
            let n: BigInt = input.parse().unwrap();
            let expected = if sign_neg { format!("-{body}") } else { body };
            prop_assert_eq!(n.to_string(), expected);
        }
    }
}
