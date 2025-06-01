from abc import abstractmethod
from typing import Protocol

from app.domain.calculators.dtos.base import BaseDTO


class IMetricsCalculator(Protocol[BaseDTO]):
    @abstractmethod
    def calculate(self) -> BaseDTO:
        raise NotImplementedError
