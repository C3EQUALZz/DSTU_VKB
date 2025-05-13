import re
from dataclasses import dataclass
from typing import override

from app.domain.values.base import BaseValueObject
from app.exceptions.domain import WrongUserRole, EmptyEmailError, InvalidEmailError, EmptyPasswordError, \
    InvalidPasswordLengthError


@dataclass
class Role(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if self.value not in ("bot", "user", "admin"):
            raise WrongUserRole(f"Bad role of user: {self.value}")

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass
class Email(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if not self.value:
            raise EmptyEmailError("Email is empty")

        email_validate_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not re.match(email_validate_pattern, self.value):
            raise InvalidEmailError(f"The provided email is invalid {self.value}")

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass
class Password(BaseValueObject[bytes]):
    value: bytes

    @override
    def validate(self) -> None:
        if not self.value:
            raise EmptyPasswordError("Password is empty")

        value_length = len(self.value)

        if value_length not in range(3, 100):
            raise InvalidPasswordLengthError(f"Password length is invalid: {str(value_length)}")

    @override
    def as_generic_type(self) -> bytes:
        return self.value
