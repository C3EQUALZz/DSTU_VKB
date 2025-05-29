from abc import abstractmethod
from typing import Protocol


class IView(Protocol):
    @abstractmethod
    def show(self) -> None:
        """Отображает представление"""
        raise NotImplementedError

    @abstractmethod
    def hide(self) -> None:
        """Скрывает представление"""
        raise NotImplementedError
