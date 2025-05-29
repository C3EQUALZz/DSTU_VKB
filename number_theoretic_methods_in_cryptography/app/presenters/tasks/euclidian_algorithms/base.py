from abc import abstractmethod
from typing import Protocol

from app.presenters.tasks.base import ITaskPresenter


class IGCDPresenter(ITaskPresenter, Protocol):
    @abstractmethod
    def on_calculate(self) -> None:
        raise NotImplementedError
