//! Безопасное простое p = 2q + 1 и первообразный корень для учебного DH.

use num_bigint::BigUint;
use num_traits::One;
use tracing::info;

use super::dh::{Party, PublicParameters};
use super::errors::DomainError;
use super::prime::{divisible_by_small_prime, generate_prime, is_probably_prime};
use super::rng::RandomSource;

#[derive(Debug, Clone)]
pub struct DhGroup {
    pub params: PublicParameters,
    pub q: BigUint,
}

#[derive(Debug, Clone)]
pub struct GroupStats {
    pub q_candidates: u64,
    pub p_candidates: u32,
}

impl DhGroup {
    /// Создать p = 2q + 1: факторизация p − 1 тогда известна без пробных делителей.
    pub fn generate<R: RandomSource>(
        bits: u32,
        rounds: u32,
        max_p_candidates: u32,
        rng: &mut R,
    ) -> Result<(Self, GroupStats), DomainError> {
        if bits < 67 {
            return Err(DomainError::TooFewBits { min: 67, got: bits });
        }
        let mut stats = GroupStats {
            q_candidates: 0,
            p_candidates: 0,
        };
        for _ in 0..max_p_candidates {
            let (q, q_stats) = generate_prime(bits - 1, rounds, 10_000, rng)?;
            stats.q_candidates += u64::from(q_stats.iterations);
            stats.p_candidates += 1;
            let p = (&q << 1u32) + BigUint::one();
            if divisible_by_small_prime(&p) || !is_probably_prime(&p, rounds, rng) {
                continue;
            }
            let mut g = BigUint::from(2u32);
            while g < p {
                if g.modpow(&BigUint::from(2u32), &p) != BigUint::one()
                    && g.modpow(&q, &p) != BigUint::one()
                {
                    info!(modulus_bits = bits, generator = %g, p_candidates = stats.p_candidates, q_candidates = stats.q_candidates, "найдена группа DH");
                    return Ok((
                        Self {
                            params: PublicParameters { n: p, g },
                            q,
                        },
                        stats,
                    ));
                }
                g += 1u32;
            }
        }
        Err(DomainError::PrimeGenExhausted {
            tries: max_p_candidates,
        })
    }

    /// Проверить полученную группу перед созданием собственного секрета.
    pub fn validate<R: RandomSource>(&self, rounds: u32, rng: &mut R) -> Result<(), DomainError> {
        let p = &self.params.n;
        let g = &self.params.g;
        if p.bits() < 67 || p.bits() > 512 {
            return Err(DomainError::InvalidGroup {
                reason: "длина модуля вне диапазона 67..=512 бит",
            });
        }
        if p != &((&self.q << 1u32) + BigUint::one()) {
            return Err(DomainError::InvalidGroup {
                reason: "p не равно 2q + 1",
            });
        }
        if divisible_by_small_prime(&self.q)
            || !is_probably_prime(&self.q, rounds, rng)
            || divisible_by_small_prime(p)
            || !is_probably_prime(p, rounds, rng)
        {
            return Err(DomainError::InvalidGroup {
                reason: "p или q не прошло проверку простоты",
            });
        }
        if g < &BigUint::from(2u32)
            || g >= &(p - BigUint::one())
            || g.modpow(&BigUint::from(2u32), p) == BigUint::one()
            || g.modpow(&self.q, p) == BigUint::one()
        {
            return Err(DomainError::InvalidGroup {
                reason: "g не является первообразным корнем",
            });
        }
        Ok(())
    }

    /// По условию X тоже генерируется как большое простое число.
    pub fn random_party<R: RandomSource>(
        &self,
        rounds: u32,
        rng: &mut R,
    ) -> Result<Party, DomainError> {
        let bits = u32::try_from(self.params.n.bits()).map_err(|_| DomainError::InvalidGroup {
            reason: "слишком длинный модуль",
        })?;
        let (x, _) = generate_prime(bits - 2, rounds, 10_000, rng)?;
        Party::from_private(x, &self.params)
    }

    pub fn validate_peer_public(&self, y: &BigUint) -> Result<(), DomainError> {
        let p = &self.params.n;
        if y <= &BigUint::one()
            || y >= &(p - BigUint::one())
            || y.modpow(&BigUint::from(2u32), p) == BigUint::one()
            || y.modpow(&self.q, p) == BigUint::one()
        {
            return Err(DomainError::InvalidPeerPublic);
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::domain::rng::SeededRng;

    #[test]
    fn generated_group_and_prime_parties_agree() {
        let mut rng = SeededRng::new(11);
        let (group, stats) = DhGroup::generate(67, 8, 1000, &mut rng).unwrap();
        assert!(stats.p_candidates > 0);
        group.validate(8, &mut rng).unwrap();
        let alice = group.random_party(8, &mut rng).unwrap();
        let bob = group.random_party(8, &mut rng).unwrap();
        group.validate_peer_public(&alice.y).unwrap();
        group.validate_peer_public(&bob.y).unwrap();
        assert_eq!(
            bob.y.modpow(&alice.x, &group.params.n),
            alice.y.modpow(&bob.x, &group.params.n)
        );
        assert!(alice.x.bits() > 64);
    }

    #[test]
    fn rejects_small_subgroups() {
        let mut rng = SeededRng::new(11);
        let (group, _) = DhGroup::generate(67, 8, 1000, &mut rng).unwrap();
        assert!(group.validate_peer_public(&BigUint::one()).is_err());
        assert!(
            group
                .validate_peer_public(&(&group.params.n - 1u32))
                .is_err()
        );
    }
}
