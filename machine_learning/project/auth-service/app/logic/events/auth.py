from app.logic.events.base import BaseEvent
from dataclasses import dataclass


@dataclass(frozen=True)
class UserRegisterEvent(BaseEvent):
    email: str
    name: str
    surname: str
    role: str
