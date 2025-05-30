from abc import abstractmethod
from typing import Protocol, TYPE_CHECKING

from app.presenters.tasks.base import ITaskPresenter

if TYPE_CHECKING:
    from app.views.tasks.legendre_and_jacobi_symbols.base import ILegendreJacobiView


class ILegendreJacobiPresenter(ITaskPresenter["ILegendreJacobiView"], Protocol):
    @abstractmethod
    def calculate(self) -> None:
        raise NotImplementedError
