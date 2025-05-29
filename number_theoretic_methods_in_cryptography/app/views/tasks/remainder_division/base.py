from abc import abstractmethod
from typing import Iterable, Protocol, TYPE_CHECKING

from app.views.base import IView

if TYPE_CHECKING:
    from app.presenters.tasks.remainder_division.base import IRemainderDivisionPresenter


class IRemainderDivisionView(IView["IRemainderDivisionPresenter"], Protocol):
    @abstractmethod
    def get_a(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_b(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_k(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_m(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_n(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def set_result1(self, text: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_result2(self, text: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_sum_result(self, text: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def show_logs(self, logs: Iterable[str]) -> None:
        raise NotImplementedError

    @abstractmethod
    def show_error(self, message: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def clear_logs(self) -> None:
        raise NotImplementedError
