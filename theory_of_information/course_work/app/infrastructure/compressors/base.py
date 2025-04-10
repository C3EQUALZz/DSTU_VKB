from abc import ABC, abstractmethod

from app.domain.entities.file_objects import (CompressedFileObjectEntity,
                                              FileObjectEntity)


class Compressor(ABC):
    @abstractmethod
    def compress(self, backup: FileObjectEntity) -> CompressedFileObjectEntity:
        raise NotImplementedError

    @abstractmethod
    def decompress(self, compressed_backup: CompressedFileObjectEntity) -> FileObjectEntity:
        raise NotImplementedError
