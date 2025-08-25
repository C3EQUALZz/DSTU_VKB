from dataclasses import dataclass
from pathlib import Path
from io import BytesIO
from compressor.domain.common.entities.base_entity import BaseEntity
from compressor.domain.files.values.compression_type import CompressionType
from compressor.domain.files.values.file_id import FileID
from compressor.domain.files.values.file_size import FileSize


@dataclass(eq=False, kw_only=True)
class CompressedFile(BaseEntity[FileID]):
    path: Path
    data: BytesIO
    size: FileSize
    compression_type: CompressionType
