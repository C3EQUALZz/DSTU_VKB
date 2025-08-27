from collections.abc import Iterable
from typing import Final, cast

from aiogram import Bot
from bazario.asyncio import Dispatcher, Registry
from bazario.asyncio.resolvers.dishka import DishkaResolver
from dishka import Provider, Scope, WithParents, provide
from dishka.integrations.aiogram import AiogramMiddlewareData, AiogramProvider
from dishka.integrations.taskiq import TaskiqProvider
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from compressor.application.commands.files.compress import CompressFileCommandHandler
from compressor.application.commands.files.decompress import DecompressFileCommandHandler
from compressor.application.commands.user.activate import ActivateUserCommandHandler
from compressor.application.commands.user.create import CreateUserCommandHandler
from compressor.application.commands.user.deactivate import DeactivateUserCommandHandler
from compressor.application.commands.user.grant_admin import GrantAdminCommandHandler
from compressor.application.commands.user.link_telegram_account import LinkTelegramAccountCommandHandler
from compressor.application.commands.user.revoke_admin import RevokeAdminCommandHandler
from compressor.application.commands.user.signup import SignUpCommandHandler
from compressor.application.common.ports.access_revoker import AccessRevoker
from compressor.application.common.ports.sender import Sender
from compressor.application.common.ports.storage import FileStorage
from compressor.application.common.ports.transaction_manager import TransactionManager
from compressor.application.common.ports.user_command_gateway import UserCommandGateway
from compressor.application.common.ports.user_query_gateway import UserQueryGateway
from compressor.application.services.files.compressor import FileCompressorService
from compressor.application.services.user.current_user_service import CurrentUserService
from compressor.domain.compressors.factories.text.base import FileCompressorFactory
from compressor.domain.compressors.factories.text.impl import FileCompressorFactoryImpl
from compressor.domain.files.ports.file_id_generator import FileIDGenerator
from compressor.domain.files.services.file_service import FileService
from compressor.domain.users.ports.password_hasher import PasswordHasher
from compressor.domain.users.ports.user_id_generator import UserIDGenerator
from compressor.domain.users.services.authorization_service import AuthorizationService
from compressor.domain.users.services.telegram_service import TelegramService
from compressor.domain.users.services.user_service import UserService
from compressor.domain.users.values.telegram_user_id import TelegramID
from compressor.infrastructure.adapters.auth.telegram_access_revoker import TelegramAccessRevoker
from compressor.infrastructure.adapters.common.password_hasher_bcrypt import BcryptPasswordHasher, PasswordPepper
from compressor.infrastructure.adapters.common.telegram_identity_provider import TelegramIdentityProvider
from compressor.infrastructure.adapters.common.uuid4_file_id_generator import UUID4FileIDGenerator
from compressor.infrastructure.adapters.common.uuid4_user_id_generator import UUID4UserIDGenerator
from compressor.infrastructure.adapters.persistence.alchemy_transaction_manager import SqlAlchemyTransactionManager
from compressor.infrastructure.adapters.persistence.alchemy_user_command_gateway import SqlAlchemyUserCommandGateway
from compressor.infrastructure.adapters.persistence.alchemy_user_query_gateway import SqlAlchemyUserQueryGateway
from compressor.infrastructure.adapters.persistence.s3_file_storage import S3FileStorage
from compressor.infrastructure.adapters.telegram_sender import TelegramSender
from compressor.infrastructure.cache.provider import get_redis, get_redis_pool
from compressor.infrastructure.event_bus.base import EventBus
from compressor.infrastructure.event_bus.bazario_event_bus import BazarioEventBus
from compressor.infrastructure.persistence.provider import (
    get_engine,
    get_s3_client,
    get_s3_session,
    get_session,
    get_sessionmaker,
)
from compressor.infrastructure.task_manager.files.base import FileTaskManager
from compressor.infrastructure.task_manager.files.task_iq import TaskIQFileTaskManager
from compressor.setup.configs.cache import RedisConfig
from compressor.setup.configs.database import PostgresConfig, SQLAlchemyConfig
from compressor.setup.configs.telegram import TGConfig


def configs_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.from_context(provides=PostgresConfig)
    provider.from_context(provides=SQLAlchemyConfig)
    provider.from_context(provides=PasswordPepper)
    provider.from_context(provides=RedisConfig)
    provider.from_context(provides=TGConfig)
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
    provider.provide(source=FileCompressorFactoryImpl, provides=FileCompressorFactory)
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


def sender_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide(TelegramSender, provides=Sender)
    return provider


def application_services_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide_all(FileCompressorService)
    return provider


def file_storage_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide(S3FileStorage, provides=FileStorage)
    provider.provide(get_s3_session)
    provider.provide(get_s3_client)
    return provider


def auth_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide(CurrentUserService)
    provider.provide(TelegramAccessRevoker, provides=AccessRevoker)
    return provider


def interactors_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide_all(
        ActivateUserCommandHandler,
        CreateUserCommandHandler,
        DeactivateUserCommandHandler,
        GrantAdminCommandHandler,
        LinkTelegramAccountCommandHandler,
        RevokeAdminCommandHandler,
        SignUpCommandHandler,
        CompressFileCommandHandler,
        DecompressFileCommandHandler,
    )
    return provider


class TelegramProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.REQUEST)
    def get_current_telegram_user_id(self, middleware_data: AiogramMiddlewareData) -> TelegramID | None:
        if current_chat := middleware_data.get("event_chat"):
            return cast(TelegramID, current_chat.id)  # noqa: TC006
        return None

    @provide(scope=scope.REQUEST)
    def get_current_bot(self, middleware_data: AiogramMiddlewareData) -> Bot | None:
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
        auth_provider(),
        sender_provider(),
        db_provider(),
        file_storage_provider(),
        interactors_provider(),
        application_services_provider(),
    )
