from dataclasses import dataclass

from mathematical_algorithms_of_geometry_in_cryptography.domain.common.values.base import BaseValueObject
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.errors.pollard_rho_errors import (
    InvalidNumberError,
)


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class Number(BaseValueObject):
    """
    Value object representing a number to find a divisor for.
    
    The number must be:
    - Greater than 1
    - Composite (not prime)
    """

    value: int

    def _validate(self) -> None:
        """Validate that the number meets the requirements."""
        if self.value <= 1:
            msg = f"Number must be greater than 1, got {self.value}"
            raise InvalidNumberError(msg)

    def __str__(self) -> str:
        return str(self.value)

    def __int__(self) -> int:
        return self.value


