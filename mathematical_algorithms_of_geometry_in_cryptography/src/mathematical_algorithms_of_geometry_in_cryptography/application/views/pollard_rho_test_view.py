from dataclasses import dataclass
from typing import Any, Optional

from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.values.step_result import (
    StepResult,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class PollardRhoTestView:
    """View для отображения результатов алгоритма Полларда."""

    number: int
    initial_value: int
    function_expression: str
    steps_count: int
    is_complete: bool
    divisor: Optional[int]
    steps: tuple[dict[str, Any], ...]


