import logging
from uuid import UUID
from typing import Final, Annotated
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path, Query
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

router: Final[APIRouter] = APIRouter(prefix="/users", tags=["users"], route_class=DishkaRoute)
logger: Final[logging.Logger] = logging.getLogger(__name__)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    description="HTTP get method for getting info about all users with pagination",
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
    description="HTTP get method for getting info about personality"
)
async def get_user(
        user_id: Annotated[UUID, Path(title="Identifier of user", description="Identifier of user which must be UUID")],
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
    description="HTTP post method for creating user"
)
async def create_user(
        scheme: CreateUserSchemaRequest, bootstrap: FromDishka[Bootstrap]
) -> UserSchemaResponse:
    messagebus: MessageBus = await bootstrap.get_messagebus()
    await messagebus.handle(CreateUserCommand(
        name=scheme.name,
        surname=scheme.surname,
        email=str(scheme.email),
        password=scheme.password,
    ))
    return UserSchemaResponse.from_entity(messagebus.command_result)


@router.patch(
    "/{user_id}/",
    status_code=status.HTTP_200_OK,
    description="HTTP patch method for updating user"
)
async def update_user(
        user_id: Annotated[UUID, Path(title="Identifier of user", description="Identifier of user which must be UUID")],
        scheme: UpdateUserSchemaRequest,
        bootstrap: FromDishka[Bootstrap],
) -> UserSchemaResponse:
    messagebus: MessageBus = await bootstrap.get_messagebus()
    await messagebus.handle(UpdateUserCommand(**{"user_id": str(user_id), **scheme.model_dump(exclude_unset=True, exclude_none=True)}))
    return UserSchemaResponse.from_entity(messagebus.command_result)


@router.delete(
    "/{user_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": UserNotFoundException},
    },
    description="HTTP delete method for deleting user"
)
async def delete_user(
        user_id: Annotated[UUID, Path(title="Identifier of user", description="Identifier of user which must be UUID")],
        bootstrap: FromDishka[Bootstrap]
) -> None:
    messagebus: MessageBus = await bootstrap.get_messagebus()
    await messagebus.handle(DeleteUserCommand(user_id=str(user_id)))
    return messagebus.command_result
