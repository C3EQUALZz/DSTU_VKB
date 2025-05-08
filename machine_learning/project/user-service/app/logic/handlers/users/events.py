from app.infrastructure.brokers.publishers.schemas.user import UserCreateSchemaEvent, UserDeleteSchemaEvent, \
    UserUpdateSchemaEvent
from app.logic.events.users import UserCreatedEvent, UserDeletedEvent, UserUpdatedEvent
from app.logic.handlers.users.base import UsersEventHandler


class UserDeletedEventHandler(UsersEventHandler):
    async def __call__(self, event: UserDeletedEvent) -> None:
        await self._broker.send_message(
            topic=self._factory.get_topic(type(self)),
            value=UserDeleteSchemaEvent(**event.to_dict()),
        )


class UserCreatedEventHandler(UsersEventHandler):
    async def __call__(self, event: UserCreatedEvent) -> None:
        await self._broker.send_message(
            topic=self._factory.get_topic(type(self)),
            value=UserCreateSchemaEvent(**event.to_dict()),
        )


class UserUpdatedEventHandler(UsersEventHandler):
    async def __call__(self, event: UserUpdatedEvent) -> None:
        await self._broker.send_message(
            topic=self._factory.get_topic(type(self)),
            value=UserUpdateSchemaEvent(**event.to_dict()),
        )
