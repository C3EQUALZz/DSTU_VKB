from abc import abstractmethod
from typing import Protocol, TypeVar

from app.presenters.tasks.base import ITaskPresenter

T = TypeVar("T", bound=ITaskPresenter)


class IView(Protocol[T]):
    @abstractmethod
    def show(self) -> None:
        """Отображает представление"""
        raise NotImplementedError

    @abstractmethod
    def hide(self) -> None:
        """Скрывает представление"""
        raise NotImplementedError

    @abstractmethod
    def attach_presenter(self, presenter: T) -> None:
        raise NotImplementedError
