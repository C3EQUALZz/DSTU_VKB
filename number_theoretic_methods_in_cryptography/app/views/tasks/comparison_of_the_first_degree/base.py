from typing import Protocol, TYPE_CHECKING, Iterable
from abc import abstractmethod
from app.views.tasks.base import ITaskView

if TYPE_CHECKING:
    from app.presenters.tasks.comparison_of_the_first_degree.base import IComparisonOfFirstDegreePresenter


class IComparisonOfFirstDegreeView(ITaskView["IComparisonOfFirstDegreePresenter"], Protocol):
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
    def show_logs(self, logs: Iterable[str]) -> None:
        raise NotImplementedError