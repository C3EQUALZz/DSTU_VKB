from abc import abstractmethod
from typing import Protocol

from app.views.application.menu.base import IMainMenuView


class IMenuPresenter(Protocol):
    @abstractmethod
    def attach_presenter(self, view: IMainMenuView) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_menu_selection(self, algorithm_key: str) -> None:
        raise NotImplementedError
