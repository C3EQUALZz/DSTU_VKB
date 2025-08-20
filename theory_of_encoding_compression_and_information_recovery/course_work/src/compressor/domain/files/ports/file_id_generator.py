from abc import abstractmethod
from pathlib import Path
from typing import Protocol

from compressor.domain.files.values.file_id import FileID


class FileIDGenerator(Protocol):
    @abstractmethod
    def __call__(self, path: Path) -> FileID:
        ...
