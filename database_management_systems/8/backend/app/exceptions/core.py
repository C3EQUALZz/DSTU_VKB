from dataclasses import dataclass
from http import HTTPStatus

from app.exceptions.base import ApplicationException


@dataclass(eq=False)
class CacheIdentificationInferenceError(ApplicationException):
    @property
    def message(self) -> str:
        return "Could not infer id for resource being cached."

    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value


@dataclass(eq=False)
class InvalidRequestError(ApplicationException):
    @property
    def message(self) -> str:
        return "Type of request not supported."

    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value


@dataclass(eq=False)
class MissingClientError(ApplicationException):
    @property
    def message(self) -> str:
        return "Client is None."

    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value
