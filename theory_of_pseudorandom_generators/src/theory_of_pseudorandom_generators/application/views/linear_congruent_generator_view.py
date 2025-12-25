"""View для линейного конгруэнтного генератора."""

from dataclasses import dataclass

from theory_of_pseudorandom_generators.application.views.polynomial_congruent_generator_view import (
    ConditionCheckResult,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class LinearCongruentGeneratorView:
    """View для отображения результатов работы линейного конгруэнтного генератора."""

    a: int
    b: int
    m: int
    x0: int
    conditions: tuple[ConditionCheckResult, ...]
    is_max_period: bool
    period: int
    start_period_index: int


