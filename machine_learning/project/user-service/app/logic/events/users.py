from dataclasses import dataclass, field

from app.logic.events.base import AbstractEvent


@dataclass(frozen=True)
class UserCreatedEvent(AbstractEvent):
    oid: str
    first_name: str
    role: str


@dataclass(frozen=True)
class UserDeletedEvent(AbstractEvent):
    user_oid: str


@dataclass(frozen=True)
class UserUpdatedEvent(UserCreatedEvent):
    ...


@dataclass(frozen=True)
class UserCreateFromTelegramBotEvent(UserCreatedEvent):
    oid: str
    first_name: str
    role: str
    telegram_id: int


@dataclass(frozen=True)
class UserUpdateFromTelegramBotEvent(AbstractEvent):
    oid: str
    first_name: str | None = field(default=None)
    telegram_id: int | None = field(default=None)
    role: str | None = field(default=None)


@dataclass(frozen=True)
class UserDeleteFromTelegramBotEvent(AbstractEvent):
    oid: str
