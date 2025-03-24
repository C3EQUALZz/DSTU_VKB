from dataclasses import dataclass
from http import HTTPStatus

from app.exceptions.base import BaseAppException


@dataclass(eq=False)
class ApplicationException(BaseAppException):
    @property
    def message(self) -> str:
        return "Exception on application layer has been occurred"

    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value

    @property
    def headers(self) -> dict[str, str] | None:
        return None


@dataclass(eq=False)
class EmptyCredentialsException(ApplicationException):
    @property
    def message(self) -> str:
        return "Credentials for auth cannot be empty"

    @property
    def status(self) -> int:
        return HTTPStatus.BAD_REQUEST.value

    @property
    def headers(self) -> dict[str, str] | None:
        return {"WWW-Authenticate": "Bearer"}


@dataclass(eq=False)
class ForbiddenTokenException(ApplicationException):
    @property
    def message(self) -> str:
        return "This token has been revoked. Please get a new token."

    @property
    def status(self) -> int:
        return HTTPStatus.FORBIDDEN.value

    @property
    def headers(self) -> dict[str, str] | None:
        return {"WWW-Authenticate": "Bearer"}


@dataclass(eq=False)
class AuthException(ApplicationException):
    value: str

    @property
    def message(self) -> str:
        return self.value

    @property
    def status(self) -> int:
        return HTTPStatus.FORBIDDEN.value

    @property
    def headers(self) -> dict[str, str] | None:
        return {"WWW-Authenticate": "Bearer"}


@dataclass(eq=False)
class RolePermissionDenyException(ApplicationException):

    @property
    def message(self) -> str:
        return "You don't have enough permissions"

    @property
    def status(self) -> int:
        return HTTPStatus.UNAUTHORIZED.value
