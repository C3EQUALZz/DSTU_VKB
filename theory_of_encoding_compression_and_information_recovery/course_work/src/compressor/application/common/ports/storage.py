from abc import abstractmethod
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Protocol

from compressor.domain.files.values.file_id import FileID


@dataclass(frozen=True, slots=True, kw_only=True)
class FileStorageDTO:
    file_id: FileID
    path: Path
    data: BytesIO


class FileStorage(Protocol):
    @abstractmethod
    async def add(self, dto: FileStorageDTO) -> None:
        ...

    @abstractmethod
    async def read_by_id(self, file_id: FileID) -> FileStorageDTO | None:
        ...

    @abstractmethod
    async def delete_by_id(self, file_id: FileID) -> None:
        ...
