from app.core.dto import NumberType, ResultDTO
from app.exceptions.models import StrategyNotSetError
from app.models.base import BaseGCDStrategy


class AlgorithmStrategyContext:
    def __init__(self, a: NumberType, b: NumberType) -> None:
        self._a: NumberType = a
        self._b: NumberType = b
        self._strategy: BaseGCDStrategy | None = None

    def set_strategy(self, strategy: BaseGCDStrategy) -> None:
        self._strategy: BaseGCDStrategy = strategy

    def execute(self) -> ResultDTO:
        if self._strategy is None:
            raise StrategyNotSetError('Strategy is not set')
        return self._strategy.compute(self._a, self._b)
