import re
from dataclasses import dataclass
from typing import override

from app.domain.exceptions import (
    EmptyEmail,
    EmptyPassword,
    EmptyUsername,
    InvalidEmail,
    InvalidPasswordLength,
    InvalidUsernameLength,
)
from app.domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Username(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if not self.value:
            raise EmptyUsername()

        value_length = len(self.value)

        if value_length not in range(3, 16):
            raise InvalidUsernameLength(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Email(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if not self.value:
            raise EmptyEmail()

        email_validate_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_validate_pattern, self.value):
            raise InvalidEmail(self.value)

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Password(BaseValueObject[str]):
    value: bytes

    def validate(self) -> None:
        if not self.value:
            raise EmptyPassword()

        value_length = len(self.value)

        if value_length not in range(3, 100):
            raise InvalidPasswordLength(str(value_length))

    def as_generic_type(self) -> str:
        return str(self.value)
