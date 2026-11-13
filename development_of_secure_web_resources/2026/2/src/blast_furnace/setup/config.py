import os
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path


@dataclass(frozen=True, slots=True, kw_only=True)
class Settings:
    author_name: str = "Ковалев Данил Петрович"
    log_path: Path = field(default_factory=lambda: Path("static/calc_log.txt").resolve())

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            author_name=os.environ.get("AUTHOR_NAME", "Ковалев Данил Петрович"),
            log_path=Path(
                os.environ.get("CALC_LOG_PATH", "static/calc_log.txt")
            ).resolve(),
        )

    @property
    def copyright_year(self) -> int:
        return datetime.now(UTC).year
