from abc import ABC
from dataclasses import dataclass
from http import HTTPStatus

from app.exceptions.base import BaseAppException


@dataclass(eq=False)
class DomainException(BaseAppException, ABC):
    @property
    def message(self) -> str:
        return "Exception on domain layer"

    @property
    def status(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value

    @property
    def headers(self) -> dict[str, str] | None:
        return None


@dataclass(eq=False)
class UnsupportedFileObjectExtensionException(DomainException):
    @property
    def message(self) -> str:
        return "Unsupported file object extension"

    @property
    def status(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value


@dataclass(eq=False)
class UnSupportedTypeOfFileException(DomainException):
    @property
    def message(self) -> str:
        return "Unsupported type of file object. It can be only file or directory."

    @property
    def status(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value
