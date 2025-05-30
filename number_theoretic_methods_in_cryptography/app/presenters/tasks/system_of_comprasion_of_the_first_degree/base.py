from typing import Protocol, TYPE_CHECKING
from abc import abstractmethod

from app.presenters.tasks.base import ITaskPresenter

if TYPE_CHECKING:
    from app.views.tasks.system_of_comprasion_of_the_first_degree.base import ICRTView  # type: ignore


class ICRTPresenter(ITaskPresenter["ICRTView"], Protocol):
    @abstractmethod
    def solve_system(self) -> None:
        raise NotImplementedError
