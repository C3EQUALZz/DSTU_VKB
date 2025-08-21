from abc import abstractmethod
from typing import Protocol
from enum import Enum


class ThrottleResponse(Enum):
    SUSPICIOUS_ACTIVITY = "SUSPICIOUS_ACTIVITY"
    BLOCKED = "BLOCKED"
    NORMAL = "NORMAL"


class ThrottleManager(Protocol):
    @abstractmethod
    async def __call__(self, user_id: int) -> ThrottleResponse:
        ...
