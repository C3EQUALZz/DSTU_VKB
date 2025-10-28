from typing import Protocol, TYPE_CHECKING, Iterable

from app.views.tasks.base import ITaskView
from abc import abstractmethod

if TYPE_CHECKING:
    from app.presenters.tasks.legendre_and_jacobi_symbols.base import ILegendreJacobiPresenter


class ILegendreJacobiView(ITaskView["ILegendreJacobiPresenter"], Protocol):
    @abstractmethod
    def get_numerator(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_denominator(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def set_result(self, symbol_type: str, result: int | str) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_logs(self, logs: Iterable[str]) -> None:
        raise NotImplementedError
