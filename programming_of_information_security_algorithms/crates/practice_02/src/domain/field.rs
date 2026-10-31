use super::Error;

/// Простое поле с модулем, помещающимся в u64.
#[derive(Clone, Copy, Debug)]
pub struct PrimeField {
    modulus: u64,
}

impl PrimeField {
    pub fn new(modulus: u64) -> Result<Self, Error> {
        if modulus <= 3 || !is_prime(modulus) {
            return Err(Error::InvalidModulus(modulus));
        }
        Ok(Self { modulus })
    }

    pub fn modulus(self) -> u64 {
        self.modulus
    }

    pub fn normalize(self, value: i128) -> u64 {
        value.rem_euclid(i128::from(self.modulus)) as u64
    }

    pub fn add(self, a: u64, b: u64) -> u64 {
        ((u128::from(a) + u128::from(b)) % u128::from(self.modulus)) as u64
    }

    pub fn sub(self, a: u64, b: u64) -> u64 {
        self.normalize(i128::from(a) - i128::from(b))
    }

    pub fn mul(self, a: u64, b: u64) -> u64 {
        mul_mod(a, b, self.modulus)
    }

    pub fn pow(self, base: u64, exponent: u64) -> u64 {
        pow_mod(base, exponent, self.modulus)
    }

    /// Малая теорема Ферма: a⁻¹ = a^(p−2) для a ≠ 0.
    pub fn inverse(self, value: u64) -> Result<u64, Error> {
        if value % self.modulus == 0 {
            return Err(Error::ZeroInverse);
        }
        Ok(self.pow(value, self.modulus - 2))
    }
}

fn mul_mod(a: u64, b: u64, modulus: u64) -> u64 {
    ((u128::from(a) * u128::from(b)) % u128::from(modulus)) as u64
}

fn pow_mod(mut base: u64, mut exponent: u64, modulus: u64) -> u64 {
    let mut result = 1;
    base %= modulus;
    while exponent != 0 {
        if exponent & 1 != 0 {
            result = mul_mod(result, base, modulus);
        }
        base = mul_mod(base, base, modulus);
        exponent >>= 1;
    }
    result
}

/// Детерминированный Miller–Rabin для всего диапазона u64.
/// Набор оснований Jim Sinclair: https://miller-rabin.appspot.com/.
pub fn is_prime(value: u64) -> bool {
    if value < 2 {
        return false;
    }
    for prime in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37] {
        if value % prime == 0 {
            return value == prime;
        }
    }
    let shifts = (value - 1).trailing_zeros();
    let odd_part = (value - 1) >> shifts;
    for base in [2, 325, 9375, 28178, 450_775, 9_780_504, 1_795_265_022] {
        if base % value == 0 {
            continue;
        }
        let mut witness = pow_mod(base, odd_part, value);
        if witness == 1 || witness == value - 1 {
            continue;
        }
        let mut passed = false;
        for _ in 1..shifts {
            witness = mul_mod(witness, witness, value);
            if witness == value - 1 {
                passed = true;
                break;
            }
        }
        if !passed {
            return false;
        }
    }
    true
}
