from abc import abstractmethod
from typing import Protocol


class IMainMenuView(Protocol):
    @abstractmethod
    def show(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def hide(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def register_button(self, name: str) -> None:
        raise NotImplementedError
