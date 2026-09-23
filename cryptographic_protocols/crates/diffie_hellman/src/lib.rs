//! Обмен ключами Диффи–Хеллмана и учебный канал связи.
//!
//! Слои Clean Architecture:
//! - [`domain`] — алгоритмы (Рабин-Миллер, генерация простых, первообразные корни, DH).
//! - [`application`] — usecases, оркестрируют domain.
//! - [`presentation`] — CLI (clap).
//!
//! - [`infrastructure`] — транспорт TCP с ограниченными по размеру кадрами.

pub mod application;
pub mod domain;
pub mod infrastructure;
pub mod presentation;
