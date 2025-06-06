import logging
from typing import Annotated, Final

from authx import AuthX, TokenPayload
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status

from app.application.api.v1.auth.dependencies import (
    RoleChecker,
    get_access_token_payload,
    get_refresh_token_payload,
)
from app.application.api.v1.auth.schemas import TokenResponse, RegisterUserSchemaRequest
from app.application.api.v1.users.schemas import UserSchemaResponse
from app.domain.entities.user import UserEntity
from app.infrastructure.dtos.cache.security import JTICacheDTO
from app.infrastructure.repositories.cache.security.base import BaseSecurityCacheRepository
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.auth import VerifyUserCredentialsCommand
from app.logic.commands.users import CreateUserCommand
from app.logic.message_bus import MessageBus
from app.logic.views.users import UsersViews

logger: Final[logging.Logger] = logging.getLogger(__name__)
router: Final[APIRouter] = APIRouter(prefix="/auth", tags=["auth"], route_class=DishkaRoute)
oauth2_scheme: Final[OAuth2PasswordBearer] = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/")


@router.post(
    "/login/",
    status_code=status.HTTP_200_OK,
    summary="Endpoint for user logging",
)
async def login(
        form: Annotated[OAuth2PasswordRequestForm, Depends()],
        bootstrap: FromDishka[Bootstrap],
        security: FromDishka[AuthX],
) -> TokenResponse:
    messagebus: MessageBus = await bootstrap.get_messagebus()
    await messagebus.handle(VerifyUserCredentialsCommand(email=form.username, password=form.password))
    user: UserEntity = messagebus.command_result

    return TokenResponse(
        access_token=security.create_access_token(uid=str(user.oid)),
        refresh_token=security.create_refresh_token(uid=str(user.oid)),
    )


@router.post(
    "/register/",
    status_code=status.HTTP_200_OK,
    summary="Endpoint for user registration",
)
async def register(
        schemas: RegisterUserSchemaRequest,
        bootstrap: FromDishka[Bootstrap]
) -> UserSchemaResponse:
    messagebus: MessageBus = await bootstrap.get_messagebus()

    await messagebus.handle(CreateUserCommand(
        name=schemas.name,
        surname=schemas.surname,
        email=str(schemas.email),
        password=schemas.password,
    ))

    return UserSchemaResponse.from_entity(messagebus.command_result)


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
    dependencies=[Depends(RoleChecker(allowed_roles=["admin", "user"]))],
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
    dependencies=[Depends(RoleChecker(allowed_roles=["admin", "user"]))],
)
async def logout(
        cache: FromDishka[BaseSecurityCacheRepository],
        token: TokenPayload = Depends(get_access_token_payload),
) -> None:
    await cache.set(JTICacheDTO(value=token.jti), ttl=36000)
