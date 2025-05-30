from abc import abstractmethod
from typing import Protocol, TYPE_CHECKING

from app.presenters.tasks.base import ITaskPresenter

if TYPE_CHECKING:
    from app.views.tasks.remainder_division.base import IRemainderDivisionView  # type: ignore


class IRemainderDivisionPresenter(ITaskPresenter["IRemainderDivisionView"], Protocol):
    @abstractmethod
    def calculate(self) -> None:
        raise NotImplementedError
