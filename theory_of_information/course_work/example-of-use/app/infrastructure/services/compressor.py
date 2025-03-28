from pathlib import Path

from app.domain.entities.file_objects import CompressedFileObject, FileObject
from app.infrastructure.compressors.base import Compressor




class CompressorService:
    def __init__(self, compressor: Compressor) -> None:
        self._compressor = compressor

    def compress(self, file_object: FileObject) -> CompressedFileObject:
        return self._compressor.compress(file_object)

    def decompress(self, file_object: CompressedFileObject) -> FileObject:
        return self._compressor.decompress(file_object)
