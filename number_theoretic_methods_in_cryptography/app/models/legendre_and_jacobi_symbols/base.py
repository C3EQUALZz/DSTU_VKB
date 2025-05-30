from abc import abstractmethod
from typing import Protocol, Iterable


class ILegendreJacobiModel(Protocol):
    @abstractmethod
    def calculate_legendre(self, a: int, p: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def calculate_jacobi(self, a: int, n: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_legendre_logs(self) -> Iterable[str]:
        raise NotImplementedError

    @abstractmethod
    def get_jacobi_logs(self) -> Iterable[str]:
        raise NotImplementedError
