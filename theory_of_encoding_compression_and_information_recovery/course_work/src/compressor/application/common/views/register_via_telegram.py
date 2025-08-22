from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class RegisterViaTelegramView:
    user_id: UUID
    telegram_id: int
    name: str
