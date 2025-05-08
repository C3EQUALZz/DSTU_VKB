from dataclasses import dataclass, field
from datetime import datetime, UTC

from app.logic.commands.base import BaseCommand
from app.logic.events.base import BaseEvent


@dataclass(frozen=True)
class CacheErrorEvent(BaseEvent):
    source: BaseEvent | BaseCommand
    microservice_name: str = field(default="auth-service", kw_only=True)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC), kw_only=True)
