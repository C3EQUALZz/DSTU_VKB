from dataclasses import dataclass

@dataclass(frozen=True, slots=True, kw_only=True)
class TelegramUserView:
    first_name: str
    role: str
    telegram_id: int
    language: str
