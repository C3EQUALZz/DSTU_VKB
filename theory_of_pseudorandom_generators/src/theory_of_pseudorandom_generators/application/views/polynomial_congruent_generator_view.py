"""View для полиномиального конгруэнтного генератора."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class ConditionCheckResult:
    """Результат проверки одного условия максимального периода."""

    condition_number: int
    description: str
    is_fulfilled: bool
    details: str


@dataclass(frozen=True, slots=True, kw_only=True)
class PolynomialCongruentGeneratorView:
    """View для отображения результатов работы полиномиального конгруэнтного генератора."""

    m: int
    a1: int
    a2: int
    b: int
    x0: int
    conditions: tuple[ConditionCheckResult, ...]
    is_max_period: bool
    period: int
    start_period_index: int


