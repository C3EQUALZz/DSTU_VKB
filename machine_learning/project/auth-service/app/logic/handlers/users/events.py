from typing import override, cast, Literal

from pydantic import EmailStr

from app.infrastructure.brokers.schemas.users import UserRegisterEventForBrokerSchema, \
    UserSendEmailForVerificationSchema
from app.logic.events.auth import UserRegisterEvent
from app.logic.handlers.users.base import UsersEventHandler


class UserRegisterEventHandler(UsersEventHandler[UserRegisterEvent]):
    @override
    async def __call__(self, event: UserRegisterEvent) -> None:
        topic: str = self._factory.get_topic(self.__class__)
        await self._broker.send_message(
            topic=topic,
            value=UserRegisterEventForBrokerSchema(
                email=cast(EmailStr, event.email),
                name=event.name,
                surname=event.surname,
                role=cast(Literal["user", "admin"], event.role),
            )
        )


class SendEmailToVerifyEventHandler(UsersEventHandler[UserRegisterEvent]):
    @override
    async def __call__(self, event: UserRegisterEvent) -> None:
        topic: str = self._factory.get_topic(self.__class__)
        await self._broker.send_message(
            topic=topic,
            value=UserSendEmailForVerificationSchema(
                email=cast(EmailStr, event.email),
                name=event.name,
                surname=event.surname,
            )
        )
