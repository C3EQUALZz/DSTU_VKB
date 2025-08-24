from abc import abstractmethod
from typing import Protocol

from compressor.domain.files.entities.file import File
from compressor.domain.files.values.file_id import FileID


class FileCommandGateway(Protocol):
    @abstractmethod
    async def add(self, file: File) -> None:
        ...

    @abstractmethod
    async def read_by_id(self, file_id: FileID) -> File:
        ...
