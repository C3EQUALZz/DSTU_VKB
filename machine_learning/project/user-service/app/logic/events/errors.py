from dataclasses import dataclass, field
from datetime import datetime, UTC

from app.logic.commands.base import AbstractCommand
from app.logic.events.base import AbstractEvent


@dataclass(frozen=True)
class CacheErrorEvent(AbstractEvent):
    source: AbstractEvent | AbstractCommand
    microservice_name: str = field(default="user-service", kw_only=True)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC), kw_only=True)
