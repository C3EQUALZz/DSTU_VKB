from abc import ABC
from dataclasses import dataclass
from http import HTTPStatus

from app.exceptions import ApplicationException


@dataclass(eq=False)
class DomainException(ApplicationException, ABC):
    @property
    def message(self) -> str:
        return "Exception on domain layer"

    @property
    def status(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value


@dataclass(eq=False)
class CastException(DomainException):
    text: str

    @property
    def message(self) -> str:
        return f"Failed to cast field {self.text}"


@dataclass(eq=False)
class InvalidUsernameLength(DomainException):
    username_value: str

    @property
    def message(self) -> str:
        return f"Username length is invalid: {self.username_value}"


@dataclass(eq=False)
class EmptyUsername(DomainException):
    @property
    def message(self) -> str:
        return "Username is empty"


@dataclass(eq=False)
class EmptyPassword(DomainException):
    @property
    def message(self) -> str:
        return "Password is empty"


@dataclass(eq=False)
class InvalidPasswordLength(DomainException):
    length: str

    @property
    def message(self) -> str:
        return f"Password length is invalid: {self.length}"


@dataclass(eq=False)
class EmptyEmail(DomainException):
    @property
    def message(self) -> str:
        return "Email is empty"


@dataclass(eq=False)
class InvalidEmail(DomainException):
    email: str

    @property
    def message(self) -> str:
        return f"The provided email is invalid: {self.email}"
