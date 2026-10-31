//! Чистые алгоритмы, без ввода-вывода и логирования.

mod curve;
mod field;

pub use curve::{Curve, EcdhResult, MAX_ENUM_MODULUS, MAX_TABLE_POINTS, MAX_WALK_STEPS, Point};
pub use field::{PrimeField, is_prime};

/// Ошибки входных параметров и ограничений учебных алгоритмов.
#[derive(Debug, thiserror::Error, PartialEq, Eq)]
pub enum Error {
    #[error("модуль p должен быть простым числом > 3, получено {0}")]
    InvalidModulus(u64),
    #[error("вырожденная кривая: 4a³ + 27b² ≡ 0 (mod p)")]
    SingularCurve,
    #[error("точка {0} не принадлежит кривой или её координаты не канонические")]
    InvalidPoint(Point),
    #[error("ноль не имеет обратного элемента в поле")]
    ZeroInverse,
    #[error("полный перебор точек разрешён только при p ≤ {MAX_ENUM_MODULUS}")]
    EnumerationLimit,
    #[error("предел {MAX_WALK_STEPS} сложений исчерпан; точный результат не найден")]
    WalkLimit,
    #[error("таблица ограничена {MAX_TABLE_POINTS} точками, в группе {0}")]
    TableLimit(usize),
    #[error("точка Q не принадлежит циклической подгруппе ⟨P⟩")]
    NoDiscreteLog,
    #[error("для ECDH требуется G ≠ O, 1 ≤ a,b < ord(G) и общий результат ≠ O")]
    InvalidEcdh,
}
