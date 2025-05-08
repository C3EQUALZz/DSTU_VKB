from typing import override
from dataclasses import dataclass
from app.domain.values.base import BaseValueObject
from app.exceptions.domain import EmptyFieldError, BadLengthError


@dataclass
class EmailBodyTitle(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("Please provide a string value, not another type %s", type(self.value))

        if self.value.isspace() or self.value == "":
            raise EmptyFieldError("Please provide some info, not empty string")

        if not 1 < len(self.value) < 255:
            raise BadLengthError("Please provide a string of length less than 255")

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass
class EmailBodyMessage(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("Please provide a string value, not another type %s", type(self.value))

        if self.value.isspace() or self.value == "":
            raise EmptyFieldError("Please provide some info, not empty string")

    @override
    def as_generic_type(self) -> str:
        return str(self.value)
