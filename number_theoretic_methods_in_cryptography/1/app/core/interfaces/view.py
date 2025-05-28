# app/presentation/interfaces.py
from typing import Protocol
from abc import abstractmethod


class GCDViewInterface(Protocol):
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
