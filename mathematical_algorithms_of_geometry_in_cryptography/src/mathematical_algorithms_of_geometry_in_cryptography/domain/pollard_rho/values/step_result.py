from __future__ import annotations

from dataclasses import dataclass

from mathematical_algorithms_of_geometry_in_cryptography.domain.common.values.base import BaseValueObject


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class StepResult(BaseValueObject):
    """
    Value object representing the result of a single step in Pollard's Rho algorithm.
    
    Attributes:
        step_number: The step number (1-based)
        a: Current value of a
        b: Current value of b
        d: GCD(a - b, n)
    """

    step_number: int
    a: int
    b: int
    d: int

    def _validate(self) -> None:
        """Validate that the step result is valid."""
        if self.step_number < 1:
            msg = f"Step number must be at least 1, got {self.step_number}"
            raise ValueError(msg)

    def __str__(self) -> str:
        return (
            f"StepResult(step={self.step_number}, "
            f"a={self.a}, b={self.b}, d={self.d})"
        )

