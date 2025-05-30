from typing import Protocol
from abc import abstractmethod

from app.presenters.tasks.base import ITaskPresenter
from app.views.tasks.base import ITaskView, T


class IMainPresenter(Protocol):
    @abstractmethod
    def register_presenter(self, key: str, presenter_class: type[ITaskPresenter]) -> None:
        raise NotImplementedError

    @abstractmethod
    def activate_presenter(self, key: str, view: ITaskView[T]) -> None:
        raise NotImplementedError
