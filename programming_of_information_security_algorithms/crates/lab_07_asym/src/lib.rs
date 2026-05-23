//! Лаб 7 — асимметричное RSA-OAEP-SHA256 шифрование через встроенный
//! криптопровайдер ОС. Strategy pattern: trait → 3 реализации по `cfg`.

pub mod application;
pub mod domain;
pub mod infrastructure;
pub mod presentation;
