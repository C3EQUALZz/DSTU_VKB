from abc import abstractmethod
from typing import Protocol

from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin.values.miller_rabin_id import MillerRabinID


class MillerRabinIDGenerator(Protocol):
    @abstractmethod
    def __call__(self) -> MillerRabinID:
        ...
