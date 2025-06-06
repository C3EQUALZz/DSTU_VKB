from abc import abstractmethod
from typing import Protocol, TYPE_CHECKING

from app.presenters.tasks.base import ITaskPresenter

if TYPE_CHECKING:
    from app.views.tasks.euclidian_algorithms.base import IGCDView


class IGCDPresenter(ITaskPresenter["IGCDView"], Protocol):
    @abstractmethod
    def on_calculate(self) -> None:
        raise NotImplementedError
