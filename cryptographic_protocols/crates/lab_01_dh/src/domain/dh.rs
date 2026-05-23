//! Схема обмена ключами Диффи-Хеллмана.

use num_bigint::BigUint;
use num_traits::One;
use tracing::debug;

use super::errors::DomainError;
use super::rng::RandomSource;

/// Общие открытые параметры протокола: модуль n (простое) и первообразный корень g.
#[derive(Debug, Clone)]
pub struct PublicParameters {
    pub n: BigUint,
    pub g: BigUint,
}

/// Сторона протокола: знает свой секретный X и вычисляет открытое Y = g^X mod n.
#[derive(Debug, Clone)]
pub struct Party {
    pub x: BigUint,
    pub y: BigUint,
}

impl Party {
    /// Создать сторону с конкретным секретом x (для воспроизводимых демонстраций).
    ///
    /// # Errors
    /// [`DomainError::PrivateOutOfRange`] если x ∉ [2; n-2].
    pub fn from_private(x: BigUint, params: &PublicParameters) -> Result<Self, DomainError> {
        let two = BigUint::from(2u32);
        let upper = &params.n - &two;
        if x < two || x > upper {
            return Err(DomainError::PrivateOutOfRange {
                value: x.to_string(),
            });
        }
        let y = params.g.modpow(&x, &params.n);
        Ok(Self { x, y })
    }

    /// Создать сторону со случайным секретом x ∈ [2; n−2].
    pub fn random<R: RandomSource>(params: &PublicParameters, rng: &mut R) -> Self {
        let two = BigUint::from(2u32);
        let upper = &params.n - BigUint::one();
        let x = rng.random_range(&two, &upper);
        let y = params.g.modpow(&x, &params.n);
        debug!(
            x_bits = x.bits(),
            y_bits = y.bits(),
            "сгенерирована сторона DH"
        );
        Self { x, y }
    }
}

/// Вычислить общий секретный ключ K, зная свой X и Y контрагента.
///
/// K = Y_other^X_self mod n.
pub fn shared_secret(self_x: &BigUint, other_y: &BigUint, n: &BigUint) -> BigUint {
    other_y.modpow(self_x, n)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::domain::rng::SeededRng;

    /// Пример из методички: n=97, g=5, X_A=36, X_B=58, общий ключ K=75.
    #[test]
    fn methodichka_example_recovers_k_75() {
        let params = PublicParameters {
            n: BigUint::from(97u32),
            g: BigUint::from(5u32),
        };
        let alice = Party::from_private(BigUint::from(36u32), &params).unwrap();
        let bob = Party::from_private(BigUint::from(58u32), &params).unwrap();

        assert_eq!(alice.y, BigUint::from(50u32));
        assert_eq!(bob.y, BigUint::from(44u32));

        let k_a = shared_secret(&alice.x, &bob.y, &params.n);
        let k_b = shared_secret(&bob.x, &alice.y, &params.n);
        assert_eq!(k_a, k_b);
        assert_eq!(k_a, BigUint::from(75u32));
    }

    #[test]
    fn random_parties_share_same_key() {
        let params = PublicParameters {
            n: BigUint::from(97u32),
            g: BigUint::from(5u32),
        };
        let mut rng = SeededRng::new(1);
        let alice = Party::random(&params, &mut rng);
        let bob = Party::random(&params, &mut rng);
        let k_a = shared_secret(&alice.x, &bob.y, &params.n);
        let k_b = shared_secret(&bob.x, &alice.y, &params.n);
        assert_eq!(k_a, k_b);
    }
}
