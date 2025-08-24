from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class RegisterViaTelegramView:
    user_id: UUID
    telegram_id: int
    name: str


@dataclass(frozen=True, slots=True, kw_only=True)
class TelegramUserView:
    first_name: str
    role: str
    telegram_id: int
    language: str