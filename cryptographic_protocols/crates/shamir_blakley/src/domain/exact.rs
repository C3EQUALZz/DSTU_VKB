//! Рациональные числа без округления для вычислений из методички.

use std::fmt;

use num_bigint::BigInt;
use num_integer::Integer;
use num_traits::{One, Signed, Zero};

use super::DomainError;

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Rational {
    numerator: BigInt,
    denominator: BigInt,
}

impl Rational {
    pub fn new(numerator: BigInt, denominator: BigInt) -> Result<Self, DomainError> {
        if denominator.is_zero() {
            return Err(DomainError::DivisionByZero);
        }
        Ok(Self::normalized(numerator, denominator))
    }

    pub fn from_integer(value: BigInt) -> Self {
        Self {
            numerator: value,
            denominator: BigInt::one(),
        }
    }

    pub fn zero() -> Self {
        Self::from_integer(BigInt::zero())
    }

    pub fn one() -> Self {
        Self::from_integer(BigInt::one())
    }

    pub fn is_zero(&self) -> bool {
        self.numerator.is_zero()
    }

    pub fn as_integer(&self) -> Option<&BigInt> {
        self.denominator.is_one().then_some(&self.numerator)
    }

    pub fn add(&self, other: &Self) -> Self {
        Self::normalized(
            &self.numerator * &other.denominator + &other.numerator * &self.denominator,
            &self.denominator * &other.denominator,
        )
    }

    pub fn sub(&self, other: &Self) -> Self {
        Self::normalized(
            &self.numerator * &other.denominator - &other.numerator * &self.denominator,
            &self.denominator * &other.denominator,
        )
    }

    pub fn mul(&self, other: &Self) -> Self {
        Self::normalized(
            &self.numerator * &other.numerator,
            &self.denominator * &other.denominator,
        )
    }

    pub fn div(&self, other: &Self) -> Result<Self, DomainError> {
        Self::new(
            &self.numerator * &other.denominator,
            &self.denominator * &other.numerator,
        )
    }

    fn normalized(mut numerator: BigInt, mut denominator: BigInt) -> Self {
        if denominator.is_negative() {
            numerator = -numerator;
            denominator = -denominator;
        }
        let divisor = numerator.gcd(&denominator);
        Self {
            numerator: numerator / &divisor,
            denominator: denominator / divisor,
        }
    }
}

impl fmt::Display for Rational {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        if self.denominator.is_one() {
            write!(f, "{}", self.numerator)
        } else {
            write!(f, "{}/{}", self.numerator, self.denominator)
        }
    }
}

#[cfg(test)]
mod tests {
    use num_bigint::BigInt;

    use super::Rational;

    #[test]
    fn exact_arithmetic_normalizes_sign_and_fraction() {
        let a = Rational::new(BigInt::from(-2), BigInt::from(-4)).unwrap();
        let b = Rational::new(BigInt::from(3), BigInt::from(2)).unwrap();
        assert_eq!(a.to_string(), "1/2");
        assert_eq!(a.add(&b).to_string(), "2");
        assert_eq!(b.sub(&a).to_string(), "1");
        assert_eq!(a.mul(&b).to_string(), "3/4");
        assert_eq!(b.div(&a).unwrap().to_string(), "3");
    }
}
