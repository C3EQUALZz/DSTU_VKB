from dataclasses import dataclass
from typing import Any

from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve.values.singularity_status import (
    SingularityStatus,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class EllipticCurveView:
    """View для отображения результатов генерации эллиптической кривой."""

    a: float
    b: float
    discriminant: float
    singularity_status: SingularityStatus
    is_singular: bool
    upper_branch_points: tuple[dict[str, Any], ...]
    lower_branch_points: tuple[dict[str, Any], ...]


