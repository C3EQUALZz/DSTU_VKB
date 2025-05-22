from dataclasses import dataclass
from http import HTTPStatus

from app.exceptions.base import BaseAppError


@dataclass(eq=False)
class ApplicationError(BaseAppError):
    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value

    @property
    def headers(self) -> dict[str, str] | None:
        return None


@dataclass(eq=False)
class EmptyCredentialsException(ApplicationError):
    @property
    def status(self) -> int:
        return HTTPStatus.BAD_REQUEST.value

    @property
    def headers(self) -> dict[str, str] | None:
        return {"WWW-Authenticate": "Bearer"}


@dataclass(eq=False)
class ForbiddenTokenException(ApplicationError):
    @property
    def status(self) -> int:
        return HTTPStatus.FORBIDDEN.value

    @property
    def headers(self) -> dict[str, str] | None:
        return {"WWW-Authenticate": "Bearer"}


@dataclass(eq=False)
class AuthException(ApplicationError):
    @property
    def status(self) -> int:
        return HTTPStatus.FORBIDDEN.value

    @property
    def headers(self) -> dict[str, str] | None:
        return {"WWW-Authenticate": "Bearer"}


@dataclass(eq=False)
class RolePermissionDenyException(ApplicationError):
    @property
    def status(self) -> int:
        return HTTPStatus.UNAUTHORIZED.value