import logging
from typing import Annotated

from authx import AuthX, TokenPayload
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette import status

from app.application.api.v1.auth.dependencies import get_access_token_payload, get_refresh_token_payload, RoleChecker
from app.application.api.v1.auth.schemas import TokenResponse
from app.application.api.v1.users.schemas import UserSchemaResponse
from app.domain.entities.user import UserEntity
from app.infrastructure.cache.base import BaseCache
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.auth import VerifyUserCredentialsCommand
from app.logic.message_bus import MessageBus
from app.logic.views.users import UsersViews

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"], route_class=DishkaRoute)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/")


@router.post(
    "/login/",
    status_code=status.HTTP_200_OK,
    summary="Endpoint for user logging",
)
async def login(
        form: Annotated[OAuth2PasswordRequestForm, Depends()],
        bootstrap: FromDishka[Bootstrap[UsersUnitOfWork]],
        security: FromDishka[AuthX]
) -> TokenResponse:
    messagebus: MessageBus = await bootstrap.get_messagebus()
    await messagebus.handle(VerifyUserCredentialsCommand(email=form.username, password=form.password))
    user: UserEntity = messagebus.command_result

    return TokenResponse(
        access_token=security.create_access_token(uid=str(user.oid)),
        refresh_token=security.create_refresh_token(uid=str(user.oid)),
    )


@router.post(
    "/refresh/",
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    summary="Endpoint for user refreshing",
)
async def refresh(
        security: FromDishka[AuthX],
        token: TokenPayload = Depends(get_refresh_token_payload),
) -> TokenResponse:
    return TokenResponse(access_token=security.create_access_token(token.sub))


@router.get(
    "/me/",
    status_code=status.HTTP_200_OK,
    summary="Endpoint for user info",
    dependencies=[Depends(RoleChecker(allowed_roles=["staffer", "admin", "manager"]))]
)
async def get_me(
        uow: FromDishka[UsersUnitOfWork],
        token: TokenPayload = Depends(get_access_token_payload),
) -> UserSchemaResponse:
    users_views: UsersViews = UsersViews(uow=uow)
    user: UserEntity = await users_views.get_user_by_id(token.sub)
    return UserSchemaResponse.from_entity(entity=user)


@router.delete(
    "/logout/",
    status_code=status.HTTP_200_OK,
    summary="Endpoint for user logout. Deletes his JWT access token",
    dependencies=[Depends(RoleChecker(allowed_roles=["staffer", "admin", "manager"]))]
)
async def logout(
        cache: FromDishka[BaseCache],
        token: TokenPayload = Depends(get_access_token_payload),
) -> None:
    await cache.set(token.jti, "", expire=36000)