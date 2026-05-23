pub mod cipher;
pub mod key;

pub use cipher::{CryptoError, SymmetricCryptoProvider, open, seal};
pub use key::SymmetricKey;
