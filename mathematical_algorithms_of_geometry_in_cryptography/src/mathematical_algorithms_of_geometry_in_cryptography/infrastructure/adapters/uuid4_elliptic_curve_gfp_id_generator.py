from typing import cast
from uuid import uuid4

from typing_extensions import override

from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.ports.elliptic_curve_gfp_id_generator import (
    EllipticCurveGFpIDGenerator,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.values.elliptic_curve_gfp_id import (
    EllipticCurveGFpID,
)


class UUID4EllipticCurveGFpIDGenerator(EllipticCurveGFpIDGenerator):
    @override
    def __call__(self) -> EllipticCurveGFpID:
        return cast(EllipticCurveGFpID, uuid4())

