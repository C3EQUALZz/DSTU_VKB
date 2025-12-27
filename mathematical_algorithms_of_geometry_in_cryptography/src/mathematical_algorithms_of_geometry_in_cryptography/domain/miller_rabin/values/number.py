from dataclasses import dataclass

from mathematical_algorithms_of_geometry_in_cryptography.domain.common.values.base import BaseValueObject
from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin.errors.miller_rabin_errors import (
    InvalidNumberError,
)


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class Number(BaseValueObject):
    """
    Value object representing a number to be tested for primality.
    
    The number must be:
    - Odd (нечетное)
    - Greater than 5
    """

    value: int

    def _validate(self) -> None:
        """Validate that the number meets the requirements for Miller-Rabin test."""
        if self.value <= 5:
            msg = f"Number must be greater than 5, got {self.value}"
            raise InvalidNumberError(msg)

        if self.value % 2 == 0:
            msg = f"Number must be odd, got {self.value}"
            raise InvalidNumberError(msg)

    def __str__(self) -> str:
        return str(self.value)

    def __int__(self) -> int:
        return self.value



