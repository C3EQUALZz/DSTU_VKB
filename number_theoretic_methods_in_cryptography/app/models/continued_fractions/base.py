from abc import abstractmethod
from typing import Protocol, Iterable


class IContinuedFractionModel(Protocol):
    @abstractmethod
    def solve_linear_congruence(self, a: int, b: int, m: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_logs(self) -> Iterable[str]:
        raise NotImplementedError
