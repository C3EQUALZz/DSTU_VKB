from abc import ABC, abstractmethod

from compressor.domain.common.services.base import DomainService
from compressor.domain.files.entities.compressed_file import CompressedFile
from compressor.domain.files.entities.file import File


class Compressor(DomainService, ABC):
    @abstractmethod
    def compress(self, file: File) -> CompressedFile:
        raise NotImplementedError

    @abstractmethod
    def decompress(self, file: CompressedFile) -> File:
        raise NotImplementedError
