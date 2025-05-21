import logging
from functools import lru_cache
from typing import cast, Final

from app.logic.handlers.users.commands import CreateUserCommandHandler, UpdateUserCommandHandler, \
    DeleteUserCommandHandler
from app.settings.configs.app import Settings, get_settings
from dishka import Provider, Scope, from_context, make_async_container, provide, AsyncContainer
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.infrastructure.uow.users.alchemy import SQLAlchemyUsersUnitOfWork
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.users import CreateUserCommand, UpdateUserCommand, DeleteUserCommand
from app.logic.event_buffer import EventBuffer
from app.logic.types.handlers import CommandHandlerMapping, EventHandlerMapping

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
    async def get_users_uow(
            self, session_maker: async_sessionmaker[AsyncSession]
    ) -> UsersUnitOfWork:
        return SQLAlchemyUsersUnitOfWork(session_factory=session_maker)

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
    async def get_engine_client(self, settings: Settings) -> AsyncEngine:
        engine: AsyncEngine = create_async_engine(
            url=settings.database.url,
            pool_pre_ping=settings.alchemy_settings.pool_pre_ping,
            pool_recycle=settings.alchemy_settings.pool_recycle,
            echo=settings.alchemy_settings.echo,
            sslcert=settings.alchemy_settings.ssl_cert,
            sslrootcert=settings.alchemy_settings.ssl_root_cert,
            sslmode=settings.alchemy_settings.ssl_mode,
            ssl_min_protocol_version=settings.alchemy_settings.ssl_min_protocol_version,
        )

        logger.info("Successfully connected to Database")

        return engine

    @provide(scope=Scope.APP)
    async def get_session_maker(
            self, engine: AsyncEngine, settings: Settings
    ) -> async_sessionmaker[AsyncSession]:
        session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=engine,
            autoflush=settings.alchemy_settings.auto_flush,
            expire_on_commit=settings.alchemy_settings.expire_on_commit,
        )

        return session_maker


@lru_cache(maxsize=1)
def get_container() -> AsyncContainer:
    return make_async_container(
        HandlerProvider(),
        AppProvider(),
        DatabaseProvider(),
        context={Settings: get_settings()},
    )
