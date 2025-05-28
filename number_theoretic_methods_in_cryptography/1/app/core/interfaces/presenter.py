from abc import abstractmethod
from typing import Protocol


class GCDPresenterInterface(Protocol):
    @abstractmethod
    def on_calculate(self) -> None:
        ...
