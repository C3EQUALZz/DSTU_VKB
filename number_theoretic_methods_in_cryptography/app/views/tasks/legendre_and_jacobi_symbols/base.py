from typing import Protocol, TYPE_CHECKING, Iterable

from app.views.tasks.base import ITaskView
from abc import abstractmethod

if TYPE_CHECKING:
    from app.presenters.tasks.legendre_and_jacobi_symbols.base import ILegendreJacobiPresenter


class ILegendreJacobiView(ITaskView["ILegendreJacobiPresenter"], Protocol):
    @abstractmethod
    def get_a1(self):
        raise NotImplementedError

    @abstractmethod
    def get_b1(self):
        raise NotImplementedError

    @abstractmethod
    def get_a2(self):
        raise NotImplementedError

    @abstractmethod
    def get_b2(self):
        raise NotImplementedError

    @abstractmethod
    def set_legendre_result(self, result: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_legendre_logs(self, logs: Iterable[str]) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_jacobi_result(self, result: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_jacobi_logs(self, logs: Iterable[str]) -> None:
        raise NotImplementedError
