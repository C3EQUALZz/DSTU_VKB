use thiserror::Error;

#[derive(Debug, Error)]
pub enum DomainError {
    #[error("в тексте найден символ '{c}' вне 33-буквенного алфавита")]
    OutOfAlphabet { c: char },

    #[error("ключ пуст")]
    EmptyKey,

    #[error("текст слишком короткий для криптоанализа: длина {len}, нужно ≥ {needed}")]
    TextTooShort { len: usize, needed: usize },
}
