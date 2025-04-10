import gzip
import logging
from pathlib import Path

from app.domain.entities.file_objects import (CompressedFileObjectEntity,
                                              FileObjectEntity)
from app.domain.values.backup import CompressionType
from app.infrastructure.compressors.base import Compressor
from app.infrastructure.compressors.gunzip import CHUNK_SIZE
from app.infrastructure.compressors.pigz.interface import compress_file
from typing_extensions import override

logger = logging.getLogger(__name__)


class PigzCompressor(Compressor):
    @override
    def compress(self, backup: FileObjectEntity) -> CompressedFileObjectEntity:
        compress_file(backup.file_path)

        logger.debug(f"Compressed to {backup.file_path}")

        return CompressedFileObjectEntity(
            backup.file_path,
            compression_type=CompressionType("gzip"),
        )

    @override
    def decompress(self, backup: CompressedFileObjectEntity) -> FileObjectEntity:
        source_path: Path = backup.file_path
        dest_path: Path = source_path.with_suffix("")

        with gzip.open(source_path, "rb") as f_in, Path.open(dest_path, "wb") as f_out:
            while chunk := f_in.read(CHUNK_SIZE):
                f_out.write(chunk)

        logger.debug(f"Decompressed {source_path} to {dest_path}")

        return FileObjectEntity(file_path=dest_path)
