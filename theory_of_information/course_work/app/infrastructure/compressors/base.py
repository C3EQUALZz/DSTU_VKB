from abc import (
    ABC,
    abstractmethod,
)

from app.domain.entities.file_objects import (
    CompressedFileObject,
    FileObject,
)


class Compressor(ABC):
    @abstractmethod
    def compress(self, backup: FileObject) -> CompressedFileObject:
        raise NotImplementedError

    @abstractmethod
    def decompress(self, compressed_backup: CompressedFileObject) -> FileObject:
        raise NotImplementedError
