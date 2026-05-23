//! Практика 1 — длинная арифметика.
//!
//! Соблюдает Clean Architecture:
//! - [`domain`] — чистые алгоритмы и типы (без IO);
//! - [`application`] — оркестрация (use case `VerifyService`);
//! - [`presentation`] — CLI.

pub mod application;
pub mod domain;
pub mod presentation;
