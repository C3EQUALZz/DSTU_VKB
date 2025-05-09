from http import HTTPStatus

from app.exceptions.base import BaseAppError
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import override


@dataclass(eq=False)
class InfrastructureError(BaseAppError, ABC):
    @override
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value


@dataclass(eq=False)
class TopicNotFoundInFactoryError(InfrastructureError): ...


@dataclass(eq=False)
class UnknownTopicError(InfrastructureError): ...
