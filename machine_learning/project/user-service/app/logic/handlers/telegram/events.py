from app.domain.entities.user import UserEntity
from app.exceptions.infrastructure import UserNotFoundError
from app.infrastructure.brokers.publishers.schemas.telegram import SendMessageToTelegramSchema
from app.infrastructure.services.users import UsersService
from app.logic.events.telegram import UserStartTelegramEvent, UserSuccessfullyLinkedTelegramEvent, \
    UserFailedLinkedTelegramEvent
from app.logic.handlers.telegram.base import UsersTelegramEventHandler


class UserStartTelegramEventHandler(UsersTelegramEventHandler[UserStartTelegramEvent]):
    async def __call__(self, event: UserStartTelegramEvent) -> None:
        async with self._users_uow as uow:
            user_service: UsersService = UsersService(uow)

            try:
                user_entity: UserEntity = await user_service.get_by_id(event.user_id)
                user_entity.telegram_id = event.telegram_id

                await user_service.update(user_entity)
                self._event_buffer.add(
                    UserSuccessfullyLinkedTelegramEvent(
                        user_id=user_entity.oid,
                        telegram_id=user_entity.telegram_id,
                    )
                )

            except UserNotFoundError:
                self._event_buffer.add(
                    UserFailedLinkedTelegramEvent(
                        user_id=event.user_id,
                        telegram_id=event.telegram_id,
                    )
                )


class UserSuccessfullyLinkedTelegramEventHandler(UsersTelegramEventHandler[UserSuccessfullyLinkedTelegramEvent]):
    async def __call__(self, event: UserSuccessfullyLinkedTelegramEvent) -> None:
        topic: str = self._factory.get_topic(self.__class__)

        await self._broker.send_message(
            topic=topic,
            value=SendMessageToTelegramSchema(
                event_id=event.oid,  # type: ignore
                telegram_id=event.telegram_id,
                message="You successfully linked telegram and backend!",
            )
        )


class UserFailedLinkedTelegramEventHandler(UsersTelegramEventHandler[UserFailedLinkedTelegramEvent]):
    async def __call__(self, event: UserFailedLinkedTelegramEvent) -> None:
        topic: str = self._factory.get_topic(self.__class__)

        await self._broker.send_message(
            topic=topic,
            value=SendMessageToTelegramSchema(
                event_id=event.oid,  # type: ignore
                telegram_id=event.telegram_id,
                message="You failed to linked telegram and backend! Please try again.",
            )
        )
