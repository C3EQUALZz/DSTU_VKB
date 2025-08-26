from abc import abstractmethod
from enum import Enum
from typing import Protocol

from compressor.domain.compressors.services.base import Compressor


class CompressorType(Enum):
    GZIP = "gzip"
    FASTLZ = "fastlz"
    PIGZ = "pigz"
    LZMA = "lzma"
    BZIP2 = "bzip2"


class FileCompressorFactory(Protocol):
    @abstractmethod
    def create(self, compressor_type: CompressorType) -> Compressor:
        ...
