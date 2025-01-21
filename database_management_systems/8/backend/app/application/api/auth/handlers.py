import logging
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from starlette import status
from starlette.requests import Request

from app.application.api.auth.schemas import (
    TokenRequest,
    UserSchemeResponse,
)
from app.core.types.handlers import (
    CommandHandlerMapping,
    EventHandlerMapping,
)
from app.domain.entities.user import UserEntity
from app.exceptions.base import ApplicationException
from app.exceptions.infrastructure import UserNotFoundException
from app.exceptions.logic import InvalidPasswordException
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.auth import VerifyUserCredentialsCommand
from app.logic.commands.users import GetUserByIdCommand
from app.logic.message_bus import MessageBus
from authx import (
    AuthX,
    TokenPayload,
)
from authx.exceptions import (
    AuthXException,
    RevokedTokenError,
)
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute


router = APIRouter(prefix="/auth", tags=["auth"], route_class=DishkaRoute)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login/")

logger = logging.getLogger(__name__)


@router.post(
    "/login/",
    status_code=status.HTTP_200_OK,
    summary="Endpoint for user logging",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": UserNotFoundException},
        status.HTTP_401_UNAUTHORIZED: {"model": InvalidPasswordException},
    },
)
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    security: FromDishka[AuthX],
    uow: FromDishka[UsersUnitOfWork],
    events: FromDishka[EventHandlerMapping],
    commands: FromDishka[CommandHandlerMapping],
) -> TokenRequest:
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=uow, events_handlers_for_injection=events, commands_handlers_for_injection=commands
        )

        messagebus: MessageBus = await bootstrap.get_messagebus()
        await messagebus.handle(VerifyUserCredentialsCommand(name=form.username, password=form.password))
        user: UserEntity = messagebus.command_result

        return TokenRequest(
            access_token=security.create_access_token(uid=user.oid),
            refresh_token=security.create_refresh_token(uid=user.oid),
        )

    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=e.message, headers={"WWW-Authenticate": "Bearer"})


@router.post(
    "/refresh/",
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    responses={
        #  status.HTTP_401_UNAUTHORIZED: {"model": RevokedTokenError},
    },
)
async def refresh(security: FromDishka[AuthX], request: Request) -> TokenRequest:
    try:
        refresh_payload: TokenPayload = await security.refresh_token_required(request)
        return TokenRequest(access_token=security.create_access_token(refresh_payload.sub))
    except AuthXException as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=e.message)


@router.get("/me/", dependencies=[Depends(oauth2_scheme)])
async def get_me(
    security: FromDishka[AuthX],
    request: Request,
    uow: FromDishka[UsersUnitOfWork],
    events: FromDishka[EventHandlerMapping],
    commands: FromDishka[CommandHandlerMapping],
) -> UserSchemeResponse:
    try:
        access_token: TokenPayload = await security.access_token_required(request)

        bootstrap: Bootstrap = Bootstrap(
            uow=uow, events_handlers_for_injection=events, commands_handlers_for_injection=commands
        )

        messagebus: MessageBus = await bootstrap.get_messagebus()
        await messagebus.handle(GetUserByIdCommand(access_token.sub))
        return UserSchemeResponse.from_entity(messagebus.command_result)

    except AuthXException as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=e.message)
