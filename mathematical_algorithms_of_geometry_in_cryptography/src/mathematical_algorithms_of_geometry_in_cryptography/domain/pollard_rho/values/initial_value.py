from dataclasses import dataclass

from mathematical_algorithms_of_geometry_in_cryptography.domain.common.values.base import BaseValueObject
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.errors.pollard_rho_errors import (
    InvalidInitialValueError,
)


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class InitialValue(BaseValueObject):
    """
    Value object representing the initial value c for Pollard's Rho algorithm.
    
    The initial value should be:
    - Non-negative
    - Typically small (0, 1, or 2)
    """

    value: int

    def _validate(self) -> None:
        """Validate that the initial value is valid."""
        if self.value < 0:
            msg = f"Initial value must be non-negative, got {self.value}"
            raise InvalidInitialValueError(msg)

    def __str__(self) -> str:
        return str(self.value)

    def __int__(self) -> int:
        return self.value

