//! Сценарий: применить длинную арифметику к двум числам и (если возможно)
//! сравнить с встроенным `i128` — то самое «вывести проверку обычного
//! сложения и вычитания», что требует условие.

use std::fmt;

use tracing::{debug, info, instrument, warn};

use crate::domain::{BigInt, ParseError, add, sub};

/// Поддерживаемые операции практики.
#[derive(Debug, Clone, Copy)]
pub enum Operation {
    Add,
    Sub,
}

impl Operation {
    pub const fn symbol(self) -> &'static str {
        match self {
            Self::Add => "+",
            Self::Sub => "-",
        }
    }

    fn apply_bigint(self, a: &BigInt, b: &BigInt) -> BigInt {
        match self {
            Self::Add => add(a, b),
            Self::Sub => sub(a, b),
        }
    }

    /// Применяет операцию во встроенной `i128`-арифметике через `checked_*`.
    /// `None`, если операнды или результат не помещаются в `i128`.
    fn apply_i128(self, a: &BigInt, b: &BigInt) -> Option<i128> {
        let a128 = a.to_i128()?;
        let b128 = b.to_i128()?;
        match self {
            Self::Add => a128.checked_add(b128),
            Self::Sub => a128.checked_sub(b128),
        }
    }
}

/// Результат разбора и вычисления операции — для CLI и для тестов.
#[derive(Debug, Clone)]
pub struct OperationReport {
    pub op: Operation,
    pub lhs: BigInt,
    pub rhs: BigInt,
    pub result: BigInt,
    /// Результат встроенной `i128`-арифметики. `None`, если операнды или
    /// результат не помещаются в `i128` — это нормально для длинных чисел.
    pub builtin_result: Option<i128>,
    /// `true`, если оба пути дали один и тот же результат
    /// (и `i128`-проверка была доступна).
    pub builtin_matches: bool,
}

impl fmt::Display for OperationReport {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        writeln!(f, "── {} {} {} ──", self.lhs, self.op.symbol(), self.rhs)?;
        writeln!(f, "BigInt:    {}", self.result)?;
        writeln!(
            f,
            "Разрядов: {} (lhs={}, rhs={})",
            self.result.decimal_digits(),
            self.lhs.decimal_digits(),
            self.rhs.decimal_digits()
        )?;
        match self.builtin_result {
            Some(v) => {
                writeln!(f, "i128:      {v}")?;
                writeln!(
                    f,
                    "Проверка:  {} (встроенная арифметика {})",
                    if self.builtin_matches {
                        "OK ✓ оба пути совпадают"
                    } else {
                        "MISMATCH ✗"
                    },
                    if self.builtin_matches {
                        "согласна"
                    } else {
                        "расходится"
                    }
                )?;
            }
            None => {
                writeln!(
                    f,
                    "i128:      — (результат вне диапазона ±2^127, проверка обычной арифметикой невозможна)"
                )?;
            }
        }
        Ok(())
    }
}

#[derive(Debug, thiserror::Error)]
pub enum VerifyError {
    #[error("не удалось разобрать операнд: {0}")]
    Parse(#[from] ParseError),
}

/// Сервис, инкапсулирующий парсинг и применение операции с логированием.
///
/// Конструируется без зависимостей — пока что чистая обёртка вокруг домена.
/// Хорошо ложится на froodi-DI, если позже понадобится подменять реализацию
/// (например, в e2e-тестах).
#[derive(Debug, Default, Clone)]
pub struct VerifyService;

impl VerifyService {
    pub const fn new() -> Self {
        Self
    }

    /// Парсит две строки и применяет операцию.
    ///
    /// # Errors
    /// Возвращает `VerifyError::Parse`, если хоть один операнд не разобран.
    #[instrument(level = "info", skip(self), fields(op = ?op))]
    pub fn run(&self, op: Operation, lhs: &str, rhs: &str) -> Result<OperationReport, VerifyError> {
        debug!(lhs, rhs, "parsing operands");
        let a: BigInt = lhs.parse()?;
        let b: BigInt = rhs.parse()?;
        debug!(
            lhs_bits = a.bit_length(),
            rhs_bits = b.bit_length(),
            lhs_digits = a.decimal_digits(),
            rhs_digits = b.decimal_digits(),
            "operands parsed"
        );

        let result = op.apply_bigint(&a, &b);
        let builtin_result = op.apply_i128(&a, &b);
        let builtin_matches = match builtin_result {
            Some(v) => result.to_i128() == Some(v),
            None => false,
        };

        if let Some(v) = builtin_result {
            if builtin_matches {
                info!(result = %result, builtin = v, "BigInt совпал с i128");
            } else {
                warn!(result = %result, builtin = v, "BigInt разошёлся с i128 — это баг");
            }
        } else {
            info!(
                result = %result,
                result_digits = result.decimal_digits(),
                "результат вне диапазона i128 — проверка через встроенную арифметику невозможна"
            );
        }

        Ok(OperationReport {
            op,
            lhs: a,
            rhs: b,
            result,
            builtin_result,
            builtin_matches,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn small_add_is_checked_against_i128() {
        let svc = VerifyService::new();
        let r = svc.run(Operation::Add, "100", "200").unwrap();
        assert_eq!(r.result.to_string(), "300");
        assert_eq!(r.builtin_result, Some(300));
        assert!(r.builtin_matches);
    }

    #[test]
    fn small_sub_is_checked_against_i128() {
        let svc = VerifyService::new();
        let r = svc.run(Operation::Sub, "100", "200").unwrap();
        assert_eq!(r.result.to_string(), "-100");
        assert_eq!(r.builtin_result, Some(-100));
        assert!(r.builtin_matches);
    }

    #[test]
    fn very_large_add_has_no_builtin_check() {
        let svc = VerifyService::new();
        let huge = "1".to_string() + &"0".repeat(80);
        let r = svc.run(Operation::Add, &huge, &huge).unwrap();
        assert_eq!(r.result.to_string(), "2".to_string() + &"0".repeat(80));
        assert!(r.builtin_result.is_none());
        assert!(!r.builtin_matches);
    }

    #[test]
    fn parse_error_is_propagated() {
        let svc = VerifyService::new();
        let err = svc.run(Operation::Add, "12abc", "1").unwrap_err();
        assert!(matches!(err, VerifyError::Parse(_)));
    }
}
