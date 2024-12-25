from abc import ABC
from dataclasses import dataclass
from http import HTTPStatus

from app.exceptions import ApplicationException


@dataclass(eq=False)
class InfrastructureException(ApplicationException, ABC):
    @property
    def message(self) -> str:
        return "Infrastructure exception has occurred"

    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value


@dataclass(eq=False)
class InvalidToken(InfrastructureException):
    @property
    def message(self) -> str:
        return "Token is invalid"

    @property
    def status(self) -> int:
        return HTTPStatus.UNAUTHORIZED.value


@dataclass(eq=False)
class ExpiredToken(InfrastructureException):
    @property
    def message(self) -> str:
        return "Token has expired"

    @property
    def status(self) -> int:
        return HTTPStatus.UNAUTHORIZED.value


@dataclass(eq=False)
class AttributeException(InfrastructureException):
    @property
    def message(self) -> str:
        return "USER_ATTRIBUTE_REQUIRED! User id or email or username is required"

    @property
    def status(self) -> int:
        return HTTPStatus.BAD_REQUEST.value


@dataclass(eq=False)
class UserNotFoundError(InfrastructureException):
    value: str

    @property
    def message(self) -> str:
        return f"Couldn't find user {self.value}"

    @property
    def status(self) -> int:
        return HTTPStatus.NOT_FOUND.value
