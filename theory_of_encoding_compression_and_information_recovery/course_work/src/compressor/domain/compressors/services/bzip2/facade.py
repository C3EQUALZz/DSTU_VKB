import bz2
import logging
from pathlib import Path
from typing import Final

from compressor.domain.compressors.errors import CantDecompressThisFileError
from compressor.domain.compressors.services.bzip2.configuration import BZip2Configuration
from compressor.domain.files.entities.compressed_file import CompressedFile
from compressor.domain.files.entities.file import File
from compressor.domain.files.values.compression_type import CompressionType
from compressor.domain.compressors.services.base import Compressor
from typing_extensions import override

from compressor.domain.files.services.file_service import FileService

logger: Final[logging.Logger] = logging.getLogger(__name__)


class BZip2Compressor(Compressor):
    def __init__(self, file_service: FileService) -> None:
        super().__init__()
        self._file_service: Final[FileService] = file_service
        self._bzip2_configuration: BZip2Configuration = BZip2Configuration()

    @override
    def compress(self, file: File) -> CompressedFile:
        source_path: Path = file.path
        dest_path: Path = source_path.with_suffix(source_path.suffix + '.bz2')

        with Path.open(
                source_path,
                "rb"
        ) as f_in, bz2.open(
                dest_path,
            "wb",
            compresslevel=self._bzip2_configuration.COMPRESS_LEVEL
        ) as f_out:
            while chunk := f_in.read(self._bzip2_configuration.CHUNK_SIZE):
                f_out.write(chunk)

        logger.debug("Compressed %s to %s", source_path, dest_path)

        return self._file_service.create_compressed_file(
            path=dest_path,
            compression_type=CompressionType.BZIP2
        )

    @override
    def decompress(self, file: CompressedFile) -> File:
        if not file.path.suffix.endswith(CompressionType.BZIP2):
            raise CantDecompressThisFileError("Expected .bz2 file, not '%s'" % file.path.suffix)

        source_path: Path = file.path
        dest_path: Path = source_path.with_suffix("")

        with bz2.open(source_path, "rb") as f_in, Path.open(dest_path, "wb") as f_out:
            while chunk := f_in.read(self._bzip2_configuration.CHUNK_SIZE):
                f_out.write(chunk)

        logger.debug("Decompressed %s to %s", source_path, dest_path)

        return self._file_service.create(path=dest_path)