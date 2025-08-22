from typing import Protocol

from compressor.domain.files.entities.file import File
from compressor.domain.files.values.file_id import FileID


class FileCommandGateway(Protocol):
    async def add(self, file: File) -> None:
        ...

    async def read_by_id(self, file_id: FileID) -> File:
        ...