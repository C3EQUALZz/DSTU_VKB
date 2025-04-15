from abc import ABC
from dataclasses import dataclass
from http import HTTPStatus

from app.exceptions.base import BaseAppError


@dataclass(eq=False)
class ApplicationError(BaseAppError, ABC): ...


@dataclass(eq=False)
class UnregisteredJobError(ApplicationError):
    def status(self) -> int:
        raise HTTPStatus.INTERNAL_SERVER_ERROR.value

