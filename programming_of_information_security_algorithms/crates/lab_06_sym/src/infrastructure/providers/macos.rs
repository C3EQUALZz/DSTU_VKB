//! macOS-реализация — прямой FFI к CommonCrypto и Security framework.
//!
//! CommonCrypto часть `libSystem.dylib`, поэтому отдельный `#[link]`
//! не нужен для AES/HMAC. `SecRandomCopyBytes` живёт в `Security.framework`
//! — его линкуем явно.
//!
//! Это полностью соответствует требованию условия лаб 6 «встроенный в ОС
//! функционал» — мы вызываем системные API напрямую, без сторонней
//! криптобиблиотеки.

#![cfg(target_os = "macos")]

use std::os::raw::c_int;

use crate::domain::cipher::{CryptoError, SymmetricCryptoProvider};
use crate::domain::key::{
    AES_BLOCK_BYTES, AES_KEY_BYTES, HMAC_KEY_BYTES, HMAC_TAG_BYTES, IV_BYTES,
};

// ───── FFI декларации ─────

// CommonCrypto: kCCEncrypt / kCCDecrypt.
const KCC_ENCRYPT: u32 = 0;
const KCC_DECRYPT: u32 = 1;
// kCCAlgorithmAES (он же AES128 — длина задаётся keyLength).
const KCC_ALG_AES: u32 = 0;
// kCCOptionPKCS7Padding.
const KCC_OPT_PKCS7: u32 = 0x0001;
// kCCHmacAlgSHA256.
const KCC_HMAC_SHA256: u32 = 2;
// kCCSuccess.
const KCC_SUCCESS: i32 = 0;
// errSecSuccess.
const ERR_SEC_SUCCESS: i32 = 0;

unsafe extern "C" {
    fn CCCrypt(
        op: u32,
        alg: u32,
        options: u32,
        key: *const u8,
        key_length: usize,
        iv: *const u8,
        data_in: *const u8,
        data_in_length: usize,
        data_out: *mut u8,
        data_out_available: usize,
        data_out_moved: *mut usize,
    ) -> i32;

    fn CCHmac(
        algorithm: u32,
        key: *const u8,
        key_length: usize,
        data: *const u8,
        data_length: usize,
        mac_out: *mut u8,
    );
}

#[link(name = "Security", kind = "framework")]
unsafe extern "C" {
    fn SecRandomCopyBytes(rnd: *const std::ffi::c_void, count: usize, bytes: *mut u8) -> c_int;
}

/// Провайдер на основе системных API macOS.
pub struct CommonCryptoProvider;

impl CommonCryptoProvider {
    /// Создаёт провайдер. Никаких ресурсов не аллоцирует —
    /// `CCCrypt` stateless.
    #[must_use]
    pub const fn new() -> Self {
        Self
    }
}

impl Default for CommonCryptoProvider {
    fn default() -> Self {
        Self::new()
    }
}

impl SymmetricCryptoProvider for CommonCryptoProvider {
    fn name(&self) -> &'static str {
        "macOS / CommonCrypto + SecRandom"
    }

    fn fill_random(&self, buf: &mut [u8]) -> Result<(), CryptoError> {
        // SecRandomCopyBytes(NULL = kSecRandomDefault, count, buf).
        let rc = unsafe { SecRandomCopyBytes(std::ptr::null(), buf.len(), buf.as_mut_ptr()) };
        if rc == ERR_SEC_SUCCESS {
            Ok(())
        } else {
            Err(CryptoError::Native(format!(
                "SecRandomCopyBytes returned {rc}"
            )))
        }
    }

    fn aes_cbc_encrypt(
        &self,
        key: &[u8; AES_KEY_BYTES],
        iv: &[u8; IV_BYTES],
        plaintext: &[u8],
    ) -> Result<Vec<u8>, CryptoError> {
        cccrypt(KCC_ENCRYPT, key, iv, plaintext)
    }

    fn aes_cbc_decrypt(
        &self,
        key: &[u8; AES_KEY_BYTES],
        iv: &[u8; IV_BYTES],
        ciphertext: &[u8],
    ) -> Result<Vec<u8>, CryptoError> {
        cccrypt(KCC_DECRYPT, key, iv, ciphertext)
    }

    fn hmac_sha256(
        &self,
        key: &[u8; HMAC_KEY_BYTES],
        data: &[u8],
    ) -> Result<[u8; HMAC_TAG_BYTES], CryptoError> {
        let mut tag = [0u8; HMAC_TAG_BYTES];
        unsafe {
            CCHmac(
                KCC_HMAC_SHA256,
                key.as_ptr(),
                key.len(),
                data.as_ptr(),
                data.len(),
                tag.as_mut_ptr(),
            );
        }
        Ok(tag)
    }
}

