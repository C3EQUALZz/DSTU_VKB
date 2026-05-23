//! Пороговая схема Шамира (m, n) на поле Z_p.
//!
//! Идея: секрет S = f(0), полином f степени m−1 с случайными коэффициентами.
//! Доли — пары (x_j, f(x_j)). По любым m долям восстанавливается f(0) по
//! формуле интерполяции Лагранжа:
//!
//! f(0) = Σ_j f(x_j) · Π_{k≠j} x_k / (x_k − x_j)   (по модулю p)

use tracing::debug;

use super::errors::DomainError;
use super::modular::{inv, norm};

/// Доля участника схемы Шамира — пара (x, y).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Share {
    pub x: i64,
    pub y: i64,
}

/// Полином над Z_p, хранится по коэффициентам [a0, a1, ..., a_{m-1}], где a0 = S.
#[derive(Debug, Clone)]
pub struct Polynomial {
    pub coeffs: Vec<i64>,
    pub p: i64,
}

impl Polynomial {
    pub fn new(coeffs: Vec<i64>, p: i64) -> Self {
        let coeffs = coeffs.into_iter().map(|c| norm(c, p)).collect();
        Self { coeffs, p }
    }

    pub fn evaluate(&self, x: i64) -> i64 {
        // Горнер: f(x) = a0 + x(a1 + x(a2 + ...))
        let mut acc = 0i64;
        for &c in self.coeffs.iter().rev() {
            acc = norm(acc * x + c, self.p);
        }
        acc
    }

    pub fn share(&self, x: i64) -> Share {
        Share {
            x,
            y: self.evaluate(x),
        }
    }
}

/// Восстановить f(0) (секрет) по m долям через интерполяцию Лагранжа.
pub fn reconstruct(shares: &[Share], p: i64) -> Result<i64, DomainError> {
    if shares.is_empty() {
        return Err(DomainError::WrongShareCount {
            needed: 1,
            given: 0,
        });
    }
    // Проверка уникальности x_j.
    for i in 0..shares.len() {
        for j in (i + 1)..shares.len() {
            if shares[i].x == shares[j].x {
                return Err(DomainError::DuplicateX { x: shares[i].x });
            }
        }
    }

    let mut total = 0i64;
    for (j, sj) in shares.iter().enumerate() {
        let mut num = 1i64;
        let mut den = 1i64;
        for (k, sk) in shares.iter().enumerate() {
            if k == j {
                continue;
            }
            // L_j(0) = Π_{k≠j} (0 − x_k) / (x_j − x_k) = Π x_k / (x_j − x_k) · (−1)^{m-1},
            // но проще: L_j(0) = Π (−x_k) / (x_j − x_k).
            num = norm(num * norm(-sk.x, p), p);
            den = norm(den * norm(sj.x - sk.x, p), p);
        }
        let lj0 = norm(num * inv(den, p)?, p);
        total = norm(total + sj.y * lj0, p);
        debug!(j, x = sj.x, y = sj.y, lj0, total, "interpolation step");
    }
    Ok(total)
}

/// Восстановить полином целиком (коэффициенты a0..a_{m-1}) по m долям.
///
/// Используется в упражнении 2: «вычислите свою правильную долю Дейва».
/// Алгоритм: f(0) восстанавливаем интерполяцией Лагранжа; затем составляем
/// систему линейных уравнений f(x_j) = y_j из (m − 1) долей (без свободного члена)
/// и решаем её методом Гаусса в Z_p.
pub fn reconstruct_polynomial(shares: &[Share], p: i64) -> Result<Polynomial, DomainError> {
    let m = shares.len();
    if m == 0 {
        return Err(DomainError::WrongShareCount {
            needed: 1,
            given: 0,
        });
    }
    // Метод Гаусса в Z_p для матрицы Вандермонда V·a = y.
    // Строки: для каждой доли (x, y) уравнение Σ a_k x^k = y, k = 0..m-1.
    let mut mat = vec![vec![0i64; m + 1]; m];
    for (i, s) in shares.iter().enumerate() {
        let mut xk = 1i64;
        for j in 0..m {
            mat[i][j] = xk;
            xk = norm(xk * s.x, p);
        }
        mat[i][m] = norm(s.y, p);
    }

    // Прямой ход.
    for col in 0..m {
        // Найти pivot.
        let mut pivot = None;
        for row in col..m {
            if mat[row][col] != 0 {
                pivot = Some(row);
                break;
            }
        }
        let pivot = pivot.ok_or(DomainError::SingularSystem)?;
        mat.swap(col, pivot);
        // Нормализовать строку col: умножить на inv(pivot_value).
        let pv_inv = inv(mat[col][col], p)?;
        for j in col..=m {
            mat[col][j] = norm(mat[col][j] * pv_inv, p);
        }
        // Обнулить остальные строки в столбце col.
        for row in 0..m {
            if row == col {
                continue;
            }
            let factor = mat[row][col];
            if factor == 0 {
                continue;
            }
            for j in col..=m {
                let sub = norm(factor * mat[col][j], p);
                mat[row][j] = norm(mat[row][j] - sub, p);
            }
        }
    }

    let coeffs: Vec<i64> = (0..m).map(|i| mat[i][m]).collect();
    Ok(Polynomial::new(coeffs, p))
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Пример 3 из методички: (3,n)-схема Шамира, p=11, доли:
    /// Алиса (9, 8), Боб (3, 8), Кэрол (6, 1). Секрет = 7.
    #[test]
    fn methodichka_example_3_secret_is_7() {
        let p = 11;
        let shares = [
            Share { x: 9, y: 8 },
            Share { x: 3, y: 8 },
            Share { x: 6, y: 1 },
        ];
        assert_eq!(reconstruct(&shares, p).unwrap(), 7);
    }

    /// По тому же примеру методички восстановим полином 2x² + 9x + 7 и
    /// проверим долю Дейва (x=2) — должна быть (2, 0).
    #[test]
    fn methodichka_example_3_recovers_polynomial() {
        let p = 11;
        let shares = [
            Share { x: 9, y: 8 },
            Share { x: 3, y: 8 },
            Share { x: 6, y: 1 },
        ];
        let poly = reconstruct_polynomial(&shares, p).unwrap();
        assert_eq!(poly.coeffs, vec![7, 9, 2]);
        assert_eq!(poly.evaluate(2), 0);
    }

    #[test]
    fn polynomial_share_evaluate_roundtrip() {
        let poly = Polynomial::new(vec![7, 9, 2], 11);
        // f(2) = 2·4 + 9·2 + 7 = 33 = 0 (mod 11)
        assert_eq!(poly.evaluate(2), 0);
        // f(9) = 2·81 + 81 + 7 = 250 = 8 (mod 11)
        assert_eq!(poly.evaluate(9), 8);
    }

    #[test]
    fn duplicate_x_rejected() {
        let shares = [Share { x: 3, y: 1 }, Share { x: 3, y: 2 }];
        assert!(matches!(
            reconstruct(&shares, 7),
            Err(DomainError::DuplicateX { x: 3 })
        ));
    }
}
