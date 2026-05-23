//! Доменные ошибки лаб 2.

use thiserror::Error;

#[derive(Debug, Error, PartialEq, Eq)]
pub enum DomainError {
    #[error("модуль p должен быть простым и > 1, получено {0}")]
    InvalidModulus(i64),

    #[error("обратный элемент {a} mod {p} не существует (gcd = {gcd})")]
    NoModularInverse { a: i64, p: i64, gcd: i64 },

    #[error("для восстановления нужно {needed} долей, передано {given}")]
    WrongShareCount { needed: usize, given: usize },

    #[error("две доли имеют совпадающую x-координату: {x}")]
    DuplicateX { x: i64 },

    #[error("матрица системы вырождена — три плоскости параллельны или совпадают")]
    SingularSystem,
}
