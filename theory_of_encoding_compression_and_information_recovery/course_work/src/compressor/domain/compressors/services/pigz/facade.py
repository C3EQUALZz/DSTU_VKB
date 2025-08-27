import logging
from typing import Final

from typing_extensions import override

from compressor.domain.compressors.services.base import Compressor
from compressor.domain.compressors.services.gunzip.facade import GunZipCompressor
from compressor.domain.compressors.services.pigz.configuration import Configuration
from compressor.domain.compressors.services.pigz.pigz_file import PigzFile
from compressor.domain.files.entities.compressed_file import CompressedFile
from compressor.domain.files.entities.file import File
from compressor.domain.files.services.file_service import FileService
from compressor.domain.files.values.compression_type import CompressionType

logger: Final[logging.Logger] = logging.getLogger(__name__)


class PigzCompressor(Compressor):
    def __init__(self, file_service: FileService, gzip_compressor: GunZipCompressor) -> None:
        super().__init__()
        self._file_service: Final[FileService] = file_service
        self._gzip_compressor: Final[GunZipCompressor] = gzip_compressor
        self._pigz_configuration: Final[Configuration] = Configuration()

    @override
    def compress(self, file: File) -> CompressedFile:
        pigz_file = PigzFile(file.path, configuration=self._pigz_configuration)
        pigz_file.process_compression_target()

        logger.debug("Compressed to %s", file.path)

        return self._file_service.create_compressed_file(
            path=file.path,
            compression_type=CompressionType.GZIP,
        )

    @override
    def decompress(self, file: CompressedFile) -> File:
        return self._gzip_compressor.decompress(file=file)
