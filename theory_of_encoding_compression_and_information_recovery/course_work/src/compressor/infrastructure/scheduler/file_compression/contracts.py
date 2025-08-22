from dataclasses import dataclass

from compressor.domain.compressors.services.factory import CompressorType
from compressor.domain.files.values.file_id import FileID


@dataclass(frozen=True, slots=True, kw_only=True)
class FileInfoDTO:
    file_id: FileID
    compressor_type: CompressorType
