from abc import ABC
from dataclasses import dataclass
from http import HTTPStatus

from app.exceptions.base import ApplicationException


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
class InvalidUsernameLengthException(DomainException):
    username_value: str

    @property
    def message(self) -> str:
        return f"Username length is invalid: {self.username_value}"


@dataclass(eq=False)
class EmptyUsernameException(DomainException):
    @property
    def message(self) -> str:
        return "Username is empty"


@dataclass(eq=False)
class EmptyPasswordException(DomainException):
    @property
    def message(self) -> str:
        return "Password is empty"


@dataclass(eq=False)
class InvalidPasswordLengthException(DomainException):
    length: str

    @property
    def message(self) -> str:
        return f"Password length is invalid: {self.length}"


@dataclass(eq=False)
class EmptyEmailException(DomainException):
    @property
    def message(self) -> str:
        return "Email is empty"


@dataclass(eq=False)
class InvalidEmailException(DomainException):
    email: str

    @property
    def message(self) -> str:
        return f"The provided email is invalid: {self.email}"


@dataclass(eq=False)
class InvalidOIDException(DomainException):
    oid: str

    @property
    def message(self) -> str:
        return f"The provided OID is invalid: {self.oid}"


@dataclass(eq=False)
class EmptyScoreException(DomainException):
    value: str

    @property
    def message(self) -> str:
        return f"The provided value is empty: {self.value}"
