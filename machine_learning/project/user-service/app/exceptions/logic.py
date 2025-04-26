from abc import ABC
from dataclasses import dataclass
from http import HTTPStatus

from app.exceptions.base import BaseAppError


@dataclass(eq=False)
class LogicError(BaseAppError, ABC):
    @property
    def message(self) -> str:
        return "An logic error has occurred"


@dataclass(eq=False)
class MessageBusMessageError(LogicError):
    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value
