import logging
from typing import Any, cast

from app.core.types.handlers import (
    CommandHandlerMapping,
    EventHandlerMapping,
    CT,
    ET
)
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.infrastructure.uow.users.mongo import MotorUsersUnitOfWork
from app.logic.commands.users import (
    CreateUserCommand,
    GetAllUsersCommand,
    GetUserByIdCommand,
    UpdateUserCommand,
)
from app.logic.handlers.users.commands import (
    CreateUserCommandHandler,
    GetAllUsersCommandHandler,
    GetUserByIdCommandHandler,
    UpdateUserCommandHandler,
)
from app.settings.config import Settings
from dishka import (
    from_context,
    make_async_container,
    provide,
    Provider,
    Scope,
)
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)


class HandlerProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_mapping_and_command_handlers(self) -> CommandHandlerMapping:
        """
        Here you have to link commands and command handlers for future inject in Bootstrap
        """
        return cast(CommandHandlerMapping, {
            CreateUserCommand: CreateUserCommandHandler,
            GetAllUsersCommand: GetAllUsersCommandHandler,
            GetUserByIdCommand: GetUserByIdCommandHandler,
            UpdateUserCommand: UpdateUserCommandHandler,
        })

    @provide(scope=Scope.APP)
    async def get_mapping_event_and_event_handlers(self) -> EventHandlerMapping:
        """
        Here you have to link events and event handlers for future inject in Bootstrap
        """
        return cast(EventHandlerMapping, {})


class AppProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_motor_client(self, settings: Settings) -> AsyncIOMotorClient[Any]:
        client: AsyncIOMotorClient[Any] = AsyncIOMotorClient(str(settings.database.url))

        if info := await client.server_info():
            logger.debug("Successfully connected to MongoDB, info [%s]", info)

        return client

    @provide(scope=Scope.APP)
    async def get_users_motor_uow(self, settings: Settings, client: AsyncIOMotorClient[Any]) -> UsersUnitOfWork:
        return MotorUsersUnitOfWork(client=client, database_name=settings.database.database_name)


container = make_async_container(
    AppProvider(),
    HandlerProvider(),
    context={
        Settings: Settings(),
    },
)
