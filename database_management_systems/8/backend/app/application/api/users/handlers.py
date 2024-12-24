from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, HTTPException
from starlette import status

from app.application.api.users.schemas import CreateUserSchema
from app.domain.entities.user import UserEntity
from app.exceptions import ApplicationException
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.users import DeleteUserCommand, CreateUserCommand
from app.logic.exceptions import UserNotFoundException
from app.logic.handlers import EVENTS_HANDLERS_FOR_INJECTION, COMMANDS_HANDLERS_FOR_INJECTION
from app.logic.message_bus import MessageBus

router = APIRouter(
    prefix="/users",
    tags=["users"],
    route_class=DishkaRoute
)


@router.post("/")
async def create_user(scheme: CreateUserSchema, uow: FromDishka[UsersUnitOfWork]) -> UserEntity:
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=uow,
            events_handlers_for_injection=EVENTS_HANDLERS_FOR_INJECTION,
            commands_handlers_for_injection=COMMANDS_HANDLERS_FOR_INJECTION
        )

        messagebus: MessageBus = await bootstrap.get_messagebus()

        await messagebus.handle(
            CreateUserCommand(
                **scheme.model_dump()
            )
        )

        return messagebus.command_result

    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.get("/")
async def get_users():
    ...


@router.get("/{user_id}")
async def get_user(user_id: int):
    ...


@router.patch("/{user_id}")
async def update_user(user_id: int):
    ...


@router.delete(
    "/{user_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": "Not found"},
        status.HTTP_404_NOT_FOUND: {"model": UserNotFoundException},
    }
)
async def delete_user(user_id: str, uow: FromDishka[UsersUnitOfWork]) -> None:
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=uow,
            events_handlers_for_injection=EVENTS_HANDLERS_FOR_INJECTION,
            commands_handlers_for_injection=COMMANDS_HANDLERS_FOR_INJECTION
        )

        messagebus: MessageBus = await bootstrap.get_messagebus()
        await messagebus.handle(
            DeleteUserCommand(
                oid=user_id,
            )
        )

        return messagebus.command_result

    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
