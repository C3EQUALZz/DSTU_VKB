from abc import abstractmethod
from typing import Protocol

from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve.values.elliptic_curve_id import (
    EllipticCurveID,
)


class EllipticCurveIDGenerator(Protocol):
    @abstractmethod
    def __call__(self) -> EllipticCurveID:
        ...


