import logging
import re
from dataclasses import dataclass
from typing import override, Final

from app.domain.values.base import BaseValueObject
from app.exceptions.domain import EmptyFieldError, UserNameCantBeDigitError, UserNameCantContainsDigitError, \
    UserSurnameCantContainsDigitError, IncorrectUserEmailError, IncorrectLengthPasswordError, UnsupportedRoleError

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass
class UserName(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError(f"UserName value must be a string, not a {type(self.value)}")

        if not self.value or self.value.isspace():
            raise EmptyFieldError("Username field can't be empty, please provide some information")

        if self.value.isdigit():
            raise UserNameCantBeDigitError("User name can't be digit, please alphabetic symbols")

        if re.match(r"\d", self.value):
            raise UserNameCantContainsDigitError("User name can't contains digit")

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass
class UserSurname(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError(f"UserSurname value must be a string, not a {type(self.value)}")

        if not self.value or self.value.isspace():
            raise EmptyFieldError("Surname field can't be empty, please provide some information")

        if self.value.isdigit():
            raise UserSurnameCantContainsDigitError("Surname can't contain digit")

        if re.match(r"\d", self.value):
            raise UserSurnameCantContainsDigitError("Surname can't contain digit")

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass
class UserEmail(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError(f"UserEmail value must be a string, not a {type(self.value)}")

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.value):
            raise IncorrectUserEmailError(f"UserEmail value {self.value} is not a valid email address")

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass
class UserPassword(BaseValueObject[str]):
    value: bytes

    @override
    def validate(self) -> None:
        if not isinstance(self.value, bytes):
            raise TypeError(f"UserPassword value must be a bytes, not a {type(self.value)}")

        if self.value.isspace() or not self.value:
            raise EmptyFieldError("Password field can't be empty, please provide some information")

        if 3 <= len(self.value) <= 255:
            raise IncorrectLengthPasswordError(
                "Password field can't contain less than 255 characters and more than 3 characters")

    @override
    def as_generic_type(self) -> bytes:
        return bytes(self.value)


@dataclass
class UserRole(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError(f"UserRole value must be a string, not a {type(self.value)}")

        if self.value not in ("user", "admin"):
            raise UnsupportedRoleError(f"{self.value} is not a valid role. It can be only user or admin")

    @override
    def as_generic_type(self) -> str:
        return str(self.value)
