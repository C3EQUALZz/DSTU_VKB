"""View для генератора Фибоначчи на регистрах сдвига."""

from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class FibonacciGeneratorView:
    """View для отображения результатов работы генератора Фибоначчи."""

    polynomial_coefficients: tuple[int, ...]
    start_state: tuple[int, ...]
    shift: int
    column_index: int
    transition_matrix_t: tuple[tuple[int, ...], ...]
    transition_matrix_v: tuple[tuple[int, ...], ...]
    binary_sequence: tuple[str, ...]
    states_sequence: tuple[tuple[int, ...], ...]  # Последовательность состояний регистра
    decimal_sequence: tuple[int, ...]
    period: int
    max_period: int
    is_max_period: bool
    gcd_s_k: int

