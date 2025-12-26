from abc import abstractmethod
from typing import Protocol

from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.values.pollard_rho_id import (
    PollardRhoID,
)


class PollardRhoIDGenerator(Protocol):
    @abstractmethod
    def __call__(self) -> PollardRhoID:
        ...

