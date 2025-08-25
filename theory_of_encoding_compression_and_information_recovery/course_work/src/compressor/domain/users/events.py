from dataclasses import dataclass, field

from compressor.domain.common.events import BaseDomainEvent


@dataclass(frozen=True, slots=True, eq=False)
class TelegramUserCreatedEvent(BaseDomainEvent):
    telegram_id: int
    first_name: str
    username: str | None
    last_name: str | None
    is_premium: bool
    is_bot: bool


@dataclass(frozen=True, slots=True, eq=False)
class TelegramUserUpdatedEvent(BaseDomainEvent):
    telegram_id: int
    first_name: str | None = field(default=None)
    username: str | None = field(default=None)
    last_name: str | None = field(default=None)
    is_premium: bool | None = field(default=None)
    is_bot: bool | None = field(default=None)
