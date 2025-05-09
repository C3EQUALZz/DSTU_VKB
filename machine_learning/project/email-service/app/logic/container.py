import logging
from functools import lru_cache
from typing import cast, Final

from dishka import (
    AsyncContainer,
    from_context,
    make_async_container,
    provide,
    Provider,
    Scope,
)

from faststream.kafka import KafkaBroker
from redis.asyncio import Redis, ConnectionPool

from app.infrastructure.brokers.factories import (
    EventHandlerTopicFactory,
)
from app.infrastructure.brokers.publishers.kafka.base import BaseKafkaPublisher
from app.infrastructure.brokers.publishers.kafka.faststream import FastStreamKafkaMessageBroker
from app.infrastructure.repositories.cache.idempotency.commands.base import BaseIdempotencyCommandCacheRepository
from app.infrastructure.repositories.cache.idempotency.commands.redis_cache import \
    RedisIdempotencyCommandCacheRepository
from app.infrastructure.repositories.cache.idempotency.events.base import BaseIdempotencyEventCacheRepository
from app.infrastructure.repositories.cache.idempotency.events.redis_cache import RedisIdempotencyEventCacheRepository
from app.infrastructure.services.idempotency import IdempotencyService
from app.logic.bootstrap import Bootstrap
from app.logic.event_buffer import EventBuffer
from app.logic.message_bus import MessageBus
from app.logic.types.handlers import (
    CommandHandlerMapping,
    EventHandlerMapping,
)
from app.settings.configs.app import (
    get_settings,
    Settings,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


class HandlerProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_mapping_and_command_handlers(self) -> "CommandHandlerMapping":
        """
        Here you have to link commands and command handlers for future inject in Bootstrap
        """
        return cast(
            "CommandHandlerMapping",
            {

            },
        )

    @provide(scope=Scope.APP)
    async def get_mapping_event_and_event_handlers(self) -> "EventHandlerMapping":
        """
        Here you have to link events and event handlers for future inject in Bootstrap
        """
        return cast(
            "EventHandlerMapping",
            {

            },
        )


class BrokerProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_mapping_events_and_topic(self, settings: Settings) -> EventHandlerTopicFactory:
        return EventHandlerTopicFactory(
            mapping={
            }
        )

    @provide(scope=Scope.APP)
    async def get_faststream_broker(self, settings: Settings) -> KafkaBroker:
        broker: KafkaBroker = KafkaBroker(settings.broker.url, logger=logger)
        logger.info("Included router")
        return broker

    @provide(scope=Scope.APP)
    async def get_producer(
            self,
            settings: Settings,
            broker: KafkaBroker,
    ) -> BaseKafkaPublisher:
        return FastStreamKafkaMessageBroker(
            broker=broker,
            producers={

            }
        )


class CacheProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_redis_connection_pool(self, settings: Settings) -> ConnectionPool:
        return ConnectionPool.from_url(str(settings.cache.url))

    @provide(scope=Scope.APP)
    async def get_redis_client(self, pool: ConnectionPool) -> Redis:
        return Redis.from_pool(pool)

    @provide(scope=Scope.APP)
    async def get_cache_idempotency_command_repository(self, client: Redis) -> BaseIdempotencyEventCacheRepository:
        return RedisIdempotencyEventCacheRepository(redis_client=client)

    @provide(scope=Scope.APP)
    async def get_cache_idempotency_event_repository(self, client: Redis) -> BaseIdempotencyCommandCacheRepository:
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
    async def get_bootstrap(
            self,
            events: EventHandlerMapping,
            commands: CommandHandlerMapping,
            event_buffer: EventBuffer,
            broker: BaseKafkaPublisher,
            event_handler_topic_factory: EventHandlerTopicFactory,
            idempotency_service: IdempotencyService,
    ) -> Bootstrap:
        return Bootstrap(
            event_buffer=event_buffer,
            events_handlers_for_injection=events,
            commands_handlers_for_injection=commands,
            idempotency_service=idempotency_service,
            dependencies={
                "broker": broker,
                "event_handler_topic_factory": event_handler_topic_factory
            },
        )

    @provide(scope=Scope.APP)
    async def get_message_bus(self, bootstrap: Bootstrap) -> MessageBus:
        return await bootstrap.get_messagebus()


@lru_cache(maxsize=1)
def get_container() -> AsyncContainer:
    return make_async_container(
        HandlerProvider(), AppProvider(), BrokerProvider(), context={Settings: get_settings()}
    )
