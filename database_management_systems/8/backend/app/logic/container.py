import logging

from dishka import Provider, Scope, provide, from_context, make_async_container
from motor.motor_asyncio import AsyncIOMotorClient

from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.infrastructure.uow.users.mongo import MotorUsersUnitOfWork
from app.settings.config import Settings

logger = logging.getLogger(__name__)


class AppProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_motor_client(self, settings: Settings) -> AsyncIOMotorClient:
        client: AsyncIOMotorClient = AsyncIOMotorClient(str(settings.database.url))

        if info := await client.server_info():
            logger.debug("Successfully connected to MongoDB, info [%s]", info)

        return client

    @provide(scope=Scope.APP)
    async def get_users_motor_uow(self, settings: Settings, client: AsyncIOMotorClient) -> UsersUnitOfWork:
        return MotorUsersUnitOfWork(client=client, database_name=settings.database.database_name)


container = make_async_container(
    AppProvider(),
    context={
        Settings: Settings(),
    }
)
