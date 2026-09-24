//! Пересечение трёх и пяти плоскостей Блэкли в точной арифметике.

use num_bigint::BigInt;

use super::DomainError;
use super::exact::Rational;
use super::linear::solve;

#[derive(Clone, Copy, Debug)]
pub struct PlaneShare {
    pub coefficients: [i64; 3],
    pub value: i64,
}

pub fn reconstruct(shares: &[PlaneShare]) -> Result<Vec<Rational>, DomainError> {
    if shares.len() < 3 {
        return Err(DomainError::TooFewShares);
    }
    let coefficients = shares
        .iter()
        .map(|share| share.coefficients.map(BigInt::from).to_vec())
        .collect::<Vec<_>>();
    let values = shares
        .iter()
        .map(|share| BigInt::from(share.value))
        .collect::<Vec<_>>();
    solve(&coefficients, &values, 3)
}

#[cfg(test)]
mod tests {
    use super::{PlaneShare, reconstruct};
    use crate::domain::DomainError;

    #[test]
    fn fifth_plane_must_contain_recovered_point() {
        let shares = [
            PlaneShare {
                coefficients: [7, 23, 1],
                value: 1502,
            },
            PlaneShare {
                coefficients: [27, 8, 15],
                value: 5479,
            },
            PlaneShare {
                coefficients: [25, 10, 13],
                value: 5079,
            },
            PlaneShare {
                coefficients: [1, 21, 30],
                value: 542,
            },
            PlaneShare {
                coefficients: [16, 3, 28],
                value: 3392,
            },
        ];
        assert_eq!(reconstruct(&shares), Err(DomainError::InconsistentShares));
    }
}
