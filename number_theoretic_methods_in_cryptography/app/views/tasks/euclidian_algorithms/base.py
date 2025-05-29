from abc import abstractmethod
from typing import Protocol

from app.presenters.tasks.euclidian_algorithms.base import IGCDPresenter
from app.views.base import IView


class IGCDView(IView[IGCDPresenter], Protocol):
    @abstractmethod
    def set_strategies(self, strategies: list[str]) -> None: ...

    @abstractmethod
    def get_inputs(self) -> tuple[str, str]: ...

    @abstractmethod
    def get_selected_strategy(self) -> str: ...

    @abstractmethod
    def display_result(self, result: str) -> None: ...

    @abstractmethod
    def display_logs(self, logs: list[str]) -> None: ...

    @abstractmethod
    def show_error(self, message: str) -> None: ...

    @abstractmethod
    def attach_presenter(self, presenter: IGCDPresenter) -> None: ...
