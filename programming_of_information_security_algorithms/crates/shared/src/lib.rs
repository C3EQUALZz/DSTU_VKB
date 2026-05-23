//! Общая инфраструктура для лабораторных по PSIA.

pub mod errors;
pub mod logging;

pub use color_eyre::{Result, eyre::WrapErr};
