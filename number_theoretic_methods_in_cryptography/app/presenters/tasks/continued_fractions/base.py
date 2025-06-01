from abc import abstractmethod
from typing import Protocol, TYPE_CHECKING

from app.presenters.tasks.base import ITaskPresenter

if TYPE_CHECKING:
    from app.views.tasks.continued_fractions.base import IContinuedFractionView  # type: ignore


class IContinuedFractionPresenter(ITaskPresenter["IContinuedFractionView"], Protocol):
    @abstractmethod
    def calculate(self) -> None:
        raise NotImplementedError
