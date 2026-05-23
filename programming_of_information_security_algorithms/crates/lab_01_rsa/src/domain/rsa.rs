//! Генерация ключей и блочные операции RSA.
//!
//! **Учебная** схема: «raw» RSA без PKCS#1 padding'а. Пригодна только
//! для лабораторных целей. Текст разбивается на блоки по `(n_bytes - 1)`
//! байт; шифртекст пишется фиксированными блоками `n_bytes` байт.
//! Чтобы корректно отрезать «хвост» при расшифровке, в начале шифртекста
//! сохраняется длина исходного сообщения (`u64` LE).

use std::cmp::Ordering;

use thiserror::Error;
use tracing::{debug, info, instrument, warn};

use crate::domain::bigint::{BigUint, RandomSource, mod_inverse, mod_pow, mul, sub};
use crate::domain::primes::{generate_prime, is_coprime};

/// Открытый ключ.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PublicKey {
    pub n: BigUint,
    pub e: BigUint,
    pub bits: usize,
}

/// Закрытый ключ. Сохраняем также `p` и `q` — пригодятся для CRT и проверки.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PrivateKey {
    pub n: BigUint,
    pub e: BigUint,
    pub d: BigUint,
    pub p: BigUint,
    pub q: BigUint,
    pub bits: usize,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct KeyPair {
    pub public: PublicKey,
    pub private: PrivateKey,
}

#[derive(Debug, Error)]
pub enum RsaError {
    #[error("шифртекст слишком короткий: ожидался минимум {expected} байт, получено {actual}")]
    CiphertextTooShort { expected: usize, actual: usize },
    #[error("длина шифртекста не кратна размеру блока {block} (получено {len})")]
    CiphertextMisaligned { block: usize, len: usize },
    #[error("заявленная длина исходного сообщения ({claimed}) больше, чем влезает в шифртекст")]
    CiphertextLengthMismatch { claimed: usize },
    #[error("блок plaintext'а имеет {actual} байт, а модуль вмещает только {limit} байт")]
    PlaintextBlockTooBig { actual: usize, limit: usize },
}

impl PublicKey {
    /// Размер модуля в байтах (округление вверх).
    #[must_use]
    pub fn byte_length(&self) -> usize {
        self.bits.div_ceil(8)
    }

    /// Сколько байт исходного текста влезает в один RSA-блок.
    #[must_use]
    pub fn plaintext_block_size(&self) -> usize {
        self.byte_length() - 1
    }
}

impl PrivateKey {
    #[must_use]
    pub fn byte_length(&self) -> usize {
        self.bits.div_ceil(8)
    }

    #[must_use]
    pub fn plaintext_block_size(&self) -> usize {
        self.byte_length() - 1
    }
}

impl KeyPair {
    /// Генерирует пару ключей RSA указанной длины модуля (в битах).
    ///
    /// `e = 65537` — стандартное значение. Если случайно gcd(e, φ) ≠ 1
    /// (крайне редкий случай), генерируется новая пара `p, q`.
    #[instrument(level = "info", skip(rng), fields(bits = bits))]
    pub fn generate<R: RandomSource>(bits: usize, rng: &mut R) -> Self {
        assert!(
            bits >= 64,
            "слишком маленький размер модуля для RSA: {bits} бит"
        );
        assert!(
            bits % 2 == 0,
            "длина модуля должна быть чётной (bits = {bits})"
        );
        let half = bits / 2;
        let e = BigUint::from_u64(65_537);
        info!("starting RSA key generation");

        loop {
            let p = generate_prime(half, rng);
            let mut q = generate_prime(half, rng);
            // Гарантируем p != q — иначе φ = (p-1)² и факторизация тривиальна.
            while p == q {
                warn!("p == q сгенерированы одинаковыми, перегенерируем q");
                q = generate_prime(half, rng);
            }
            // Для удобства — упорядочим p ≥ q.
            let (p, q) = match p.cmp(&q) {
                Ordering::Less => (q, p),
                _ => (p, q),
            };
            let n = mul(&p, &q);

            let p_minus_one = sub(&p, &BigUint::one());
            let q_minus_one = sub(&q, &BigUint::one());
            let phi = mul(&p_minus_one, &q_minus_one);

            if !is_coprime(&e, &phi) {
                warn!("gcd(e, φ) ≠ 1 — повторяем генерацию пары простых");
                continue;
            }

            let Some(d) = mod_inverse(&e, &phi) else {
                warn!("mod_inverse(e, φ) не существует — повторяем");
                continue;
            };

            debug!(
                n_bits = n.bit_length(),
                p_bits = p.bit_length(),
                q_bits = q.bit_length(),
                "RSA key generated"
            );

            let public = PublicKey {
                n: n.clone(),
                e: e.clone(),
                bits,
            };
            let private = PrivateKey {
                n,
                e: e.clone(),
                d,
                p,
                q,
                bits,
            };
            return Self { public, private };
        }
    }
}

