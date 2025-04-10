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
class EmptyTextError(DomainError): ...


@dataclass(eq=False)
class TitleTooLongError(DomainError): ...


@dataclass(eq=False)
class BadChatTypeError(DomainError): ...
