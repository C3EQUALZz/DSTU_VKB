import logging
from dataclasses import dataclass, field
from typing import Final

from mathematical_algorithms_of_geometry_in_cryptography.domain.common.entities.base_aggregate import (
    BaseAggregateRoot,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.values.curve_parameters_gfp import (
    CurveParametersGFp,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.values.elliptic_curve_gfp_id import (
    EllipticCurveGFpID,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.values.gfp_point import (
    GFpPoint,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(eq=False, kw_only=True)
class EllipticCurveGFp(BaseAggregateRoot[EllipticCurveGFpID]):
    """
    Aggregate root representing an elliptic curve y² = x³ + ax + b over GF(p).
    
    This aggregate encapsulates:
    - Curve parameters (a, b, p)
    - All points on the curve
    - Order of the curve
    """

    parameters: CurveParametersGFp
    points: list[GFpPoint] = field(default_factory=list)

    @property
    def order(self) -> int:
        """Get the order of the curve (number of points)."""
        return len(self.points)

    def contains_point(self, point: GFpPoint) -> bool:
        """
        Check if a point belongs to the curve.
        
        Args:
            point: The point to check
            
        Returns:
            True if point is on the curve, False otherwise
        """
        return point in self.points


