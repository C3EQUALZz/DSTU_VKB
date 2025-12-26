import logging
from dataclasses import dataclass, field
from typing import Final, Optional

from mathematical_algorithms_of_geometry_in_cryptography.domain.common.entities.base_aggregate import (
    BaseAggregateRoot,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.values.function_expression import (
    FunctionExpression,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.values.initial_value import (
    InitialValue,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.values.number import (
    Number,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.values.pollard_rho_id import (
    PollardRhoID,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.values.step_result import (
    StepResult,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(eq=False, kw_only=True)
class PollardRhoTest(BaseAggregateRoot[PollardRhoID]):
    """
    Aggregate root representing a Pollard's Rho algorithm execution.
    
    This aggregate encapsulates:
    - The number to factor
    - Initial value c
    - Function expression f(x)
    - All step results
    - The found divisor (if any)
    """

    number: Number
    initial_value: InitialValue
    function_expression: FunctionExpression
    steps: list[StepResult] = field(default_factory=list)
    divisor: Optional[int] = field(default=None)
    is_complete: bool = field(default=False)

    def add_step(self, step: StepResult) -> None:
        """
        Add a step result to the aggregate.
        
        Args:
            step: The step result to add
        """
        if self.is_complete:
            msg = "Cannot add step to a completed test"
            raise ValueError(msg)

        if step.step_number != len(self.steps) + 1:
            msg = (
                f"Expected step {len(self.steps) + 1}, "
                f"got {step.step_number}"
            )
            raise ValueError(msg)

        self.steps.append(step)

        # If d != 1 and d != n, we found a divisor
        if step.d != 1 and step.d != int(self.number):
            self.divisor = step.d
            self.is_complete = True

    def mark_complete_no_divisor(self) -> None:
        """Mark the test as complete without finding a divisor (d == n)."""
        self.is_complete = True

    @property
    def steps_count(self) -> int:
        """Get the number of completed steps."""
        return len(self.steps)

