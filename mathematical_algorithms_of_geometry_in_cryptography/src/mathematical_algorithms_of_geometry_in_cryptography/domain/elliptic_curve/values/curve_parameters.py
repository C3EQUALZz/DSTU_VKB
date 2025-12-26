from dataclasses import dataclass

from mathematical_algorithms_of_geometry_in_cryptography.domain.common.values.base import BaseValueObject


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class CurveParameters(BaseValueObject):
    """
    Value object representing parameters of an elliptic curve y² = x³ + ax + b.
    
    Attributes:
        a: Coefficient a
        b: Coefficient b
    """

    a: float
    b: float

    def _validate(self) -> None:
        """Validate that the parameters are valid."""
        # Parameters can be any real numbers, no specific validation needed
        pass

    def __str__(self) -> str:
        return f"CurveParameters(a={self.a}, b={self.b})"

