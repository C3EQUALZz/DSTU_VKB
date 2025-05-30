from typing import Protocol, TYPE_CHECKING
from abc import abstractmethod
from app.presenters.tasks.base import ITaskPresenter

if TYPE_CHECKING:
    from app.views.tasks.comparison_of_the_first_degree.base import IComparisonOfFirstDegreeView

class IComparisonOfFirstDegreePresenter(ITaskPresenter["IComparisonOfFirstDegreeView"], Protocol):
    @abstractmethod
    def solve_congruence(self) -> None:
        raise NotImplementedError
