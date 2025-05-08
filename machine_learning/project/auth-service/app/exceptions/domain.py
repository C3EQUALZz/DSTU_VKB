from abc import ABC
from dataclasses import dataclass
from http import HTTPStatus

from app.exceptions.base import BaseAppError


@dataclass(eq=False)
class DomainError(BaseAppError, ABC):
    @property
    def status(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value


@dataclass(eq=False)
class EmptyFieldError(DomainError):
    @property
    def message(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value


@dataclass(eq=False)
class UserNameCantBeDigitError(DomainError):
    @property
    def message(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value


@dataclass(eq=False)
class UserNameCantContainsDigitError(DomainError):
    @property
    def message(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value


@dataclass(eq=False)
class UserSurnameCantContainsDigitError(DomainError):
    @property
    def message(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value


@dataclass(eq=False)
class IncorrectUserEmailError(DomainError):
    @property
    def message(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value


@dataclass(eq=False)
class IncorrectLengthPasswordError(DomainError):
    @property
    def message(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value


@dataclass(eq=False)
class UnsupportedRoleError(DomainError):
    @property
    def message(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value
