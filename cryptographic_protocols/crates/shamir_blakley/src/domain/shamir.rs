//! Восстановление квадратичного полинома по трём или пяти долям.

use std::collections::HashSet;

use num_bigint::BigInt;

use super::DomainError;
use super::exact::Rational;
use super::linear::solve;

#[derive(Clone, Copy, Debug)]
pub struct Share {
    pub x: i64,
    pub y: i64,
}

pub fn reconstruct(shares: &[Share]) -> Result<Vec<Rational>, DomainError> {
    if shares.len() < 3 {
        return Err(DomainError::TooFewShares);
    }
    let mut seen = HashSet::new();
    if shares.iter().any(|share| !seen.insert(share.x)) {
        return Err(DomainError::DuplicateAbscissa);
    }

    let degree_plus_one = shares.len();
    let matrix = shares
        .iter()
        .map(|share| {
            let x = BigInt::from(share.x);
            let mut power = BigInt::from(1);
            (0..degree_plus_one)
                .map(|_| {
                    let value = power.clone();
                    power *= &x;
                    value
                })
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();
    let values = shares
        .iter()
        .map(|share| BigInt::from(share.y))
        .collect::<Vec<_>>();
    let coefficients = solve(&matrix, &values, degree_plus_one)?;
    if coefficients.iter().skip(3).any(|value| !value.is_zero()) {
        return Err(DomainError::NotQuadratic);
    }
    Ok(coefficients)
}

#[cfg(test)]
mod tests {
    use proptest::prelude::*;

    use super::{Share, reconstruct};
    use crate::domain::DomainError;

    proptest! {
        #[test]
        fn quadratic_is_recovered_exactly(secret in -1000i64..1000, a in -20i64..20, b in -20i64..20) {
            let xs = [2, 5, 6, 8, 13];
            let shares = xs.map(|x| Share { x, y: a*x*x+b*x+secret });
            for count in [3, 5] {
                let result = reconstruct(&shares[..count]).unwrap();
                prop_assert_eq!(result[0].to_string(), secret.to_string());
                prop_assert_eq!(result[1].to_string(), b.to_string());
                prop_assert_eq!(result[2].to_string(), a.to_string());
            }
        }
    }

    #[test]
    fn fifth_share_must_match_quadratic() {
        let shares = [
            Share { x: 2, y: 235 },
            Share { x: 5, y: 367 },
            Share { x: 6, y: 431 },
            Share { x: 8, y: 589 },
            Share { x: 13, y: 1160 },
        ];
        assert_eq!(reconstruct(&shares), Err(DomainError::NotQuadratic));
    }

    #[test]
    fn duplicate_abscissa_is_rejected() {
        let shares = [
            Share { x: 2, y: 1 },
            Share { x: 2, y: 2 },
            Share { x: 3, y: 3 },
        ];
        assert_eq!(reconstruct(&shares), Err(DomainError::DuplicateAbscissa));
    }
}
