import logging
from typing import (
    Any,
    cast,
)

from app.core.types.handlers import (
    CommandHandlerMapping,
    EventHandlerMapping,
)
from app.infrastructure.uow.scores.base import ScoresUnitOfWork
from app.infrastructure.uow.scores.mongo import MotorScoresUnitOfWork
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.infrastructure.uow.users.mongo import MotorUsersUnitOfWork
from app.logic.commands.auth import VerifyUserCredentialsCommand
from app.logic.commands.scores import (
    CreateScoreCommand,
    DeleteScoreCommand,
    GetAllScoresCommand,
    GetAllUserScoresCommand,
    GetScoreByIdCommand,
    UpdateScoreCommand,
)
from app.logic.commands.users import (
    CreateUserCommand,
    GetAllUsersCommand,
    GetUserByIdCommand,
    UpdateUserCommand,
)
from app.logic.handlers.auth.commands import VerifyUserCredentialsCommandHandler
from app.logic.handlers.scores.commands import (
    CreateScoreCommandHandler,
    DeleteScoreCommandHandler,
    GetAllScoresCommandHandler,
    GetAllUserScoresCommandHandler,
    GetScoreByIdCommandHandler,
    UpdateScoreCommandHandler,
)
from app.logic.handlers.users.commands import (
    CreateUserCommandHandler,
    GetAllUsersCommandHandler,
    GetUserByIdCommandHandler,
    UpdateUserCommandHandler,
)
from app.settings.config import Settings
from authx import (
    AuthX,
    AuthXConfig,
)
from dishka import (
    from_context,
    make_async_container,
    provide,
    Provider,
    Scope,
)
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import (
    ConnectionPool,
    Redis,
)


logger = logging.getLogger(__name__)


class AuthProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_config(self, settings: Settings) -> AuthXConfig:
        return AuthXConfig(
            JWT_ALGORITHM="RS256", JWT_PRIVATE_KEY=settings.auth.private_key, JWT_PUBLIC_KEY=settings.auth.public_key
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
    async def get_client(self, pool: ConnectionPool) -> Redis:
        return Redis.from_pool(pool)


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
                GetAllUsersCommand: GetAllUsersCommandHandler,
                GetUserByIdCommand: GetUserByIdCommandHandler,
                UpdateUserCommand: UpdateUserCommandHandler,
                VerifyUserCredentialsCommand: VerifyUserCredentialsCommandHandler,
                CreateScoreCommand: CreateScoreCommandHandler,
                GetAllScoresCommand: GetAllScoresCommandHandler,
                GetScoreByIdCommand: GetScoreByIdCommandHandler,
                UpdateScoreCommand: UpdateScoreCommandHandler,
                DeleteScoreCommand: DeleteScoreCommandHandler,
                GetAllUserScoresCommand: GetAllUserScoresCommandHandler,
            },
        )

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

    @provide(scope=Scope.APP)
    async def get_scores_motor_uow(self, settings: Settings, client: AsyncIOMotorClient[Any]) -> ScoresUnitOfWork:
        return MotorScoresUnitOfWork(client=client, database_name=settings.database.database_name)


container = make_async_container(
    AppProvider(),
    HandlerProvider(),
    AuthProvider(),
    RedisProvider(),
    context={
        Settings: Settings(),
    },
)
