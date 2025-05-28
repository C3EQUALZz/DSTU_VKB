from dataclasses import dataclass, field
from decimal import Decimal
from typing import Union

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

