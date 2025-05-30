from abc import abstractmethod
from typing import Protocol, Iterable


class IChineseRemainderSolver(Protocol):
    @abstractmethod
    def solve(self, remainders: list[int], moduli: list[int]) -> tuple[int, int] | None:
        raise NotImplementedError

    @abstractmethod
    def get_logs(self) -> Iterable[str]:
        raise NotImplementedError
