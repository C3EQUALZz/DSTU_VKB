from app.logic.events.users import UserDeleteEvent, UserCreateEvent, UserUpdateEvent
from app.logic.handlers.users.base import UsersEventHandler


class UserDeleteEventHandler(UsersEventHandler[UserDeleteEvent]):
    async def __call__(self, event: UserDeleteEvent) -> None:
        await self._broker.send_message(
            topic="delete-user",
            value=await event.to_broker_message(),
            key=str(event.oid).encode(),
        )


class UserCreateEventHandler(UsersEventHandler[UserCreateEvent]):
    async def __call__(self, event: UserCreateEvent) -> None:
        await self._broker.send_message(
            topic="create-user",
            value=await event.to_broker_message(),
            key=str(event.oid).encode(),
        )


class UserUpdateEventHandler(UsersEventHandler[UserUpdateEvent]):
    async def __call__(self, event: UserCreateEvent) -> None:
        await self._broker.send_message(
            topic="update-user",
            value=await event.to_broker_message(),
            key=str(event.oid).encode(),
        )
