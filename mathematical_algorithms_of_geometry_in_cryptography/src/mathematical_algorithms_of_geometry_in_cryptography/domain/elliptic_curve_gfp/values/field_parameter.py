from dataclasses import dataclass

from mathematical_algorithms_of_geometry_in_cryptography.domain.common.values.base import BaseValueObject
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.errors.elliptic_curve_gfp_errors import (
    InvalidFieldParameterError,
)


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class FieldParameter(BaseValueObject):
    """
    Value object representing a prime field parameter p for GF(p).
    
    The parameter must be:
    - A prime number
    - Greater than 1
    """

    value: int

    def _validate(self) -> None:
        """Validate that the field parameter is a prime number."""
        if self.value <= 1:
            msg = f"Field parameter must be greater than 1, got {self.value}"
            raise InvalidFieldParameterError(msg)

        # Simple primality check
        if self.value > 2 and self.value % 2 == 0:
            msg = f"Field parameter must be prime, got {self.value}"
            raise InvalidFieldParameterError(msg)

        # Check for small primes
        if self.value > 2:
            for i in range(3, int(self.value ** 0.5) + 1, 2):
                if self.value % i == 0:
                    msg = f"Field parameter must be prime, got {self.value}"
                    raise InvalidFieldParameterError(msg)

    def __str__(self) -> str:
        return str(self.value)

    def __int__(self) -> int:
        return self.value

