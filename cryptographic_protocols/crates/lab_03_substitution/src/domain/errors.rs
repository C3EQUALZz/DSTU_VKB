use thiserror::Error;

#[derive(Debug, Error)]
pub enum DomainError {
    #[error("шифртекст содержит токен '{token}', не являющийся числом")]
    InvalidToken { token: String },

    #[error("в тексте найден символ '{c}' вне 33-буквенного алфавита")]
    OutOfAlphabet { c: char },
}
