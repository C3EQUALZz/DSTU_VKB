from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class TelegramContactsData:
    telegram_id: int
    full_name: str
    telegram_username: str | None = None
