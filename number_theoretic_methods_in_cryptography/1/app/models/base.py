from abc import ABC, abstractmethod
from typing import Iterable

from app.core.dto import NumberType, ResultDTO
from app.core.registry import LogRegistry


class BaseGCDStrategy(ABC):
    """
    Базовый класс стратегии для выбора различных поведений вычислений алгоритма.
    Здесь каждый метод должен наследоваться от данного класса, чтобы определить свою логику.
    """

    def __init__(self) -> None:
        self._iterations: int = 0
        self._registry: LogRegistry = LogRegistry()

    @abstractmethod
    def compute(self, a: NumberType, b: NumberType) -> ResultDTO:
        raise NotImplementedError

    @property
    def iterations(self) -> int:
        return self._iterations

    def get_logs(self) -> Iterable[str]:
        return self._registry.logs
