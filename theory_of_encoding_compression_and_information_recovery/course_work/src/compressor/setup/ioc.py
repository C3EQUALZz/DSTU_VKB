from typing import Iterable, Final

from aiogram import Bot
from bazario.asyncio import Registry, Dispatcher
from bazario.asyncio.resolvers.dishka import DishkaResolver
from dishka import Provider, Scope, provide, WithParents
from dishka.integrations.aiogram import AiogramProvider, AiogramMiddlewareData
from dishka.integrations.taskiq import TaskiqProvider
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from compressor.application.common.ports.identity_provider import CompositeIdentityProvider, IdentityProvider
from compressor.application.common.ports.transaction_manager import TransactionManager
from compressor.application.common.ports.user_command_gateway import UserCommandGateway
from compressor.application.common.ports.user_query_gateway import UserQueryGateway
from compressor.domain.files.ports.file_id_generator import FileIDGenerator
from compressor.domain.files.services.file_service import FileService
from compressor.domain.users.ports.password_hasher import PasswordHasher
from compressor.domain.users.ports.user_id_generator import UserIDGenerator
from compressor.domain.users.services.authorization_service import AuthorizationService
from compressor.domain.users.services.telegram_service import TelegramService
from compressor.domain.users.services.user_service import UserService
from compressor.infrastructure.adapters.common.password_hasher_bcrypt import PasswordPepper, BcryptPasswordHasher
from compressor.infrastructure.adapters.common.telegram_identity_provider import TelegramIdentityProvider
from compressor.infrastructure.adapters.common.uuid4_file_id_generator import UUID4FileIDGenerator
from compressor.infrastructure.adapters.common.uuid4_user_id_generator import UUID4UserIDGenerator
from compressor.infrastructure.adapters.persistence.alchemy_transaction_manager import SqlAlchemyTransactionManager
from compressor.infrastructure.adapters.persistence.alchemy_user_command_gateway import (
    SqlAlchemyUserCommandGateway
)
from compressor.infrastructure.adapters.persistence.alchemy_user_query_gateway import (
    SqlAlchemyUserQueryGateway
)
from compressor.infrastructure.cache.provider import get_redis_pool, get_redis
from compressor.infrastructure.event_bus.base import EventBus
from compressor.infrastructure.event_bus.bazario_event_bus import BazarioEventBus
from compressor.infrastructure.persistence.provider import get_engine, get_sessionmaker, get_session
from compressor.infrastructure.task_manager.files.base import FileTaskManager
from compressor.infrastructure.task_manager.files.task_iq import TaskIQFileTaskManager
from compressor.setup.configs.cache import RedisConfig
from compressor.setup.configs.database import PostgresConfig, SQLAlchemyConfig


def configs_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.from_context(provides=PostgresConfig)
    provider.from_context(provides=SQLAlchemyConfig)
    provider.from_context(provides=PasswordPepper)
    provider.from_context(provides=RedisConfig)
    return provider


def db_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide(get_engine, scope=Scope.APP)
    provider.provide(get_sessionmaker, scope=Scope.APP)
    provider.provide(get_session, provides=AsyncSession)
    return provider


def cache_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide(get_redis_pool, scope=Scope.APP)
    provider.provide(get_redis, provides=Redis)
    return provider


def domain_ports_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide(source=BcryptPasswordHasher, provides=PasswordHasher)
    provider.provide(source=UUID4UserIDGenerator, provides=UserIDGenerator)
    provider.provide(source=UUID4FileIDGenerator, provides=FileIDGenerator)
    provider.provide(source=UserService)
    provider.provide(source=TelegramService)
    provider.provide(source=AuthorizationService)
    provider.provide(source=FileService)
    return provider


def gateways_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide(source=SqlAlchemyTransactionManager, provides=TransactionManager)
    provider.provide(source=SqlAlchemyUserCommandGateway, provides=UserCommandGateway)
    provider.provide(source=SqlAlchemyUserQueryGateway, provides=UserQueryGateway)
    return provider


def registry_provider() -> Registry:
    registry: Final[Registry] = Registry()
    return registry


def event_bus_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide(registry_provider)
    provider.provide(BazarioEventBus, provides=EventBus)
    provider.provide(WithParents[Dispatcher])
    provider.provide(WithParents[DishkaResolver])
    return provider


def task_manager_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide(TaskIQFileTaskManager, provides=FileTaskManager)
    return provider


def auth_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.decorate(CompositeIdentityProvider, provides=IdentityProvider)
    return provider


class TelegramProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.REQUEST)
    def get_current_telegram_user_id(
            self, middleware_data: AiogramMiddlewareData
    ) -> int | None:
        if current_chat := middleware_data.get("event_chat"):
            return current_chat.id
        return None

    @provide(scope=scope.REQUEST)
    def get_current_bot(
            self, middleware_data: AiogramMiddlewareData
    ) -> Bot | None:
        if bot := middleware_data.get("bot"):
            return bot
        return None

    idp = provide(WithParents[TelegramIdentityProvider])


def setup_providers() -> Iterable[Provider]:
    return (
        configs_provider(),
        TelegramProvider(),
        AiogramProvider(),
        TaskiqProvider(),
        cache_provider(),
        domain_ports_provider(),
        gateways_provider(),
        event_bus_provider(),
        task_manager_provider(),
        auth_provider()
    )
