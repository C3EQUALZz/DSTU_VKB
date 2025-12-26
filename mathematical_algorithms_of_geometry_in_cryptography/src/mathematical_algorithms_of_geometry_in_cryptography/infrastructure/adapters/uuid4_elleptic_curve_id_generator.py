from typing_extensions import override

from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve.ports.elliptic_curve_id_generator import (
    EllipticCurveIDGenerator
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve.values.elliptic_curve_id import (
    EllipticCurveID
)


class UUID4EllipticCurveIDGenerator(EllipticCurveIDGenerator):
    @override
    def __call__(self) -> EllipticCurveID:
        ...
