from dataclasses import dataclass
from typing import override

from app.domain.values.base import BaseValueObject
from app.exceptions.domain import NumberCannotBeNegativeError, WrongTypeError


@dataclass
class PositiveNumber(BaseValueObject[int]):
    value: int

    @override
    def validate(self) -> None:
        if self.value < 0:
            raise NumberCannotBeNegativeError(f"{self.value} is negative")

        if not isinstance(self.value, int):
            raise WrongTypeError(f"{self.value} is not int, type: {type(self.value)}")

    @override
    def as_generic_type(self) -> int:
        return int(self.value)
