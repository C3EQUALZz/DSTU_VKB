//! Лаб 6 — симметричное шифрование через встроенный криптопровайдер ОС.
//!
//! Архитектура:
//! - [`domain::cipher::SymmetricCryptoProvider`] — Strategy-trait;
//! - [`infrastructure::providers`] — три реализации (macOS / Linux / Windows),
//!   выбор компилируется через `cfg(target_os = …)`;
//! - [`application::usecases`] — generate-key / encrypt / decrypt поверх trait'а;
//! - [`presentation::cli`] — clap.

pub mod application;
pub mod domain;
pub mod infrastructure;
pub mod presentation;
