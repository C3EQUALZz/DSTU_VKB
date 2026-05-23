//! Общая инфраструктура для лабораторных по курсу «Криптографические протоколы».

pub mod alphabet;
pub mod errors;
pub mod logging;

pub use color_eyre::{Result, eyre::WrapErr};