const HEADER_LEN: usize = 8;

/// Шифрует произвольный поток байт открытым ключом.
///
/// # Errors
/// `PlaintextBlockTooBig` если блок plaintext оказался ≥ модуля
/// (теоретически невозможно при корректной генерации ключа).
#[instrument(level = "info", skip(public, plaintext), fields(plaintext_bytes = plaintext.len()))]
pub fn encrypt(public: &PublicKey, plaintext: &[u8]) -> Result<Vec<u8>, RsaError> {
    let nbytes = public.byte_length();
    let block_in = public.plaintext_block_size();
    let block_out = nbytes;

    let blocks = plaintext.len().div_ceil(block_in).max(1);
    let mut ct = Vec::with_capacity(HEADER_LEN + blocks * block_out);
    ct.extend_from_slice(&(plaintext.len() as u64).to_le_bytes());

    for (idx, chunk) in plaintext.chunks(block_in).enumerate() {
        let m = BigUint::from_bytes_be(chunk);
        if m >= public.n {
            return Err(RsaError::PlaintextBlockTooBig {
                actual: chunk.len(),
                limit: block_in,
            });
        }
        let c = mod_pow(&m, &public.e, &public.n);
        ct.extend_from_slice(&c.to_bytes_be(block_out));
        debug!(block = idx, "encrypted block");
    }
    info!(
        plaintext_bytes = plaintext.len(),
        ciphertext_bytes = ct.len(),
        "encryption finished"
    );
    Ok(ct)
}

