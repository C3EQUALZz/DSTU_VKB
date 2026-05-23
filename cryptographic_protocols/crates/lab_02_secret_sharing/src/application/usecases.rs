//! Сценарии лаб 2: упражнения 2 (Шамир) и 3 (Блэкли) по вариантам.

use tracing::info;

use crate::domain::blakley::{
    PlaneShare, SecretPoint, reconstruct as blakley_reconstruct, share_from_ab,
};
use crate::domain::errors::DomainError;
use crate::domain::shamir::{Polynomial, Share, reconstruct, reconstruct_polynomial};

/// Результат упражнения 2 (Шамир): секрет + восстановленный полином + доля Дейва.
#[derive(Debug, Clone)]
pub struct ShamirExerciseReport {
    pub secret: i64,
    pub polynomial: Polynomial,
    pub dave_share: Share,
}

/// Восстановить секрет/полином/долю Дейва для упражнения 2.
///
/// `dave_x` — x-координата, по которой генерируется новая «легальная» доля Дейва.
pub fn shamir_exercise2(
    shares: &[Share],
    p: i64,
    dave_x: i64,
) -> Result<ShamirExerciseReport, DomainError> {
    let secret = reconstruct(shares, p)?;
    let polynomial = reconstruct_polynomial(shares, p)?;
    let dave_share = polynomial.share(dave_x);
    info!(
        secret,
        dave_x,
        dave_y = dave_share.y,
        "Шамир: упражнение 2 решено"
    );
    Ok(ShamirExerciseReport {
        secret,
        polynomial,
        dave_share,
    })
}

/// Результат упражнения 3 (Блэкли): 4 созданные доли + восстановленный секрет
/// по трём из них.
#[derive(Debug, Clone)]
pub struct BlakleyExerciseReport {
    pub q: SecretPoint,
    pub shares: [PlaneShare; 4],
    pub recovered_q: SecretPoint,
}

/// Решить упражнение 3: для секретной точки Q и четырёх пар (a, b) построить
/// доли и восстановить Q «по любым трём из них» (методичка).
///
/// Если первая тройка (A, B, D) даёт вырожденную систему — перебираем
/// все 4 комбинации по 3.
pub fn blakley_exercise3(
    q: SecretPoint,
    p: i64,
    abcd_pairs: [(i64, i64); 4],
) -> Result<BlakleyExerciseReport, DomainError> {
    let [pa, pb, pd, pc] = abcd_pairs;
    let shares = [
        share_from_ab(pa.0, pa.1, q, p),
        share_from_ab(pb.0, pb.1, q, p),
        share_from_ab(pd.0, pd.1, q, p),
        share_from_ab(pc.0, pc.1, q, p),
    ];
    // Перебираем тройки в порядке: {A,B,D}, {A,B,C}, {A,D,C}, {B,D,C}.
    let combos: [[usize; 3]; 4] = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]];
    let mut last_err: Option<DomainError> = None;
    for combo in combos {
        let trio = [shares[combo[0]], shares[combo[1]], shares[combo[2]]];
        match blakley_reconstruct(&trio, p) {
            Ok(recovered_q) => {
                info!(?recovered_q, ?combo, "Блэкли: упражнение 3 решено");
                return Ok(BlakleyExerciseReport {
                    q,
                    shares,
                    recovered_q,
                });
            }
            Err(e) => last_err = Some(e),
        }
    }
    Err(last_err.unwrap_or(DomainError::SingularSystem))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn shamir_methodichka_example_3() {
        let shares = [
            Share { x: 9, y: 8 },
            Share { x: 3, y: 8 },
            Share { x: 6, y: 1 },
        ];
        let r = shamir_exercise2(&shares, 11, 2).unwrap();
        assert_eq!(r.secret, 7);
        assert_eq!(r.polynomial.coeffs, vec![7, 9, 2]);
        assert_eq!(r.dave_share, Share { x: 2, y: 0 });
    }

    #[test]
    fn blakley_methodichka_example_1() {
        let q = SecretPoint {
            x0: 5,
            y0: 1,
            z0: 2,
        };
        let r = blakley_exercise3(q, 7, [(5, 2), (-5, -2), (4, 2), (2, -6)]).unwrap();
        assert_eq!(r.recovered_q, q);
    }
}
