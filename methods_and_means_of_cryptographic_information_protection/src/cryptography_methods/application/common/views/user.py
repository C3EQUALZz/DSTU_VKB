from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class UserView:
    first_name: str
    role: str
    language: str
    telegram_id: int | None = field(default=None)
    last_name: str | None = field(default=None)
