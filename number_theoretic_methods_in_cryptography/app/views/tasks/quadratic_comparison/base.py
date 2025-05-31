from abc import abstractmethod
from typing import Protocol, Iterable, TYPE_CHECKING

from app.views.tasks.base import ITaskView

if TYPE_CHECKING:
    from app.presenters.tasks.quadratic_comparison.base import IQuadraticComparisonPresenter  # type: ignore


class IQuadraticComparisonView(ITaskView["IQuadraticComparisonPresenter"], Protocol):
    @abstractmethod
    def get_number(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_prime(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def set_result(self, result: tuple[int, int]) -> None:
        raise NotImplementedError

    @abstractmethod
    def show_logs(self, logs: Iterable[str]) -> None:
        raise NotImplementedError
