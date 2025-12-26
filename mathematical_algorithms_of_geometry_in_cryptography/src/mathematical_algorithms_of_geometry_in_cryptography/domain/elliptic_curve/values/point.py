from dataclasses import dataclass
from math import isnan

from mathematical_algorithms_of_geometry_in_cryptography.domain.common.values.base import BaseValueObject


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class Point(BaseValueObject):
    """
    Value object representing a point on an elliptic curve.
    
    Attributes:
        x: x-coordinate
        y: y-coordinate (can be NaN if point doesn't exist)
    """

    x: float
    y: float

    def _validate(self) -> None:
        """Validate that the point is valid."""
        # y can be NaN if point doesn't exist on the curve
        pass

    @property
    def is_valid(self) -> bool:
        """Check if the point is valid (y is not NaN)."""
        return not isnan(self.y)

    def __str__(self) -> str:
        if self.is_valid:
            return f"Point(x={self.x}, y={self.y})"
        return f"Point(x={self.x}, y=NaN)"

