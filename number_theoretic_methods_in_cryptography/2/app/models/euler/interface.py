from abc import abstractmethod
from typing import Protocol, Iterable


class EulerModelInterface(Protocol):
    @abstractmethod
    def solve_congruence(self, a: int, b: int, n: int) -> int | None:
        raise NotImplementedError

    @abstractmethod
    def get_logs(self) -> Iterable[str]:
        raise NotImplementedError
