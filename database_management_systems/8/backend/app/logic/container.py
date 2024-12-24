from dishka import Provider, Scope, provide, from_context, make_async_container
from motor.motor_asyncio import AsyncIOMotorClient

from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.infrastructure.uow.users.mongo import MotorUsersUnitOfWork
from app.settings.config import Settings


class AppProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_motor_client(self, settings: Settings) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(str(settings.database.url))

    @provide(scope=Scope.APP)
    def get_users_motor_uow(self, settings: Settings, client: AsyncIOMotorClient) -> UsersUnitOfWork:
        return MotorUsersUnitOfWork(client=client, database_name=settings.database.database_name)


container = make_async_container(
    AppProvider(),
    context={
        Settings: Settings(),
    }
)
