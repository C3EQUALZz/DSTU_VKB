import os
from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class Settings:
    author_name: str = "Ковалев Данил Петрович"

    @classmethod
    def from_env(cls) -> Settings:
        return cls(author_name=os.environ.get("AUTHOR_NAME", "Ковалев Данил Петрович"))

    @property
    def copyright_year(self) -> int:
        return datetime.now(UTC).year
