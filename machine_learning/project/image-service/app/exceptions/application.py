from abc import ABC
from dataclasses import dataclass
from http import HTTPStatus

from app.exceptions.base import BaseAppError


@dataclass(eq=False)
class ApplicationException(BaseAppError, ABC):
    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value


@dataclass(eq=False)
class WrongFileFormatError(ApplicationException):
    @property
    def status(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value


@dataclass(eq=False)
class WrongFileFormatError(ApplicationException):
    @property
    def status(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value


@dataclass(eq=False)
class CantDecodeImageError(ApplicationException):
    @property
    def status(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value


@dataclass(eq=False)
class ImageProcessingError(ApplicationException):
    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value
