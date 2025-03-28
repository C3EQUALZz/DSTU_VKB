from dataclasses import dataclass
from pathlib import Path

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class CompressFileCommand(AbstractCommand):
    src_file_path: Path
    compress_type: str


@dataclass(frozen=True)
class DecompressFileCommand(AbstractCommand):
    src_file_path: Path
    compress_type: str
