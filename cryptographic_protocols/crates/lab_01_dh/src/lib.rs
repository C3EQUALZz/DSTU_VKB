//! Лаб 1: Диффи-Хеллман.
//!
//! Слои Clean Architecture:
//! - [`domain`] — алгоритмы (Рабин-Миллер, генерация простых, первообразные корни, DH).
//! - [`application`] — usecases, оркестрируют domain.
//! - [`presentation`] — CLI (clap).
//!
//! Инфраструктурного слоя как такового нет: внешние ресурсы (рандом) инжектятся
//! через trait [`domain::rng::RandomSource`].

pub mod application;
pub mod domain;
pub mod presentation;
