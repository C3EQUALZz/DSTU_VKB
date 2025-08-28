from dataclasses import dataclass

from compressor.domain.compressors.factories.text.base import CompressorType
from compressor.domain.files.values.file_id import FileID


@dataclass(frozen=True, slots=True)
class CompressTextFileDTO:
    compressor_type: CompressorType
    file_id: FileID


@dataclass(frozen=True, slots=True)
class DecompressTextFileDTO:
    compressor_type: CompressorType
    file_id: FileID
