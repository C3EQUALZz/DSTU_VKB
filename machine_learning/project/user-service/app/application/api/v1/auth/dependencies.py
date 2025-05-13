import logging

from authx import AuthX, RequestToken, TokenPayload
from authx.exceptions import AuthXException
from dishka import AsyncContainer
from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from app.domain.entities.user import UserEntity
from app.exceptions.application import (
    AuthException,
    EmptyCredentialsException,
    ForbiddenTokenException,
    RolePermissionDenyException,
)
from app.infrastructure.repositories.cache.security.base import BaseSecurityCacheRepository
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.container import get_container
from app.logic.views.users import UsersViews

logger = logging.getLogger(__name__)
http_bearer = HTTPBearer(auto_error=False)


async def get_access_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> TokenPayload:
    container: AsyncContainer = get_container()
    security: AuthX = await container.get(AuthX)
    cache: BaseSecurityCacheRepository = await container.get(BaseSecurityCacheRepository)

    if credentials is None:
        raise EmptyCredentialsException

    try:
        payload = security.verify_token(RequestToken(token=credentials.credentials, location="headers", type="access"))

        if await cache.get(payload.jti) is not None:
            raise ForbiddenTokenException("This token has been revoked. Please get a new token.")

        return payload

    except AuthXException as e:
        raise AuthException(str(e))


async def get_refresh_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> TokenPayload:
    container: AsyncContainer = get_container()
    security: AuthX = await container.get(AuthX)
    cache: BaseSecurityCacheRepository = await container.get(BaseSecurityCacheRepository)

    if credentials is None:
        raise EmptyCredentialsException

    try:
        payload = security.verify_token(RequestToken(token=credentials.credentials, location="headers", type="refresh"))

        if await cache.get(payload.jti) is not None:
            raise ForbiddenTokenException("This token has been revoked. Please get a new token.")

        return payload

    except AuthXException as e:
        raise AuthException(str(e))


class RoleChecker:
    def __init__(self, allowed_roles: list[str]) -> None:
        self._allowed_roles: list[str] = allowed_roles
        self._container: AsyncContainer = get_container()

    async def __call__(self, token: TokenPayload = Depends(get_access_token_payload)) -> bool:
        uow: UsersUnitOfWork = await self._container.get(UsersUnitOfWork)

        users_views: UsersViews = UsersViews(uow=uow)
        user: UserEntity = await users_views.get_user_by_id(token.sub)

        if user.role.as_generic_type() in self._allowed_roles:
            return True

        raise RolePermissionDenyException("You don't have enough permissions")