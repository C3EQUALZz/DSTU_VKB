from dataclasses import dataclass
from typing import Any

from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.values.gfp_point import (
    GFpPoint,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class EllipticCurveGFpView:
    """View для отображения результатов работы с эллиптической кривой над GF(p)."""

    a: int
    b: int
    p: int
    order: int
    points: tuple[dict[str, Any], ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class PointOperationView:
    """View для отображения результата операции с точками."""

    result: str
    result_point: GFpPoint

