from abc import abstractmethod
from typing import Protocol

from app.views.base import IView


class IPresenter(Protocol):
    @abstractmethod
    def attach_view(self, view: IView) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_activate(self) -> None:
        """Вызывается при активации презентера"""
        raise NotImplementedError
