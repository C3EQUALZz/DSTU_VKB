from abc import abstractmethod
from typing import Protocol, Iterable


class IRemainderDivision(Protocol):
    @abstractmethod
    def solve(self, a: int, exponent: int, modulus: int) -> int | None:
        raise NotImplementedError

    @abstractmethod
    def get_logs(self) -> Iterable[str]:
        raise NotImplementedError
