import os
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path


def database_path_from_env() -> Path:
    return Path(os.environ.get("DATABASE_PATH", "data/securedev.db")).resolve()


@dataclass(frozen=True, slots=True, kw_only=True)
class Settings:
    secret_key: str = field(repr=False)
    author_name: str = "Ковалев Данил Петрович"
    log_path: Path = field(default_factory=lambda: Path("logs/calc_log.txt").resolve())
    database_path: Path = field(default_factory=database_path_from_env)
    secure_cookies: bool = False

    def __post_init__(self) -> None:
        if len(self.secret_key) < 32:
            raise ValueError("Задайте случайный SECRET_KEY длиной не менее 32 символов.")

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            secret_key=os.environ.get("SECRET_KEY", ""),
            author_name=os.environ.get("AUTHOR_NAME", "Ковалев Данил Петрович"),
            log_path=Path(os.environ.get("CALC_LOG_PATH", "logs/calc_log.txt")).resolve(),
            secure_cookies=os.environ.get("SESSION_COOKIE_SECURE") == "1",
        )

    @property
    def copyright_year(self) -> int:
        return datetime.now(UTC).year
