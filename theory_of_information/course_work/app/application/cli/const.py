from pathlib import Path
from typing import Final

BACKUP_DIRECTORY_PATH: Final[Path] = Path(__file__).resolve().parent.parent.parent.parent / "tmp"
