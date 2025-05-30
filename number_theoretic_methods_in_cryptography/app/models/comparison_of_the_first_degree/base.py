from abc import abstractmethod
from typing import Protocol, Iterable


class ILinearCongruenceSolver(Protocol):
    @abstractmethod
    def solve(self, coefficient: int, constant_term: int, modulus: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_logs(self) -> Iterable[str]:
        raise NotImplementedError
