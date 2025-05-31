from typing import Protocol, Iterable
from abc import abstractmethod


class IQuadraticComparisonModel(Protocol):
    @abstractmethod
    def get_logs(self) -> Iterable[str]:
        raise NotImplementedError

    @abstractmethod
    def solve_quadratic_comparison(self, number: int, prime: int) -> tuple[int, int]:
        raise NotImplementedError
