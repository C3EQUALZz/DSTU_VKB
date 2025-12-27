from dataclasses import dataclass

from mathematical_algorithms_of_geometry_in_cryptography.domain.common.values.base import BaseValueObject
from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin.errors.miller_rabin_errors import (
    InvalidTestParametersError,
)


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class TestParameters(BaseValueObject):
    """
    Value object representing parameters for a single Miller-Rabin test iteration.
    
    Attributes:
        s: The exponent such that n-1 = 2^s * t
        t: The odd part of n-1
        a: The random base for the test
    """

    s: int
    t: int
    a: int

    def _validate(self) -> None:
        """Validate that the test parameters are valid."""
        if self.s < 0:
            msg = f"Parameter s must be non-negative, got {self.s}"
            raise InvalidTestParametersError(msg)

        if self.t <= 0:
            msg = f"Parameter t must be positive, got {self.t}"
            raise InvalidTestParametersError(msg)

        if self.t % 2 == 0:
            msg = f"Parameter t must be odd, got {self.t}"
            raise InvalidTestParametersError(msg)

        if self.a <= 0:
            msg = f"Parameter a must be positive, got {self.a}"
            raise InvalidTestParametersError(msg)

    def __str__(self) -> str:
        return f"TestParameters(s={self.s}, t={self.t}, a={self.a})"



