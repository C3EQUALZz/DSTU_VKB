from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True, kw_only=True)
class ReadTextQuery:
    path: Path


class ReadTextQueryHandler:
    def __call__(self, data: ReadTextQuery) -> str:
        return data.path.read_text(encoding="utf-8", errors="ignore")
