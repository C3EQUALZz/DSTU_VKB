from typing import Protocol, Iterable, TYPE_CHECKING
from abc import abstractmethod
from app.views.tasks.base import ITaskView

if TYPE_CHECKING:
    from app.presenters.tasks.system_of_comprasion_of_the_first_degree.base import ICRTPresenter


class ICRTView(ITaskView["ICRTPresenter"], Protocol):
    @abstractmethod
    def get_remainders(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def get_moduli(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def show_logs(self, logs: Iterable[str]) -> None:
        raise NotImplementedError