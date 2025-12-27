from dataclasses import dataclass

from mathematical_algorithms_of_geometry_in_cryptography.domain.common.values.base import BaseValueObject
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.values.field_parameter import (
    FieldParameter,
)


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class CurveParametersGFp(BaseValueObject):
    """
    Value object representing parameters of an elliptic curve y² = x³ + ax + b over GF(p).
    
    Attributes:
        a: Coefficient a
        b: Coefficient b
        p: Prime field parameter
    """

    a: int
    b: int
    p: FieldParameter

    def _validate(self) -> None:
        """Validate that the parameters are valid."""
        p_value = int(self.p)
        # Coefficients should be in range [0, p-1]
        if self.a < 0 or self.a >= p_value:
            msg = f"Coefficient a must be in range [0, {p_value-1}], got {self.a}"
            raise ValueError(msg)

        if self.b < 0 or self.b >= p_value:
            msg = f"Coefficient b must be in range [0, {p_value-1}], got {self.b}"
            raise ValueError(msg)

    def __str__(self) -> str:
        return f"CurveParametersGFp(a={self.a}, b={self.b}, p={self.p})"


