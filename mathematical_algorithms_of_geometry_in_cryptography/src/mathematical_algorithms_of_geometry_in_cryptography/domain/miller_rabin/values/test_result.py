from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

from mathematical_algorithms_of_geometry_in_cryptography.domain.common.values.base import BaseValueObject

if TYPE_CHECKING:
    from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin.values.test_parameters import (
        TestParameters,
    )


class PrimalityStatus(str, Enum):
    """Status of primality test result."""

    PROBABLY_PRIME = "probably_prime"
    COMPOSITE = "composite"


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class TestResult(BaseValueObject):
    """
    Value object representing the result of a single Miller-Rabin test iteration.
    
    Attributes:
        status: Whether the number is probably prime or composite
        iteration: The iteration number (1-based)
        parameters: The test parameters used
        intermediate_values: Dictionary of intermediate calculation values
    """

    status: PrimalityStatus
    iteration: int
    parameters: TestParameters
    intermediate_values: dict[str, int | str]

    def _validate(self) -> None:
        """Validate that the test result is valid."""
        if self.iteration < 1:
            msg = f"Iteration must be at least 1, got {self.iteration}"
            raise ValueError(msg)

    def __str__(self) -> str:
        return (
            f"TestResult(iteration={self.iteration}, "
            f"status={self.status.value}, "
            f"parameters={self.parameters})"
        )

