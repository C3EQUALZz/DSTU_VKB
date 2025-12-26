import logging
from dataclasses import dataclass, field
from math import isnan
from typing import Final

from mathematical_algorithms_of_geometry_in_cryptography.domain.common.entities.base_aggregate import (
    BaseAggregateRoot,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve.values.curve_parameters import (
    CurveParameters,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve.values.elliptic_curve_id import (
    EllipticCurveID,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve.values.point import (
    Point,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve.values.singularity_status import (
    SingularityStatus,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(eq=False, kw_only=True)
class EllipticCurve(BaseAggregateRoot[EllipticCurveID]):
    """
    Aggregate root representing an elliptic curve y² = x³ + ax + b.
    
    This aggregate encapsulates:
    - Curve parameters (a, b)
    - Singularity status
    - Discriminant value
    - Points on the curve (upper and lower branches)
    """

    parameters: CurveParameters
    singularity_status: SingularityStatus
    discriminant: float
    upper_branch_points: list[Point] = field(default_factory=list)
    lower_branch_points: list[Point] = field(default_factory=list)

    @property
    def is_singular(self) -> bool:
        """Check if the curve is singular."""
        return self.singularity_status == SingularityStatus.SINGULAR

    @property
    def is_non_singular(self) -> bool:
        """Check if the curve is non-singular."""
        return self.singularity_status == SingularityStatus.NON_SINGULAR

    def get_valid_points(self) -> tuple[list[Point], list[Point]]:
        """
        Get only valid points (excluding NaN values).
        
        Returns:
            Tuple of (upper_branch_valid_points, lower_branch_valid_points)
        """
        upper_valid = [p for p in self.upper_branch_points if p.is_valid]
        lower_valid = [p for p in self.lower_branch_points if p.is_valid]
        return upper_valid, lower_valid

