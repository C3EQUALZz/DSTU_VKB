from dataclasses import dataclass
from typing import Any

from mathematical_algorithms_of_geometry_in_cryptography.domain.common.values.base import BaseValueObject


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class SequenceResult(BaseValueObject):
    """
    Value object representing the result of pseudorandom sequence generation.
    
    Attributes:
        sequence: List of generated points
        period: Period of the sequence
        binary_sequence: Binary sequence from least significant bits of y-coordinates
    """

    sequence: tuple[dict[str, Any], ...]
    period: int
    binary_sequence: str

    def _validate(self) -> None:
        """Validate that the sequence result is valid."""
        if self.period < 0:
            msg = f"Period must be non-negative, got {self.period}"
            raise ValueError(msg)

    def __str__(self) -> str:
        return f"SequenceResult(period={self.period}, binary_length={len(self.binary_sequence)})"

