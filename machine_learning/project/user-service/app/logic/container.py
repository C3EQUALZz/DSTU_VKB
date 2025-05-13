import logging
from functools import lru_cache
from typing import cast

from authx import AuthXConfig, AuthX
from dishka import Provider, Scope, from_context, make_async_container, provide, AsyncContainer
from faststream.kafka import KafkaBroker
from redis.asyncio import ConnectionPool, Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.infrastructure.brokers.base import BaseMessageBroker
from app.infrastructure.brokers.factory import EventHandlerTopicFactory
from app.infrastructure.brokers.publishers.faststream import FastStreamKafkaMessageBroker
from app.infrastructure.repositories.cache.idempotency.commands.base import BaseIdempotencyCommandCacheRepository
from app.infrastructure.repositories.cache.idempotency.commands.redis_cache import \
    RedisIdempotencyCommandCacheRepository
from app.infrastructure.repositories.cache.idempotency.events.base import BaseIdempotencyEventCacheRepository
from app.infrastructure.repositories.cache.idempotency.events.redis_cache import RedisIdempotencyEventCacheRepository
from app.infrastructure.services.idempotency import IdempotencyService
from app.infrastructure.uow.users.alchemy import SQLAlchemyUsersUnitOfWork
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.users import CreateUserCommand, UpdateUserCommand, DeleteUserCommand
from app.logic.event_buffer import EventBuffer
from app.logic.events.users import UserCreatedEvent, UserDeletedEvent, UserUpdatedEvent
from app.logic.handlers.users.commands import CreateUserCommandHandler, UpdateUserCommandHandler, \
    DeleteUserCommandHandler
from app.logic.handlers.users.events import UserCreatedEventHandler, UserDeletedEventHandler, UserUpdatedEventHandler
from app.logic.types.handlers import CommandHandlerMapping, EventHandlerMapping
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
                DeleteUserCommand: DeleteUserCommandHandler
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
                UserCreatedEvent: [UserCreatedEventHandler],
                UserDeletedEvent: [UserDeletedEventHandler],
                UserUpdatedEvent: [UserUpdatedEventHandler],
            },
        )


class BrokerProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_mapping_events_and_topic(self, settings: Settings) -> EventHandlerTopicFactory:
        return EventHandlerTopicFactory(
            mapping={
                UserCreatedEventHandler: settings.broker.user_created_topic,
                UserDeletedEventHandler: settings.broker.user_deleted_topic,
                UserUpdatedEventHandler: settings.broker.user_updated_topic,
            }
        )

    @provide(scope=Scope.APP)
    async def get_faststream_kafka_broker(self, settings: Settings) -> KafkaBroker:
        broker: KafkaBroker = KafkaBroker(settings.broker.url)

        return broker

    @provide(scope=Scope.APP)
    async def get_producer(
            self,
            settings: Settings,
            broker: KafkaBroker,
    ) -> BaseMessageBroker:
        return FastStreamKafkaMessageBroker(
            broker=broker,
            producers={
                settings.broker.user_created_topic: broker.publisher(settings.broker.user_created_topic),
                settings.broker.user_updated_topic: broker.publisher(settings.broker.user_updated_topic),
                settings.broker.user_deleted_topic: broker.publisher(settings.broker.user_deleted_topic),
            }
        )


class AuthProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_config(self, settings: Settings) -> AuthXConfig:
        return AuthXConfig(
            JWT_ALGORITHM="RS256",
            JWT_DECODE_ALGORITHMS=["RS256"],
            JWT_PRIVATE_KEY=settings.auth.private_key,
            JWT_PUBLIC_KEY=settings.auth.public_key,
        )

    @provide(scope=Scope.APP)
    async def get_security(self, config: AuthXConfig) -> AuthX:
        return AuthX(config=config)


class CacheProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_redis_connection_pool(self, settings: Settings) -> ConnectionPool:
        return ConnectionPool.from_url(str(settings.cache.url))

    @provide(scope=Scope.APP)
    async def get_redis_client(self, pool: ConnectionPool) -> Redis:
        return Redis.from_pool(pool)

    @provide(scope=Scope.APP)
    async def get_event_cache_idempotency_repository(self, client: Redis) -> BaseIdempotencyEventCacheRepository:
        return RedisIdempotencyEventCacheRepository(redis_client=client)

    @provide(scope=Scope.APP)
    async def get_command_cache_idempotency_repository(self, client: Redis) -> BaseIdempotencyCommandCacheRepository:
        return RedisIdempotencyCommandCacheRepository(redis_client=client)


class AppProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_event_buffer(self) -> EventBuffer:
        return EventBuffer()

    @provide(scope=Scope.APP)
    async def get_idempotency_service(
            self,
            event_buffer: EventBuffer,
            event_idempotency_repository: BaseIdempotencyEventCacheRepository,
            command_idempotency_repository: BaseIdempotencyCommandCacheRepository,
    ) -> IdempotencyService:
        return IdempotencyService(
            event_buffer=event_buffer,
            event_cache=event_idempotency_repository,
            command_cache=command_idempotency_repository,
        )

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
            broker: BaseMessageBroker,
            event_handler_and_topic_factory: EventHandlerTopicFactory
    ) -> Bootstrap:
        return Bootstrap(
            event_buffer=event_buffer,
            events_handlers_for_injection=events,
            commands_handlers_for_injection=commands,
            dependencies={
                "broker": broker,
                "event_handler_and_topic_factory": event_handler_and_topic_factory
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
        )

        logger.debug("Successfully connected to Database")

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
        BrokerProvider(),
        AppProvider(),
        CacheProvider(),
        DatabaseProvider(),
        context={Settings: get_settings()},
    )
