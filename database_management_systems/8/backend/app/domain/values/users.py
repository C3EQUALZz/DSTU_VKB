import re
from dataclasses import dataclass
from typing import override

from app.domain.exceptions import (
    EmptyEmailException,
    EmptyPasswordException,
    EmptyUsernameException,
    InvalidEmailException,
    InvalidPasswordLengthException,
    InvalidUsernameLengthException,
)
from app.domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Username(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if not self.value:
            raise EmptyUsernameException()

        value_length = len(self.value)

        if value_length not in range(3, 16):
            raise InvalidUsernameLengthException(self.value)

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Email(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if not self.value:
            raise EmptyEmailException()

        email_validate_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_validate_pattern, self.value):
            raise InvalidEmailException(self.value)

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Password(BaseValueObject[bytes]):
    value: bytes

    @override
    def validate(self) -> None:
        if not self.value:
            raise EmptyPasswordException()

        value_length = len(self.value)

        if value_length not in range(3, 100):
            raise InvalidPasswordLengthException(str(value_length))

    @override
    def as_generic_type(self) -> bytes:
        return self.value
