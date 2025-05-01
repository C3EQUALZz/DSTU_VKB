from app.infrastructure.brokers.schemas.users import UserCreateSchema, UserDeleteSchema, UserUpdateSchema
from app.logic.events.user import UserCreateEvent, UserUpdateEvent, UserDeleteEvent
from app.logic.handlers.users.base import UsersEventHandler


class UserCreateEventHandler(UsersEventHandler[UserCreateEvent]):
    async def __call__(self, event: UserCreateEvent) -> None:
        topic: str = self._event_factory.get_topic(self.__class__)

        await self._broker.send_message(
            topic=topic,
            value=UserCreateSchema(
                full_name=event.full_name,
                user_login=event.user_login,
                role=event.role,  # noqa
                language_code=event.language_code,
                id=event.user_id
            )
        )


class UserUpdateEventHandler(UsersEventHandler[UserUpdateEvent]):
    async def __call__(self, event: UserUpdateEvent) -> None:
        topic: str = self._event_factory.get_topic(self.__class__)

        await self._broker.send_message(
            topic=topic,
            value=UserUpdateSchema(
                full_name=event.full_name,
                user_login=event.user_login,
                role=event.role,  # noqa
                language_code=event.language_code,
                id=event.user_id
            )
        )


class UserDeleteEventHandler(UsersEventHandler[UserDeleteEvent]):
    async def __call__(self, event: UserDeleteEvent) -> None:
        topic: str = self._event_factory.get_topic(self.__class__)

        await self._broker.send_message(
            topic=topic,
            value=UserDeleteSchema(id=event.user_id)
        )
