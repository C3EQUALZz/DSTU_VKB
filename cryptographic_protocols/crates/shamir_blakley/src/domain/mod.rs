pub mod blakley;
pub mod exact;
pub mod linear;
pub mod shamir;

use thiserror::Error;

#[derive(Debug, Error, PartialEq, Eq)]
pub enum DomainError {
    #[error("нужно не менее трёх долей")]
    TooFewShares,
    #[error("координаты x долей Шамира должны различаться")]
    DuplicateAbscissa,
    #[error("размеры матрицы и правой части не совпадают")]
    InvalidSystem,
    #[error("система не имеет единственного решения")]
    DegenerateSystem,
    #[error("доли противоречат друг другу")]
    InconsistentShares,
    #[error("доли Шамира не лежат на полиноме степени не выше двух")]
    NotQuadratic,
    #[error("деление на нуль")]
    DivisionByZero,
}
