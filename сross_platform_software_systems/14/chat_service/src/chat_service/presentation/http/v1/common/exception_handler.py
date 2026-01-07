import logging
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Final

import pydantic

from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from fastapi.responses import ORJSONResponse

from chat_service.application.errors.base import ApplicationError
from chat_service.application.errors.query_params import PaginationError, SortingError
from chat_service.application.errors.user import UserNotFoundError
from chat_service.domain.common.errors.base import (
    AppError,
    DomainError,
    DomainFieldError,
)
from chat_service.domain.user.errors import (
    ActivationChangeNotPermittedError,
    AuthorizationError,
    RoleChangeNotPermittedError,
)
from chat_service.infrastructure.errors.base import InfrastructureError
from chat_service.infrastructure.errors.transaction_manager import EntityAddError, RepoError, RollbackError

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ExceptionSchema:
    description: str


@dataclass(frozen=True, slots=True)
class ExceptionSchemaRich:
    description: str
    details: list[dict[str, Any]] | None = None


class ExceptionHandler:
    _ERROR_MAPPING: Final[MappingProxyType[type[Exception], int]] = MappingProxyType(
        {
            # 400
            DomainFieldError: status.HTTP_400_BAD_REQUEST,

            # 401
            # 403
            AuthorizationError: status.HTTP_403_FORBIDDEN,
            ActivationChangeNotPermittedError: status.HTTP_403_FORBIDDEN,
            RoleChangeNotPermittedError: status.HTTP_403_FORBIDDEN,
            # 415
            # 404
            UserNotFoundError: status.HTTP_404_NOT_FOUND,
            # 408
            # 409
            SortingError: status.HTTP_409_CONFLICT,
            EntityAddError: status.HTTP_409_CONFLICT,
            # 422
            pydantic.ValidationError: status.HTTP_422_UNPROCESSABLE_CONTENT,
            PaginationError: status.HTTP_422_UNPROCESSABLE_CONTENT,
            # 500
            DomainError: status.HTTP_500_INTERNAL_SERVER_ERROR,
            ApplicationError: status.HTTP_500_INTERNAL_SERVER_ERROR,
            InfrastructureError: status.HTTP_500_INTERNAL_SERVER_ERROR,
            AppError: status.HTTP_500_INTERNAL_SERVER_ERROR,
            Exception: status.HTTP_500_INTERNAL_SERVER_ERROR,
            # 503
            RepoError: status.HTTP_503_SERVICE_UNAVAILABLE,
            RollbackError: status.HTTP_503_SERVICE_UNAVAILABLE,
        }
    )

    def __init__(self, app: FastAPI) -> None:
        self._app: Final[FastAPI] = app
        self._status_internal_server_error: Final[int] = 500

    async def _handle(self, _: Request, exc: Exception) -> ORJSONResponse:
        status_code: int = self._ERROR_MAPPING.get(
            type(exc),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

        response: ExceptionSchema | ExceptionSchemaRich
        if isinstance(exc, pydantic.ValidationError):
            response = ExceptionSchemaRich(str(exc), jsonable_encoder(exc.errors()))

        elif status_code == status.HTTP_503_SERVICE_UNAVAILABLE:
            message_if_unavailable: str = "Service temporarily unavailable. Please try again later."
            response = ExceptionSchema(message_if_unavailable)

        else:
            message: str = str(exc) if status_code < self._status_internal_server_error else "Internal server error."
            response = ExceptionSchema(message)

        if status_code >= self._status_internal_server_error:
            logger.error(
                "Exception '%s' occurred: '%s'.",
                type(exc).__name__,
                exc,
                exc_info=exc,
            )

        else:
            logger.warning("Exception '%s' occurred: '%s'.", type(exc).__name__, exc)

        return ORJSONResponse(
            status_code=status_code,
            content=response,
        )

    def setup_handlers(self) -> None:
        for exc_class in self._ERROR_MAPPING:
            self._app.add_exception_handler(exc_class, self._handle)
        self._app.add_exception_handler(Exception, self._handle)
