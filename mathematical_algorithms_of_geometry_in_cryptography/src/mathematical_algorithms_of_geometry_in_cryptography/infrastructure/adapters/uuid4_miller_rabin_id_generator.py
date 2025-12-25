from typing import cast
from uuid import uuid4

from typing_extensions import override

from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin.ports.miller_rabin_id_generator import (
    MillerRabinIDGenerator
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin.values.miller_rabin_id import MillerRabinID


class UUID4MillerRabinIDGenerator(MillerRabinIDGenerator):
    @override
    def __call__(self) -> MillerRabinID:
        return cast(MillerRabinID, uuid4())
