from typing import cast
from uuid import uuid4

from typing_extensions import override

from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.ports.pollard_rho_id_generator import (
    PollardRhoIDGenerator
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.values.pollard_rho_id import PollardRhoID


class UUID4PollardRhoIDGenerator(PollardRhoIDGenerator):
    @override
    def __call__(self) -> PollardRhoID:
        return cast(PollardRhoID, uuid4())
