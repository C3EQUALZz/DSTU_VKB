//! Пороговая схема Блэкли (3, n) на поле Z_p.
//!
//! Идея: секрет — координата x_0 точки Q = (x_0, y_0, z_0) в трёхмерном пространстве.
//! Каждая доля — уравнение плоскости z = a·x + b·y + c, где
//! c = z_0 − a·x_0 − b·y_0 (mod p). Любые три плоскости пересекаются в Q.

use super::errors::DomainError;
use super::modular::{inv, norm};

/// Точка-секрет: (x_0 = секрет, y_0, z_0 — случайные).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SecretPoint {
    pub x0: i64,
    pub y0: i64,
    pub z0: i64,
}

/// Доля Блэкли — плоскость z = a·x + b·y + c (хранится по коэффициентам).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct PlaneShare {
    pub a: i64,
    pub b: i64,
    pub c: i64,
}

/// Создать долю из (a, b) и секретной точки Q. c = z_0 − a·x_0 − b·y_0.
pub fn share_from_ab(a: i64, b: i64, q: SecretPoint, p: i64) -> PlaneShare {
    let c = norm(q.z0 - a * q.x0 - b * q.y0, p);
    PlaneShare {
        a: norm(a, p),
        b: norm(b, p),
        c,
    }
}

/// Восстановить точку Q = (x_0, y_0, z_0) по трём долям-плоскостям через решение системы
/// в Z_p методом Гаусса.
///
/// Система:
///   a_1 x + b_1 y − z = −c_1
///   a_2 x + b_2 y − z = −c_2
///   a_3 x + b_3 y − z = −c_3
pub fn reconstruct(shares: &[PlaneShare], p: i64) -> Result<SecretPoint, DomainError> {
    if shares.len() != 3 {
        return Err(DomainError::WrongShareCount {
            needed: 3,
            given: shares.len(),
        });
    }
    let mut mat = [[0i64; 4]; 3];
    for (i, s) in shares.iter().enumerate() {
        mat[i][0] = norm(s.a, p);
        mat[i][1] = norm(s.b, p);
        mat[i][2] = norm(-1, p);
        mat[i][3] = norm(-s.c, p);
    }
    gauss_3x4(&mut mat, p)?;
    Ok(SecretPoint {
        x0: mat[0][3],
        y0: mat[1][3],
        z0: mat[2][3],
    })
}

fn gauss_3x4(mat: &mut [[i64; 4]; 3], p: i64) -> Result<(), DomainError> {
    for col in 0..3 {
        // pivot
        let mut pivot = None;
        for row in col..3 {
            if mat[row][col] != 0 {
                pivot = Some(row);
                break;
            }
        }
        let pivot = pivot.ok_or(DomainError::SingularSystem)?;
        mat.swap(col, pivot);
        let pv_inv = inv(mat[col][col], p)?;
        for j in 0..4 {
            mat[col][j] = norm(mat[col][j] * pv_inv, p);
        }
        for row in 0..3 {
            if row == col {
                continue;
            }
            let factor = mat[row][col];
            if factor == 0 {
                continue;
            }
            for j in 0..4 {
                let sub = norm(factor * mat[col][j], p);
                mat[row][j] = norm(mat[row][j] - sub, p);
            }
        }
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Пример 1 из методички: Q=(5,1,2), p=7, доля Алисы (a=5, b=2).
    /// c = 2 − 5·5 − 2·1 = −25 = 3 (mod 7).
    #[test]
    fn methodichka_alice_share_c_is_3() {
        let q = SecretPoint {
            x0: 5,
            y0: 1,
            z0: 2,
        };
        let s = share_from_ab(5, 2, q, 7);
        assert_eq!(s, PlaneShare { a: 5, b: 2, c: 3 });
    }

    /// По примеру 1 восстановим Q по трём долям.
    #[test]
    fn methodichka_example_1_reconstructs_q() {
        let q = SecretPoint {
            x0: 5,
            y0: 1,
            z0: 2,
        };
        let p = 7;
        let alice = share_from_ab(5, 2, q, p);
        let bob = share_from_ab(-5, -2, q, p);
        let dave = share_from_ab(4, 2, q, p);
        let recovered = reconstruct(&[alice, bob, dave], p).unwrap();
        assert_eq!(recovered, q);
    }

    /// Пример 2 из методички: p=11, Алиса z=x−y+6, Боб z=−6x+3y+2, Кэрол z=3x+4y+9.
    /// Q = (10, 2, 3).
    #[test]
    fn methodichka_example_2_recovers_q_10_2_3() {
        let p = 11;
        let alice = PlaneShare { a: 1, b: -1, c: 6 };
        let bob = PlaneShare { a: -6, b: 3, c: 2 };
        let carol = PlaneShare { a: 3, b: 4, c: 9 };
        let q = reconstruct(&[alice, bob, carol], p).unwrap();
        assert_eq!(
            q,
            SecretPoint {
                x0: 10,
                y0: 2,
                z0: 3
            }
        );
    }
}
