from abc import abstractmethod
from typing import Protocol

from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.values.elliptic_curve_gfp_id import (
    EllipticCurveGFpID,
)


class EllipticCurveGFpIDGenerator(Protocol):
    @abstractmethod
    def __call__(self) -> EllipticCurveGFpID:
        ...

