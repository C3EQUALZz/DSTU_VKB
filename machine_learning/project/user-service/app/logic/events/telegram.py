from dataclasses import dataclass

from app.logic.events.base import AbstractEvent


@dataclass(frozen=True)
class UserStartTelegramEvent(AbstractEvent):
    user_id: str
    telegram_id: int


@dataclass(frozen=True)
class UserSuccessfullyLinkedTelegramEvent(AbstractEvent):
    user_id: str
    telegram_id: int


@dataclass(frozen=True)
class UserFailedLinkedTelegramEvent(AbstractEvent):
    user_id: str
    telegram_id: int
