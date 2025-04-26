from abc import ABC
from dataclasses import dataclass
from http import HTTPStatus

from app.exceptions.base import BaseAppError


@dataclass(eq=False)
class InfrastructureError(BaseAppError, ABC):
    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value


@dataclass(eq=False)
class UnregisteredJobError(InfrastructureError):
    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value


@dataclass(eq=False)
class TopicNotFoundInFactoryError(InfrastructureError):
    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value


@dataclass(eq=False)
class UnknownTopicError(InfrastructureError):
    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value
