import lzma
import logging
from pathlib import Path
from typing import Final

from compressor.domain.compressors.services.lempel_ziv_markov_chain.configuration import LZMAConfiguration
from compressor.domain.files.entities.compressed_file import CompressedFile
from compressor.domain.files.entities.file import File
from compressor.domain.files.values.compression_type import CompressionType
from compressor.domain.compressors.services.base import Compressor
from typing_extensions import override

from compressor.domain.files.services.file_service import FileService

logger: Final[logging.Logger] = logging.getLogger(__name__)


class LZMACompressor(Compressor):
    def __init__(self, file_service: FileService) -> None:
        super().__init__()
        self._file_service: Final[FileService] = file_service
        self._lzma_configuration: LZMAConfiguration = LZMAConfiguration()

    @override
    def compress(self, file: File) -> CompressedFile:
        source_path: Path = file.path
        dest_path: Path = source_path.with_suffix(source_path.suffix + '.xz')

        with Path.open(
                source_path,
                "rb"
        ) as f_in, lzma.open(
            dest_path,
            "wb",
            preset=self._lzma_configuration.COMPRESS_LEVEL,
            format=lzma.FORMAT_XZ
        ) as f_out:
            while chunk := f_in.read(self._lzma_configuration.CHUNK_SIZE):
                f_out.write(chunk)

        logger.debug("Compressed %s to %s", source_path, dest_path)

        return self._file_service.create_compressed_file(
            path=dest_path,
            compression_type=CompressionType.LZMA
        )

    @override
    def decompress(self, file: CompressedFile) -> File:
        source_path: Path = file.path
        dest_path: Path = source_path.with_suffix("")

        with lzma.open(source_path, "rb") as f_in, Path.open(dest_path, "wb") as f_out:
            while chunk := f_in.read(self._lzma_configuration.CHUNK_SIZE):
                f_out.write(chunk)

        logger.debug("Decompressed %s to %s", source_path, dest_path)

        return self._file_service.create(path=dest_path)
