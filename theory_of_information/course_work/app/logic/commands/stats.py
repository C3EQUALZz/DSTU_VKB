from dataclasses import dataclass
from pathlib import Path

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class GetFileFullStatsCommand(AbstractCommand):
    file_path: Path
