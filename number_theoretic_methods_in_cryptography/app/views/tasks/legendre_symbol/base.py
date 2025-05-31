from abc import abstractmethod
from typing import Protocol, TYPE_CHECKING, Iterable

from app.views.tasks.base import ITaskView

if TYPE_CHECKING:
    from app.presenters.tasks.legendre_symbol.base import ILegendrePresenter  # type: ignore


class ILegendreView(ITaskView["ILegendrePresenter"], Protocol):
    @abstractmethod
    def get_variant_number(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def set_n(self, n: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_p(self, p: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_legendre_result(self, n: int, p: int, result: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_logs(self, logs: Iterable[str]) -> None:
        raise NotImplementedError
