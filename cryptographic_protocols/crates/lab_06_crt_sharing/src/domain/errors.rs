//! Доменные ошибки лаб 6.

use thiserror::Error;

#[derive(Debug, Error)]
pub enum DomainError {
    #[error("пороги (k, n) должны удовлетворять 1 ≤ k ≤ n, получено k={k}, n={n}")]
    InvalidThreshold { k: usize, n: usize },

    #[error("не найдена последовательность Миньотта/Асмут-Блума для (k={k}, n={n}, S={secret})")]
    SequenceNotFound { k: usize, n: usize, secret: String },

    #[error("обратный элемент {a} mod {p} не существует")]
    NoModularInverse { a: String, p: String },

    #[error("дано {given} долей, требуется ровно {needed}")]
    WrongShareCount { needed: usize, given: usize },

    #[error("базис СОК должен состоять из попарно взаимно простых чисел")]
    NonCoprimeBasis,
}
