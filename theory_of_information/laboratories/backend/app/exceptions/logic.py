from abc import ABC
from dataclasses import dataclass
from http import HTTPStatus

from app.exceptions.base import ApplicationException


@dataclass(eq=False)
class LogicException(ApplicationException, ABC):
    @property
    def message(self) -> str:
        return "An logic error has occurred"

    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value
