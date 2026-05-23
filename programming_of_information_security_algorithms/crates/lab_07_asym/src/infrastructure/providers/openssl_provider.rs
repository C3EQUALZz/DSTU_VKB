//! Универсальный provider поверх крейта `openssl` (тонкая обёртка над
//! системным `libcrypto`). Используется на macOS и Linux —
//! Apple deprecated `SecKey*` для импорта raw-DER ключей, а OpenSSL
//! на macOS поставляется штатно (или через Homebrew в системном месте).

#![cfg(any(target_os = "macos", target_os = "linux"))]

use openssl::md::Md;
use openssl::pkey::{PKey, Private, Public};
use openssl::pkey_ctx::PkeyCtx;
use openssl::rsa::{Padding, Rsa};

use crate::domain::cipher::{
    AsymmetricCryptoProvider, CryptoError, RawKeyPair, RawPrivateKey, RawPublicKey,
};

pub struct OpenSslProvider;

impl OpenSslProvider {
    #[must_use]
    pub const fn new() -> Self {
        Self
    }
}

impl Default for OpenSslProvider {
    fn default() -> Self {
        Self::new()
    }
}

fn map_err<E: std::fmt::Display>(e: E) -> CryptoError {
    CryptoError::Native(e.to_string())
}

impl AsymmetricCryptoProvider for OpenSslProvider {
    fn name(&self) -> &'static str {
        #[cfg(target_os = "macos")]
        {
            "macOS / OpenSSL (system libcrypto)"
        }
        #[cfg(target_os = "linux")]
        {
            "Linux / OpenSSL (system libcrypto)"
        }
        #[cfg(not(any(target_os = "macos", target_os = "linux")))]
        {
            "OpenSSL (system libcrypto)"
        }
    }

    fn generate_rsa_keypair(&self, bits: usize) -> Result<RawKeyPair, CryptoError> {
        let rsa = Rsa::generate(bits as u32).map_err(map_err)?;
        let public_der = rsa.public_key_to_der_pkcs1().map_err(map_err)?;
        let private_der = rsa.private_key_to_der().map_err(map_err)?;
        Ok(RawKeyPair {
            public: RawPublicKey {
                bits,
                der: public_der,
            },
            private: RawPrivateKey {
                bits,
                der: private_der,
            },
        })
    }

    fn rsa_oaep_encrypt(
        &self,
        public: &RawPublicKey,
        plaintext: &[u8],
    ) -> Result<Vec<u8>, CryptoError> {
        let rsa = Rsa::public_key_from_der_pkcs1(&public.der).map_err(map_err)?;
        let pkey = PKey::<Public>::from_rsa(rsa).map_err(map_err)?;
        let mut ctx = PkeyCtx::new(&pkey).map_err(map_err)?;
        ctx.encrypt_init().map_err(map_err)?;
        ctx.set_rsa_padding(Padding::PKCS1_OAEP).map_err(map_err)?;
        ctx.set_rsa_oaep_md(Md::sha256()).map_err(map_err)?;
        ctx.set_rsa_mgf1_md(Md::sha256()).map_err(map_err)?;
        let mut ct = Vec::new();
        ctx.encrypt_to_vec(plaintext, &mut ct).map_err(map_err)?;
        Ok(ct)
    }

    fn rsa_oaep_decrypt(
        &self,
        private: &RawPrivateKey,
        ciphertext: &[u8],
    ) -> Result<Vec<u8>, CryptoError> {
        let rsa = Rsa::private_key_from_der(&private.der).map_err(map_err)?;
        let pkey = PKey::<Private>::from_rsa(rsa).map_err(map_err)?;
        let mut ctx = PkeyCtx::new(&pkey).map_err(map_err)?;
        ctx.decrypt_init().map_err(map_err)?;
        ctx.set_rsa_padding(Padding::PKCS1_OAEP).map_err(map_err)?;
        ctx.set_rsa_oaep_md(Md::sha256()).map_err(map_err)?;
        ctx.set_rsa_mgf1_md(Md::sha256()).map_err(map_err)?;
        let mut pt = Vec::new();
        ctx.decrypt_to_vec(ciphertext, &mut pt).map_err(map_err)?;
        Ok(pt)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn generate_and_round_trip_2048() {
        let p = OpenSslProvider::new();
        let kp = p.generate_rsa_keypair(2048).unwrap();
        assert_eq!(kp.public.bits, 2048);
        let msg = b"Hello, system libcrypto!";
        let ct = p.rsa_oaep_encrypt(&kp.public, msg).unwrap();
        let pt = p.rsa_oaep_decrypt(&kp.private, &ct).unwrap();
        assert_eq!(pt, msg);
    }

    #[test]
    fn corrupted_ciphertext_is_rejected() {
        let p = OpenSslProvider::new();
        let kp = p.generate_rsa_keypair(2048).unwrap();
        let mut ct = p.rsa_oaep_encrypt(&kp.public, b"hi").unwrap();
        let last = ct.len() - 1;
        ct[last] ^= 0xFF;
        let err = p.rsa_oaep_decrypt(&kp.private, &ct).unwrap_err();
        let msg = format!("{err}");
        assert!(msg.to_lowercase().contains("decrypt") || msg.contains("OAEP"));
    }
}
