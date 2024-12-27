from typing import Annotated

from authx import TokenPayload, AuthX
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status

from app.core.types.handlers import EventHandlerMapping, CommandHandlerMapping
from app.domain.entities.user import UserEntity
from app.exceptions import ApplicationException
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.auth import VerifyUserCredentialsCommand
from app.logic.message_bus import MessageBus
from app.logic.container import container

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    route_class=DishkaRoute
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post(
    "/login/",
    status_code=status.HTTP_201_CREATED
)
async def login(
        form: Annotated[OAuth2PasswordRequestForm, Depends()],
        security: FromDishka[AuthX],
        uow: FromDishka[UsersUnitOfWork],
        events: FromDishka[EventHandlerMapping],
        commands: FromDishka[CommandHandlerMapping]
):
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=uow,
            events_handlers_for_injection=events,
            commands_handlers_for_injection=commands
        )

        messagebus: MessageBus = await bootstrap.get_messagebus()
        await messagebus.handle(VerifyUserCredentialsCommand(name=form.username, password=form.password))
        user: UserEntity = messagebus.command_result

        access_token = security.create_access_token(uid=user.oid)
        refresh_token = security.create_refresh_token(uid=user.oid)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    except ApplicationException as e:
        raise HTTPException(status_code=e.status, detail=e.message, headers={"WWW-Authenticate": "Bearer"})


async def get_security() -> AuthX:
    return await container.get(AuthX)


@router.post("/refresh/")
async def refresh(
        security: FromDishka[AuthX],
        refresh_payload: TokenPayload = Depends(security.refresh_token_required)
):
    access_token = security.create_access_token(refresh_payload.sub)
    return {"access_token": access_token}
