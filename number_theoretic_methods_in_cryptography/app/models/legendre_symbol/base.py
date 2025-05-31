from abc import abstractmethod
from typing import Protocol, Iterable


class ILegendreModel(Protocol):
    @abstractmethod
    def calculate_legendre(self, numerator: int, prime_denominator: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def generate_n_p(self, variant_number: int) -> tuple[int, int]:
        raise NotImplementedError

    @abstractmethod
    def get_logs(self) -> Iterable[str]:
        raise NotImplementedError
