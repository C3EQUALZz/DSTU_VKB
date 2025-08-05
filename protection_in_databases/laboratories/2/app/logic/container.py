import logging
from functools import lru_cache
from typing import cast, Final
from pathlib import Path
import pymysql
from pymysql import Connection
from dishka import Provider, Scope, from_context, make_async_container, provide, AsyncContainer

from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.infrastructure.uow.users.mysql import PyMySQLUsersUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.users import CreateUserCommand, UpdateUserCommand, DeleteUserCommand
from app.logic.event_buffer import EventBuffer
from app.logic.handlers.users.commands import CreateUserCommandHandler, UpdateUserCommandHandler, DeleteUserCommandHandler
from app.logic.types.handlers import CommandHandlerMapping, EventHandlerMapping
from app.settings.configs.app import Settings, get_settings, PATH_TO_PROJECT

logger: Final[logging.Logger] = logging.getLogger(__name__)


class HandlerProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_mapping_and_command_handlers(self) -> CommandHandlerMapping:
        """
        Here you have to link commands and command handlers for future inject in Bootstrap
        """
        return cast(
            CommandHandlerMapping,
            {
                CreateUserCommand: CreateUserCommandHandler,
                UpdateUserCommand: UpdateUserCommandHandler,
                DeleteUserCommand: DeleteUserCommandHandler,
            },
        )

    @provide(scope=Scope.APP)
    async def get_mapping_event_and_event_handlers(self) -> EventHandlerMapping:
        """
        Here you have to link events and event handlers for future inject in Bootstrap
        """
        return cast(
            EventHandlerMapping,
            {
            },
        )


class AppProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_event_buffer(self) -> EventBuffer:
        return EventBuffer()

    @provide(scope=Scope.APP)
    async def get_bootstrap(
            self,
            event_buffer: EventBuffer,
            events: EventHandlerMapping,
            commands: CommandHandlerMapping,
            users_uow: UsersUnitOfWork,
    ) -> Bootstrap:
        return Bootstrap(
            event_buffer=event_buffer,
            events_handlers_for_injection=events,
            commands_handlers_for_injection=commands,
            dependencies={
                "users_uow": users_uow,
            },
        )


class DatabaseProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_users_uow(self, connection: Connection) -> UsersUnitOfWork:
        return PyMySQLUsersUnitOfWork(
            connection=connection,
        )

    @provide(scope=Scope.APP)
    async def get_engine_client(self, settings: Settings) -> Connection:
        conn: Connection = pymysql.connect(
            user=settings.database.user,
            host=settings.database.host,
            port=settings.database.port,
            password=settings.database.password,
            database=settings.database.name,
            cursorclass=pymysql.cursors.DictCursor,
            ssl_ca=f"{PATH_TO_PROJECT}{settings.database.ssl_ca}",
            ssl_cert=f"{PATH_TO_PROJECT}{settings.database.ssl_cert}",
            ssl_key=f"{PATH_TO_PROJECT}{settings.database.ssl_key}",
        )

        return conn


@lru_cache(maxsize=1)
def get_container() -> AsyncContainer:
    return make_async_container(
        HandlerProvider(),
        AppProvider(),
        DatabaseProvider(),
        context={Settings: get_settings()},
    )
