from abc import abstractmethod
from typing import Protocol, TYPE_CHECKING

from app.presenters.tasks.base import ITaskPresenter

if TYPE_CHECKING:
    from app.views.tasks.quadratic_comparison.base import IQuadraticComparisonView  # type: ignore


class IQuadraticComparisonPresenter(ITaskPresenter["IQuadraticComparisonView"], Protocol):
    @abstractmethod
    def calculate(self) -> None:
        raise NotImplementedError
