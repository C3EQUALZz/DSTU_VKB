import re
from dataclasses import dataclass
from email.utils import parseaddr
from pathlib import Path
from typing import override

from app.domain.values.base import BaseValueObject
from app.exceptions.domain import BadFormatEmailError, MalformedEmailError, EmptyFieldError, BadLengthError


@dataclass
class Email(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("Please provide a string value, not another")

        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', self.value):
            raise BadFormatEmailError(self.value)

        parsed_string: tuple[str, str] = parseaddr(self.value)

        if parsed_string[1].isspace() or parsed_string[1] == "" or len(parsed_string[0]) > 0:
            raise MalformedEmailError(self.value)

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass
class TemplateName(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("Please provide a string value, not another type: %s", type(self.value))

        if not self.value.endswith(".html"):
            raise ValueError("Wrong extension of file: %s", Path(self.value).suffix)

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass
class EmailSubject(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("Please provide a string value, not another type: %s", type(self.value))

        if self.value.isspace() or self.value == "":
            raise EmptyFieldError("Please provide some info")

        if not 1 < len(self.value) < 100:
            raise BadLengthError("Please provide email length in range 1 to 100")

    @override
    def as_generic_type(self) -> str:
        return str(self.value)
