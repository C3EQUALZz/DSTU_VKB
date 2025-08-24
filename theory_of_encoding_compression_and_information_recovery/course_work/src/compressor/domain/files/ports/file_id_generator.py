from abc import abstractmethod
from typing import Protocol

from compressor.domain.files.values.file_id import FileID


class FileIDGenerator(Protocol):
    @abstractmethod
    def __call__(self) -> FileID:
        ...
