from typing import List

from fastapi import (
    APIRouter,
    HTTPException,
)
from starlette import status

from app.application.api.users.schemas import (
    CreateUserSchemaRequest,
    ErrorMessageScheme,
    UpdateUserSchemaRequest,
    UserSchemeResponse,
)
from app.core.types.handlers import (
    CommandHandlerMapping,
    EventHandlerMapping,
    CT,
    ET
)
from app.exceptions import ApplicationException
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.users import (
    CreateUserCommand,
    DeleteUserCommand,
    GetAllUsersCommand,
    GetUserByIdCommand,
    UpdateUserCommand,
)
from app.logic.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.logic.message_bus import MessageBus
from dishka.integrations.fastapi import (
    DishkaRoute,
    FromDishka,
)

router = APIRouter(prefix="/users", tags=["users"], route_class=DishkaRoute)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {"model": UserAlreadyExistsException},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorMessageScheme},
    },
)
async def create_user(
        scheme: CreateUserSchemaRequest,
        uow: FromDishka[UsersUnitOfWork],
        events: FromDishka[EventHandlerMapping[ET]],
        commands: FromDishka[CommandHandlerMapping[CT]],
) -> UserSchemeResponse:
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=uow, events_handlers_for_injection=events, commands_handlers_for_injection=commands
        )

        messagebus: MessageBus = await bootstrap.get_messagebus()

        await messagebus.handle(CreateUserCommand(**scheme.model_dump()))

        return UserSchemeResponse.from_entity(messagebus.command_result)

    except ApplicationException as e:
        raise HTTPException(status_code=e.status, detail=str(e))


@router.get("/")
async def get_users(
        uow: FromDishka[UsersUnitOfWork],
        events: FromDishka[EventHandlerMapping[ET]],
        commands: FromDishka[CommandHandlerMapping[CT]],
) -> List[UserSchemeResponse]:
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=uow, events_handlers_for_injection=events, commands_handlers_for_injection=commands
        )

        messagebus: MessageBus = await bootstrap.get_messagebus()

        await messagebus.handle(GetAllUsersCommand())

        return [UserSchemeResponse.from_entity(entity=entity) for entity in messagebus.command_result]

    except ApplicationException as e:
        raise HTTPException(status_code=e.status, detail=str(e))


@router.get("/{user_id}/")
async def get_user(
        user_id: str,
        uow: FromDishka[UsersUnitOfWork],
        events: FromDishka[EventHandlerMapping[ET]],
        commands: FromDishka[CommandHandlerMapping[CT]],
) -> UserSchemeResponse:
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=uow, events_handlers_for_injection=events, commands_handlers_for_injection=commands
        )

        messagebus: MessageBus = await bootstrap.get_messagebus()

        await messagebus.handle(GetUserByIdCommand(oid=user_id))

        return UserSchemeResponse.from_entity(messagebus.command_result)

    except ApplicationException as e:
        raise HTTPException(status_code=e.status, detail=str(e))


@router.patch("/{user_id}/")
async def update_user(
        scheme: UpdateUserSchemaRequest,
        uow: FromDishka[UsersUnitOfWork],
        events: FromDishka[EventHandlerMapping[ET]],
        commands: FromDishka[CommandHandlerMapping[CT]],
) -> UserSchemeResponse:
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=uow, events_handlers_for_injection=events, commands_handlers_for_injection=commands
        )

        messagebus: MessageBus = await bootstrap.get_messagebus()

        await messagebus.handle(UpdateUserCommand(**scheme.model_dump()))

        return UserSchemeResponse.from_entity(messagebus.command_result)

    except ApplicationException as e:
        raise HTTPException(status_code=e.status, detail=str(e))


@router.delete(
    "/{user_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorMessageScheme},
        status.HTTP_404_NOT_FOUND: {"model": UserNotFoundException},
    },
)
async def delete_user(
        user_id: str,
        uow: FromDishka[UsersUnitOfWork],
        events: FromDishka[EventHandlerMapping[ET]],
        commands: FromDishka[CommandHandlerMapping[CT]],
) -> None:
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=uow, events_handlers_for_injection=events, commands_handlers_for_injection=commands
        )

        messagebus: MessageBus = await bootstrap.get_messagebus()
        await messagebus.handle(DeleteUserCommand(oid=user_id))

        return messagebus.command_result

    except ApplicationException as e:
        raise HTTPException(status_code=e.status, detail=e.message)
