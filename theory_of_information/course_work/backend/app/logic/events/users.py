from dataclasses import dataclass

from app.logic.events.base import AbstractEvent


@dataclass(frozen=True)
class UserCreateEvent(AbstractEvent):
    oid: str
    email: str
    surname: str
    name: str
    patronymic: str


@dataclass(frozen=True)
class UserDeleteEvent(AbstractEvent):
    user_oid: str


@dataclass(frozen=True)
class UserUpdateEvent(AbstractEvent):
    oid: str
    email: str
    surname: str
    name: str
    patronymic: str
