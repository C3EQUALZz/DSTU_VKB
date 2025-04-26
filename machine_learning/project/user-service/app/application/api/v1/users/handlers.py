import logging
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Query
from starlette import status

from app.application.api.v1.users.schemas import (
    CreateUserSchemaRequest,
    UpdateUserSchemaRequest,
    UserSchemaResponse,
)
from app.domain.entities.user import UserEntity
from app.exceptions.infrastructure import UserNotFoundException
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.users import (
    CreateUserCommand,
    DeleteUserCommand,
    UpdateUserCommand,
)
from app.logic.message_bus import MessageBus
from app.logic.views.users import UsersViews

router = APIRouter(prefix="/users", tags=["users"], route_class=DishkaRoute)
logger = logging.getLogger(__name__)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
)
async def get_users(
    uow: FromDishka[UsersUnitOfWork],
    page: int = Query(1, ge=1, description="Номер страницы"),
    size: int = Query(10, ge=1, le=100, description="Размер страницы"),
) -> list[UserSchemaResponse]:
    users_views: UsersViews = UsersViews(uow=uow)
    users: list[UserEntity] = await users_views.get_all_users(page_number=page, page_size=size)
    return [UserSchemaResponse.from_entity(entity=entity) for entity in users]


@router.get(
    "/{user_id}/",
    status_code=status.HTTP_200_OK,
)
async def get_user(
    user_id: UUID,
    uow: FromDishka[UsersUnitOfWork],
) -> UserSchemaResponse:
    users_views: UsersViews = UsersViews(uow=uow)
    user: UserEntity = await users_views.get_user_by_id(str(user_id))
    return UserSchemaResponse.from_entity(entity=user)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {"model": UserNotFoundException},
    },
)
async def create_user(
    scheme: CreateUserSchemaRequest, bootstrap: FromDishka[Bootstrap[UsersUnitOfWork]]
) -> UserSchemaResponse:
    messagebus: MessageBus = await bootstrap.get_messagebus()

    await messagebus.handle(CreateUserCommand(**scheme.model_dump()))

    return UserSchemaResponse.from_entity(messagebus.command_result)


@router.patch(
    "/{user_id}/",
    status_code=status.HTTP_200_OK,
)
async def update_user(
    scheme: UpdateUserSchemaRequest,
    bootstrap: FromDishka[Bootstrap[UsersUnitOfWork]],
) -> UserSchemaResponse:
    messagebus: MessageBus = await bootstrap.get_messagebus()
    await messagebus.handle(UpdateUserCommand(**scheme.model_dump()))
    return UserSchemaResponse.from_entity(messagebus.command_result)


@router.delete(
    "/{user_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": UserNotFoundException},
    },
)
async def delete_user(user_id: UUID, bootstrap: FromDishka[Bootstrap[UsersUnitOfWork]]) -> None:
    messagebus: MessageBus = await bootstrap.get_messagebus()
    await messagebus.handle(DeleteUserCommand(oid=str(user_id)))
    return messagebus.command_result