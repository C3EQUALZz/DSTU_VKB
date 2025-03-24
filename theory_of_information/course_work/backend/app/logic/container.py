import logging
from typing import cast

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from authx import AuthXConfig, AuthX
from dishka import (
    Provider,
    Scope,
    from_context,
    make_async_container,
    provide,
)
from redis.asyncio import ConnectionPool, Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.infrastructure.brokers.base import BaseMessageBroker
from app.infrastructure.brokers.kafka import KafkaMessageBroker
from app.infrastructure.cache.base import BaseCache
from app.infrastructure.cache.redis import RedisCache
from app.infrastructure.uow.users.alchemy import SQLAlchemyUsersUnitOfWork
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.auth import VerifyUserCredentialsCommand
from app.logic.commands.users import CreateUserCommand, UpdateUserCommand, DeleteUserCommand
from app.logic.events.users import UserDeleteEvent
from app.logic.handlers.auth.commands import VerifyUserCredentialsCommandHandler
from app.logic.handlers.users.commands import CreateUserCommandHandler, UpdateUserCommandHandler, \
    DeleteUserCommandHandler
from app.logic.handlers.users.events import UserDeleteEventHandler
from app.logic.types.handlers import CommandHandlerMapping, EventHandlerMapping
from app.logic.types.handlers import UT
from app.settings.config import Settings, get_settings

logger = logging.getLogger(__name__)


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
                VerifyUserCredentialsCommand: VerifyUserCredentialsCommandHandler,
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
                UserDeleteEvent: [UserDeleteEventHandler]
            }
        )


class BrokerProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_kafka_broker(self, settings: Settings) -> BaseMessageBroker:
        return KafkaMessageBroker(
            producer=AIOKafkaProducer(bootstrap_servers=settings.broker.url),
            consumer=AIOKafkaConsumer(
                bootstrap_servers=settings.broker.url,
                group_id=f"users-service-group",
                metadata_max_age_ms=30000,
            ),
        )


class AppProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_users_uow(self, session_maker: async_sessionmaker[AsyncSession]) -> UsersUnitOfWork:
        return SQLAlchemyUsersUnitOfWork(session_factory=session_maker)

    @provide(scope=Scope.APP)
    async def get_bootstrap(
            self,
            events: EventHandlerMapping,
            commands: CommandHandlerMapping,
            broker: BaseMessageBroker,
            uow: UT
    ) -> Bootstrap[UT]:
        return Bootstrap(
            uow=uow,
            events_handlers_for_injection=events,
            commands_handlers_for_injection=commands,
            dependencies={"broker": broker}
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
        )

        logger.debug("Successfully connected to Database")

        return engine

    @provide(scope=Scope.APP)
    async def get_session_maker(self, engine: AsyncEngine, settings: Settings) -> async_sessionmaker[AsyncSession]:
        session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=engine,
            autoflush=settings.alchemy_settings.auto_flush,
            expire_on_commit=settings.alchemy_settings.expire_on_commit,
        )

        return session_maker


class AuthProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_config(self, settings: Settings) -> AuthXConfig:
        return AuthXConfig(
            JWT_ALGORITHM="RS256",
            JWT_DECODE_ALGORITHMS=["RS256"],
            JWT_PRIVATE_KEY=settings.auth.private_key,
            JWT_PUBLIC_KEY=settings.auth.public_key
        )

    @provide(scope=Scope.APP)
    async def get_security(self, config: AuthXConfig) -> AuthX:
        return AuthX(config=config)


class RedisProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_connection_pool(self, settings: Settings) -> ConnectionPool:
        return ConnectionPool.from_url(str(settings.cache.url), encoding="utf8", decode_responses=True)

    @provide(scope=Scope.APP)
    async def get_client(self, pool: ConnectionPool) -> BaseCache:
        return RedisCache(Redis.from_pool(pool))


container = make_async_container(
    DatabaseProvider(),
    HandlerProvider(),
    BrokerProvider(),
    AppProvider(),
    AuthProvider(),
    RedisProvider(),
    context={
        Settings: get_settings(),
    }
)
