from app.infrastructure.brokers.publishers.schemas.user import UserCreateSchemaEvent, UserDeleteSchemaEvent, \
    UserUpdateSchemaEvent
from app.logic.events.users import UserCreateEvent, UserDeleteEvent, UserUpdateEvent
from app.logic.handlers.users.base import UsersEventHandler


class UserDeleteEventHandler(UsersEventHandler):
    async def __call__(self, event: UserDeleteEvent) -> None:
        await self._broker.send_message(
            topic=self._factory.get_topic(type(self)),
            value=UserDeleteSchemaEvent(**await event.to_dict()),
        )


class UserCreateEventHandler(UsersEventHandler):
    async def __call__(self, event: UserCreateEvent) -> None:
        await self._broker.send_message(
            topic=self._factory.get_topic(type(self)),
            value=UserCreateSchemaEvent(**await event.to_dict()),
        )


class UserUpdateEventHandler(UsersEventHandler):
    async def __call__(self, event: UserUpdateEvent) -> None:
        await self._broker.send_message(
            topic=self._factory.get_topic(type(self)),
            value=UserUpdateSchemaEvent(**await event.to_dict()),
        )
