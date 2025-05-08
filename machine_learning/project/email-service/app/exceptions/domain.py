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
class BadFormatEmailError(DomainError):
    ...


@dataclass(eq=False)
class MalformedEmailError(DomainError):
    ...


@dataclass(eq=False)
class EmptyFieldError(DomainError):
    ...


@dataclass(eq=False)
class BadLengthError(DomainError):
    ...
