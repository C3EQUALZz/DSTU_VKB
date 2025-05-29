from abc import abstractmethod
from typing import Protocol

from app.views.interface import ViewInterface


class PresenterInterface(Protocol):
    @abstractmethod
    def attach_view(self, view: ViewInterface) -> None:
        raise NotImplementedError

    @abstractmethod
    def calculate(self) -> None:
        raise NotImplementedError
