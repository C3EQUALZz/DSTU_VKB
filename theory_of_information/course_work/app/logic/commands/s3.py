from pathlib import Path

from app.logic.commands.base import AbstractCommand
from dataclasses import dataclass


@dataclass(frozen=True)
class CreateFileInS3Command(AbstractCommand):
    file_path: Path
    delete: bool


@dataclass(frozen=True)
class GetFileFromS3Command(AbstractCommand):
    oid: str


@dataclass(frozen=True)
class DeleteFileFromS3Command(AbstractCommand):
    oid: str


@dataclass(frozen=True)
class ListFilesInS3Command(AbstractCommand):
    start: int
    end: int
