from abc import abstractmethod
from typing import Protocol, TypeVar

# Обобщаем Presenter
TView = TypeVar("TView", bound="IView")


class ITaskPresenter(Protocol[TView]):
    @abstractmethod
    def attach_view(self, view: TView) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_activate(self) -> None:
        """Вызывается при активации презентера"""
        raise NotImplementedError
