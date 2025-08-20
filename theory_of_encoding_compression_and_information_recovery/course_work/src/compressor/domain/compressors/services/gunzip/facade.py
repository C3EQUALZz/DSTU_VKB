import gzip
import logging
from pathlib import Path
from typing import Final

from compressor.domain.compressors.errors import CantDecompressThisFileError
from compressor.domain.compressors.services.gunzip.configuration import GunZipConfiguration
from compressor.domain.files.entities.compressed_file import CompressedFile
from compressor.domain.files.entities.file import File
from compressor.domain.files.values.compression_type import CompressionType
from compressor.domain.compressors.services.base import Compressor
from typing_extensions import override

from compressor.domain.files.services.file_service import FileService

logger: Final[logging.Logger] = logging.getLogger(__name__)


class GunZipCompressor(Compressor):
    def __init__(self, file_service: FileService) -> None:
        super().__init__()
        self._file_service: Final[FileService] = file_service
        self._gunzip_configuration: GunZipConfiguration = GunZipConfiguration()

    @override
    def compress(self, file: File) -> CompressedFile:
        source_path: Path = file.path
        dest_path: Path = source_path.with_suffix(source_path.suffix + '.gz')

        with Path.open(source_path, "rb") as f_in, gzip.open(dest_path, "wb") as f_out:
            while chunk := f_in.read(self._gunzip_configuration.CHUNK_SIZE):
                f_out.write(chunk)

        logger.debug("Compressed %s to %s", source_path, dest_path)

        return self._file_service.create_compressed_file(
            path=dest_path,
            compression_type=CompressionType.GZIP
        )

    @override
    def decompress(self, file: CompressedFile) -> File:
        if not file.path.suffix.endswith(CompressionType.GZIP):
            raise CantDecompressThisFileError("Expected .gzip file, not '%s'" % file.path.suffix)

        source_path: Path = file.path
        dest_path: Path = source_path.with_suffix("")

        with gzip.open(source_path, "rb") as f_in, Path.open(dest_path, "wb") as f_out:
            while chunk := f_in.read(self._gunzip_configuration.CHUNK_SIZE):
                f_out.write(chunk)

        logger.debug("Decompressed %s to %s", source_path, dest_path)

        return self._file_service.create(path=dest_path)
