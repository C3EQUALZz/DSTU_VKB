from typing import Protocol, TYPE_CHECKING, Iterable
from abc import abstractmethod
from app.views.tasks.base import ITaskView

if TYPE_CHECKING:
    from app.presenters.tasks.continued_fractions.base import IContinuedFractionPresenter  # type: ignore


class IContinuedFractionView(ITaskView["IContinuedFractionPresenter"], Protocol):
    @abstractmethod
    def get_a(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_b(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_m(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def set_solution(self, solution: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_logs(self, logs: Iterable[str]) -> None:
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError
