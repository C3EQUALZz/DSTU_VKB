//! Модулярная арифметика над i64 для пороговых схем.
//!
//! Поля Z_p в наших задачах малы (p ≤ 31), используем i64.

use super::errors::DomainError;

/// «Положительный» модуль: возвращает значение в диапазоне [0; p).
pub fn norm(a: i64, p: i64) -> i64 {
    let r = a % p;
    if r < 0 { r + p } else { r }
}

/// Расширенный алгоритм Евклида: возвращает (gcd, x, y) такие, что a·x + b·y = gcd.
pub fn ext_gcd(a: i64, b: i64) -> (i64, i64, i64) {
    if b == 0 {
        (a, 1, 0)
    } else {
        let (g, x1, y1) = ext_gcd(b, a % b);
        (g, y1, x1 - (a / b) * y1)
    }
}

/// Модулярный обратный: a^{-1} mod p (p простое, иначе может не существовать).
pub fn inv(a: i64, p: i64) -> Result<i64, DomainError> {
    if p <= 1 {
        return Err(DomainError::InvalidModulus(p));
    }
    let (g, x, _) = ext_gcd(norm(a, p), p);
    if g != 1 {
        return Err(DomainError::NoModularInverse { a, p, gcd: g });
    }
    Ok(norm(x, p))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn norm_handles_negatives() {
        assert_eq!(norm(-3, 11), 8);
        assert_eq!(norm(17, 11), 6);
        assert_eq!(norm(0, 11), 0);
    }

    #[test]
    fn inverse_basic() {
        assert_eq!(inv(2, 11).unwrap(), 6); // 2·6 = 12 ≡ 1
        assert_eq!(inv(3, 11).unwrap(), 4);
        assert_eq!(inv(1, 7).unwrap(), 1);
    }

    #[test]
    fn no_inverse_for_zero_divisor() {
        // 6 не имеет обратного по модулю 9 (gcd = 3).
        assert!(matches!(
            inv(6, 9),
            Err(DomainError::NoModularInverse { .. })
        ));
    }
}
