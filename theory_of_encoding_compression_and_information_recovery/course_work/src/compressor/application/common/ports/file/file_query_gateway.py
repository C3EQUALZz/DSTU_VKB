from abc import abstractmethod
from pathlib import Path
from typing import Protocol

from compressor.domain.files.entities.file import File
from compressor.domain.files.values.file_id import FileID


class FileQueryGateway(Protocol):
    @abstractmethod
    async def read_by_id(self, file: FileID) -> File:
        ...

    @abstractmethod
    async def read_by_path(self, path: Path) -> File:
        ...
