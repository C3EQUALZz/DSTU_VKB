from dataclasses import dataclass

from app.logic.events.base import AbstractEvent


@dataclass(frozen=True)
class UserCreateEvent(AbstractEvent):
    user_id: int
    full_name: str
    user_login: str
    role: str
    language_code: str


@dataclass(frozen=True)
class UserUpdateEvent(UserCreateEvent):
    ...


@dataclass(frozen=True)
class UserDeleteEvent(AbstractEvent):
    user_id: int


@dataclass(frozen=True)
class SendMessageSuccessLinkOrNotEvent(AbstractEvent):
    telegram_id: int
    message: str
