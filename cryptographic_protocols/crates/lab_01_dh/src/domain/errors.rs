//! Доменные ошибки лаб 1.

use thiserror::Error;

#[derive(Debug, Error)]
pub enum DomainError {
    #[error("параметр {name} должен быть положительным, получено {value}")]
    NonPositive { name: &'static str, value: String },

    #[error("число бит должно быть не меньше {min}, получено {got}")]
    TooFewBits { min: u32, got: u32 },

    #[error("по условию большие числа должны превышать 2^64, поэтому n_bits ≥ 65 (получено {got})")]
    NotLargeEnough { got: u32 },

    #[error("первообразный корень не существует для модуля n = {n}")]
    NoPrimitiveRoot { n: String },

    #[error("исчерпан лимит итераций генерации простого ({tries})")]
    PrimeGenExhausted { tries: u32 },

    #[error("секретный показатель X должен лежать в [2; n-2], получено {value}")]
    PrivateOutOfRange { value: String },
}
