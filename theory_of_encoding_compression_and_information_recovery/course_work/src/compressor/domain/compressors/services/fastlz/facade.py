import logging
from pathlib import Path
from typing import Final

from typing_extensions import override

from compressor.domain.compressors.services.base import Compressor
from compressor.domain.compressors.services.fastlz.interface import FastLzInterface
from compressor.domain.files.entities.compressed_file import CompressedFile
from compressor.domain.files.entities.file import File
from compressor.domain.files.services.file_service import FileService
from compressor.domain.files.values.compression_type import CompressionType

logger: Final[logging.Logger] = logging.getLogger(__name__)


class FastLZCompressor(Compressor):
    def __init__(self, file_service: FileService) -> None:
        super().__init__()
        self._compressor: Final[FastLzInterface] = FastLzInterface()
        self._file_service: Final[FileService] = file_service

    @override
    def compress(self, file: File) -> CompressedFile:
        source_path: Path = file.path
        dest_path: Path = source_path.with_suffix(source_path.suffix + ".fastlz")

        with Path.open(source_path, "rb") as f_in, open(dest_path, "wb") as f_out:
            data: bytearray = bytearray(f_in.read())
            f_out.write(bytes(self._compressor.compress(data, level=2)))

        logger.info(
            "Compressed %s to %s",
            source_path,
            dest_path,
        )

        return self._file_service.create_compressed_file(
            dest_path,
            compression_type=CompressionType.FASTLZ
        )

    @override
    def decompress(self, file: CompressedFile) -> File:
        source_path: Path = file.path
        dest_path: Path = source_path.with_suffix("")

        with Path.open(source_path, "rb") as f_in, Path.open(dest_path, "wb") as f_out:
            data: bytearray = bytearray(f_in.read())
            f_out.write(bytes(self._compressor.decompress(data)))

        logger.debug(f"Decompressed {source_path} to {dest_path}")

        return self._file_service.create(path=dest_path)