fn cccrypt(op: u32, key: &[u8], iv: &[u8], input: &[u8]) -> Result<Vec<u8>, CryptoError> {
    // С PKCS7 padding'ом размер выхода ≤ inputLen + одного блока.
    let cap = input.len() + AES_BLOCK_BYTES;
    let mut out = vec![0u8; cap];
    let mut moved: usize = 0;
    let rc = unsafe {
        CCCrypt(
            op,
            KCC_ALG_AES,
            KCC_OPT_PKCS7,
            key.as_ptr(),
            key.len(),
            iv.as_ptr(),
            input.as_ptr(),
            input.len(),
            out.as_mut_ptr(),
            cap,
            &raw mut moved,
        )
    };
    if rc == KCC_SUCCESS {
        out.truncate(moved);
        Ok(out)
    } else {
        Err(CryptoError::Native(format!("CCCrypt returned status {rc}")))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Самопроверка раунд-трипа на короткой строке.
    #[test]
    fn aes_cbc_round_trip_basic() {
        let p = CommonCryptoProvider::new();
        let key = [0x42u8; AES_KEY_BYTES];
        let iv = [0x10u8; IV_BYTES];
        let pt = b"hello, common-crypto!";
        let ct = p.aes_cbc_encrypt(&key, &iv, pt).unwrap();
        let pt2 = p.aes_cbc_decrypt(&key, &iv, &ct).unwrap();
        assert_eq!(pt2, pt);
    }

    /// NIST CAVS AES-256-CBC: KEY 0..0, IV 0..0, plaintext one block of zeros →
    /// дает известное значение. Сверка одного блока.
    #[test]
    fn aes_cbc_one_block_against_known_vector() {
        let p = CommonCryptoProvider::new();
        let key = [0u8; AES_KEY_BYTES];
        let iv = [0u8; IV_BYTES];
        let pt = [0u8; AES_BLOCK_BYTES];
        // Зашифрованный нулевой блок ключом из нулей с IV из нулей.
        // Из NIST CAVS (KAT_AES.zip, ECBVarTxt256.rsp, Key=0):
        // Ciphertext = dc 95 c0 78 a2 40 89 89 ad 48 a2 14 92 84 20 87
        // С PKCS7 padding'ом добавится ещё блок — сверяем только первый блок.
        let ct = p.aes_cbc_encrypt(&key, &iv, &pt).unwrap();
        let expected_first_block: [u8; 16] = [
            0xdc, 0x95, 0xc0, 0x78, 0xa2, 0x40, 0x89, 0x89, 0xad, 0x48, 0xa2, 0x14, 0x92, 0x84,
            0x20, 0x87,
        ];
        assert_eq!(&ct[..16], &expected_first_block);
    }

    /// RFC 4231 §4.2 — HMAC-SHA-256 для ключа `0x0b…0b` и сообщения «Hi There».
    #[test]
    fn hmac_sha256_against_rfc4231() {
        // Длина 20 байт в RFC, но HMAC принимает любую длину; padded zero нулями
        // даст другой результат → используем 20 значащих байт.
        let mut key20 = [0u8; 20];
        key20.fill(0x0b);
        // У нас тип контракта `&[u8; 32]`, поэтому используем helper напрямую.
        let mut tag = [0u8; HMAC_TAG_BYTES];
        unsafe {
            CCHmac(
                KCC_HMAC_SHA256,
                key20.as_ptr(),
                key20.len(),
                b"Hi There".as_ptr(),
                b"Hi There".len(),
                tag.as_mut_ptr(),
            );
        }
        let expected: [u8; 32] = [
            0xb0, 0x34, 0x4c, 0x61, 0xd8, 0xdb, 0x38, 0x53, 0x5c, 0xa8, 0xaf, 0xce, 0xaf, 0x0b,
            0xf1, 0x2b, 0x88, 0x1d, 0xc2, 0x00, 0xc9, 0x83, 0x3d, 0xa7, 0x26, 0xe9, 0x37, 0x6c,
            0x2e, 0x32, 0xcf, 0xf7,
        ];
        assert_eq!(tag, expected);
    }

    #[test]
    fn fill_random_returns_non_zero_bytes() {
        let p = CommonCryptoProvider::new();
        let mut buf = [0u8; 64];
        p.fill_random(&mut buf).unwrap();
        assert!(buf.iter().any(|&b| b != 0));
    }
}
