from dataclasses import dataclass
from typing import override
import re

from app.domain.values.base import BaseValueObject
from app.exceptions.domain import EmptyGenderException, PhoneNumberException, UnExistingGenderException


@dataclass
class Gender(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if not self.value:
            raise EmptyGenderException()

        if self.value not in ("male", "female"):
            raise UnExistingGenderException(self.value)

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass
class PhoneNumber(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        pattern = r"^([+]?[\s0-9]+)?(\d{3}|[(]?[0-9]+[)])?([-]?[\s]?[0-9])+$"

        if not re.match(pattern, self.value):
            raise PhoneNumberException()

    @override
    def as_generic_type(self) -> str:
        return str(self.value)
