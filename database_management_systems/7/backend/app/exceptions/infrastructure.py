from abc import ABC
from dataclasses import dataclass
from http import HTTPStatus

from app.exceptions.base import ApplicationException


@dataclass(eq=False)
class InfrastructureException(ApplicationException, ABC):
    @property
    def message(self) -> str:
        return "Infrastructure exception has occurred"

    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value


@dataclass(eq=False)
class AttributeException(InfrastructureException):
    value: str

    @property
    def message(self) -> str:
        return f"ATTRIBUTE_REQUIRED! {self.value} is required"

    @property
    def status(self) -> int:
        return HTTPStatus.BAD_REQUEST.value
