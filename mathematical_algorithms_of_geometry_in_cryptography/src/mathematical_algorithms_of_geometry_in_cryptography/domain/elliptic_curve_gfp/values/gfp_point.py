from dataclasses import dataclass

from mathematical_algorithms_of_geometry_in_cryptography.domain.common.values.base import BaseValueObject


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class GFpPoint(BaseValueObject):
    """
    Value object representing a point on an elliptic curve over GF(p).
    
    Attributes:
        x: x-coordinate (or -1 for infinity point)
        y: y-coordinate (or -1 for infinity point)
    """

    x: int
    y: int

    def _validate(self) -> None:
        """Validate that the point is valid."""
        # Infinity point is represented as (-1, -1)
        if (self.x == -1 and self.y != -1) or (self.x != -1 and self.y == -1):
            msg = "Invalid infinity point representation"
            raise ValueError(msg)

    @property
    def is_infinity(self) -> bool:
        """Check if this is the infinity point."""
        return self.x == -1 and self.y == -1

    def __str__(self) -> str:
        if self.is_infinity:
            return "O"
        return f"({self.x}, {self.y})"

    @staticmethod
    def infinity() -> "GFpPoint":
        """Create the infinity point."""
        return GFpPoint(x=-1, y=-1)


