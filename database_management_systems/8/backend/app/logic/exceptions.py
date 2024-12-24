from abc import ABC
from dataclasses import dataclass
from http import HTTPStatus

from app.exceptions import ApplicationException


@dataclass(eq=False)
class LogicException(ApplicationException, ABC):
    @property
    def message(self) -> str:
        return "An logic error has occurred"

    def status_code(self) -> int:
        ...


@dataclass(eq=False)
class UserAlreadyExistsException(LogicException):
    value: str

    @property
    def message(self) -> str:
        return f"User {self.value} already exists"

    @property
    def status(self) -> int:
        return HTTPStatus.CONFLICT.value


@dataclass(eq=False)
class InvalidPasswordException(LogicException):
    @property
    def message(self) -> str:
        return "Invalid password"

    @property
    def status(self) -> int:
        return HTTPStatus.UNAUTHORIZED.value


@dataclass(eq=False)
class MessageBusMessageException(LogicException):
    @property
    def message(self) -> str:
        return "Message bus message should be eiter of Event type, or Command type"

    @property
    def status(self) -> int:
        return HTTPStatus.BAD_REQUEST.value


@dataclass(eq=False)
class UserNotFoundException(LogicException):
    value: str

    @property
    def message(self) -> str:
        return f"User with {self.value=} was not found"

    @property
    def status_code(self) -> int:
        return HTTPStatus.NOT_FOUND.value
