from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Iterable
from typing import Union

from app.core.registry import LogRegistry

NumberType = Union[int, float, complex, Decimal]


@dataclass(frozen=True)
class ResultDTO:
    greatest_common_divisor: NumberType
    x: NumberType | None = field(default_factory=lambda: None)
    y: NumberType | None = field(default_factory=lambda: None)

    def __str__(self) -> str:
        if self.x is None or self.y is None:
            return f"НОД = {self.greatest_common_divisor}"
        return f"НОД = {self.greatest_common_divisor}. Коэффициенты Безу: x = {self.x}, y = {self.y}"


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
