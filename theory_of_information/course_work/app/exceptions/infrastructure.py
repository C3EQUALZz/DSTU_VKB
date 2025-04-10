from abc import ABC
from dataclasses import dataclass
from http import HTTPStatus

from app.exceptions.base import BaseAppException


@dataclass(eq=False)
class InfrastructureException(BaseAppException, ABC):
    @property
    def message(self) -> str:
        return "Infrastructure exception has occurred"

    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value

    @property
    def headers(self) -> dict[str, str] | None:
        return None


@dataclass(eq=False)
class BadDataException(InfrastructureException):
    value: str

    @property
    def message(self) -> str:
        return f"Bad data exception has occurred. Info: {self.value}"

    @property
    def status(self) -> int:
        return HTTPStatus.BAD_REQUEST.value
