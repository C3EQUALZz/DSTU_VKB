//! Метод Гаусса–Жордана для квадратных и переопределённых систем.

use num_bigint::BigInt;

use super::DomainError;
use super::exact::Rational;

pub fn solve(
    coefficients: &[Vec<BigInt>],
    right_hand_side: &[BigInt],
    variables: usize,
) -> Result<Vec<Rational>, DomainError> {
    if variables == 0
        || coefficients.len() != right_hand_side.len()
        || coefficients.len() < variables
        || coefficients.iter().any(|row| row.len() != variables)
    {
        return Err(DomainError::InvalidSystem);
    }

    let mut matrix: Vec<Vec<Rational>> = coefficients
        .iter()
        .zip(right_hand_side)
        .map(|(row, value)| {
            row.iter()
                .cloned()
                .chain(std::iter::once(value.clone()))
                .map(Rational::from_integer)
                .collect()
        })
        .collect();

    let mut rank = 0;
    for column in 0..variables {
        let Some(pivot) = (rank..matrix.len()).find(|&row| !matrix[row][column].is_zero()) else {
            continue;
        };
        matrix.swap(rank, pivot);
        tracing::info!(column, pivot_row = pivot, "выбран ведущий элемент");

        let divisor = matrix[rank][column].clone();
        for entry in &mut matrix[rank][column..=variables] {
            *entry = entry.div(&divisor)?;
        }

        for row in 0..matrix.len() {
            if row == rank || matrix[row][column].is_zero() {
                continue;
            }
            let factor = matrix[row][column].clone();
            for col in column..=variables {
                matrix[row][col] = matrix[row][col].sub(&factor.mul(&matrix[rank][col]));
            }
        }
        rank += 1;
    }

    if matrix
        .iter()
        .any(|row| row[..variables].iter().all(Rational::is_zero) && !row[variables].is_zero())
    {
        return Err(DomainError::InconsistentShares);
    }
    if rank != variables {
        return Err(DomainError::DegenerateSystem);
    }
    Ok((0..variables)
        .map(|row| matrix[row][variables].clone())
        .collect())
}

#[cfg(test)]
mod tests {
    use num_bigint::BigInt;

    use super::solve;
    use crate::domain::DomainError;

    #[test]
    fn overdetermined_consistent_system() {
        let a = vec![vec![1, 1], vec![1, -1], vec![2, 0]];
        let b = vec![5, 1, 6];
        let a = a
            .into_iter()
            .map(|row| row.into_iter().map(BigInt::from).collect())
            .collect::<Vec<Vec<BigInt>>>();
        let b = b.into_iter().map(BigInt::from).collect::<Vec<_>>();
        let result = solve(&a, &b, 2).unwrap();
        assert_eq!(result[0].to_string(), "3");
        assert_eq!(result[1].to_string(), "2");
    }

    #[test]
    fn inconsistent_extra_equation_is_rejected() {
        let a = vec![vec![1, 1], vec![1, -1], vec![2, 0]];
        let b = vec![5, 1, 7];
        let a = a
            .into_iter()
            .map(|row| row.into_iter().map(BigInt::from).collect())
            .collect::<Vec<Vec<BigInt>>>();
        let b = b.into_iter().map(BigInt::from).collect::<Vec<_>>();
        assert_eq!(solve(&a, &b, 2), Err(DomainError::InconsistentShares));
    }
}
