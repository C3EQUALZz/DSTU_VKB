from app.domain.entities.file_objects import (
    CompressedFileObjectEntity,
    FileObjectEntity,
)
from app.infrastructure.compressors.base import Compressor


class CompressorService:
    def __init__(self, compressor: Compressor) -> None:
        self._compressor = compressor

    def compress(self, file_object: FileObjectEntity) -> CompressedFileObjectEntity:
        return self._compressor.compress(file_object)

    def decompress(self, file_object: CompressedFileObjectEntity) -> FileObjectEntity:
        return self._compressor.decompress(file_object)