/// Расшифровывает поток байт закрытым ключом.
///
/// # Errors
/// — `CiphertextTooShort` / `CiphertextMisaligned` / `CiphertextLengthMismatch`
/// при некорректном формате шифртекста.
#[instrument(level = "info", skip(private, ciphertext), fields(ciphertext_bytes = ciphertext.len()))]
pub fn decrypt(private: &PrivateKey, ciphertext: &[u8]) -> Result<Vec<u8>, RsaError> {
    let nbytes = private.byte_length();
    let block_out = nbytes;

    if ciphertext.len() < HEADER_LEN {
        return Err(RsaError::CiphertextTooShort {
            expected: HEADER_LEN,
            actual: ciphertext.len(),
        });
    }
    let mut header = [0u8; HEADER_LEN];
    header.copy_from_slice(&ciphertext[..HEADER_LEN]);
    let plain_len = u64::from_le_bytes(header) as usize;
    let body = &ciphertext[HEADER_LEN..];

    if body.len() % block_out != 0 {
        return Err(RsaError::CiphertextMisaligned {
            block: block_out,
            len: body.len(),
        });
    }
    let block_in = private.plaintext_block_size();
    let expected_min = if plain_len == 0 {
        0
    } else {
        plain_len.div_ceil(block_in) * block_out
    };
    if body.len() < expected_min {
        return Err(RsaError::CiphertextLengthMismatch { claimed: plain_len });
    }

    // При шифровании последнего неполного блока plaintext'а сериализовался как
    // BigUint::from_bytes_be(chunk_len_бит), поэтому при расшифровке его исходную
    // длину надо знать заранее — она равна `plain_len % block_in`
    // (или `block_in`, если делится без остатка).
    let total_blocks = body.len() / block_out;
    let mut out = Vec::with_capacity(plain_len);
    for (idx, chunk) in body.chunks(block_out).enumerate() {
        let c = BigUint::from_bytes_be(chunk);
        let m = mod_pow(&c, &private.d, &private.n);
        let is_last = idx + 1 == total_blocks;
        let block_len = if is_last {
            let rem = plain_len % block_in;
            if rem == 0 && plain_len > 0 {
                block_in
            } else {
                rem
            }
        } else {
            block_in
        };
        if block_len == 0 {
            // plain_len == 0, единственный «пустой» блок — пропускаем.
            debug!(block = idx, "decrypted empty block");
            continue;
        }
        let bytes = m.to_bytes_be(block_len);
        // `to_bytes_be(block_len)` гарантирует длину ≥ block_len и большее число
        // никогда не получится при корректном шифртексте (m < n < 2^(bits)).
        let start = bytes.len() - block_len;
        out.extend_from_slice(&bytes[start..]);
        debug!(block = idx, "decrypted block");
        if out.len() == plain_len {
            break;
        }
    }
    info!(
        plaintext_bytes = out.len(),
        ciphertext_bytes = ciphertext.len(),
        "decryption finished"
    );
    Ok(out)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::domain::rng::DeterministicRng;

    /// Учебный пример RSA из Википедии: p=61, q=53, e=17, d=2753, n=3233.
    /// «65» шифруется в «2790». Соберём пары вручную и проверим encrypt/decrypt
    /// на однобайтном сообщении.
    #[test]
    fn textbook_rsa_round_trip() {
        let p = BigUint::from_u64(61);
        let q = BigUint::from_u64(53);
        let n = mul(&p, &q);
        let phi = mul(&sub(&p, &BigUint::one()), &sub(&q, &BigUint::one()));
        let e = BigUint::from_u64(17);
        let d = mod_inverse(&e, &phi).unwrap();
        assert_eq!(d, BigUint::from_u64(2753));

        // 65^17 mod 3233 = 2790
        let m = BigUint::from_u64(65);
        let c = mod_pow(&m, &e, &n);
        assert_eq!(c, BigUint::from_u64(2790));
        let m2 = mod_pow(&c, &d, &n);
        assert_eq!(m2, m);
    }

    /// Генерация пары + round-trip на маленьком сообщении на 128-битном модуле
    /// (учебно-быстрый размер для тестов).
    #[test]
    fn generated_key_round_trips_small_modulus() {
        let mut rng = DeterministicRng::new(0x5EED_1234_BEEF_CAFE);
        let kp = KeyPair::generate(128, &mut rng);
        let plaintext = b"hi";
        let ct = encrypt(&kp.public, plaintext).unwrap();
        let pt = decrypt(&kp.private, &ct).unwrap();
        assert_eq!(pt, plaintext);
    }

    #[test]
    fn generated_key_round_trips_multi_block() {
        let mut rng = DeterministicRng::new(0xAAAA_BBBB_CCCC_DDDD);
        let kp = KeyPair::generate(128, &mut rng);
        let plaintext = b"The quick brown fox jumps over the lazy dog. 1234567890 \xff\x00abc";
        let ct = encrypt(&kp.public, plaintext).unwrap();
        let pt = decrypt(&kp.private, &ct).unwrap();
        assert_eq!(pt, plaintext);
    }

    #[test]
    fn empty_plaintext_round_trips() {
        let mut rng = DeterministicRng::new(7);
        let kp = KeyPair::generate(128, &mut rng);
        let ct = encrypt(&kp.public, b"").unwrap();
        let pt = decrypt(&kp.private, &ct).unwrap();
        assert_eq!(pt, b"");
    }

    #[test]
    fn ciphertext_corruption_changes_plaintext() {
        let mut rng = DeterministicRng::new(11);
        let kp = KeyPair::generate(128, &mut rng);
        let plaintext = b"hello there general kenobi";
        let mut ct = encrypt(&kp.public, plaintext).unwrap();
        // Меняем последний байт шифртекста.
        let last = ct.len() - 1;
        ct[last] ^= 0xFF;
        let pt = decrypt(&kp.private, &ct).unwrap();
        // Без padding (учебный RSA) расшифровка не паникует, но даст другой текст.
        assert_ne!(pt, plaintext);
    }

    #[test]
    fn invalid_ciphertext_too_short_is_reported() {
        let mut rng = DeterministicRng::new(13);
        let kp = KeyPair::generate(128, &mut rng);
        let err = decrypt(&kp.private, b"abc").unwrap_err();
        assert!(matches!(err, RsaError::CiphertextTooShort { .. }));
    }
}
