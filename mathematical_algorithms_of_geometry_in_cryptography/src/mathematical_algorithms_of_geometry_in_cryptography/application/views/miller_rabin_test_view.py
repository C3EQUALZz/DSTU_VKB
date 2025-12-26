from dataclasses import dataclass
from typing import Any

from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin.values.test_result import (
    PrimalityStatus,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class MillerRabinTestView:
    """View для отображения результатов теста Миллера-Рабина."""

    number: int
    iterations_count: int
    is_complete: bool
    is_probably_prime: bool
    is_composite: bool
    results: tuple[dict[str, Any], ...]

