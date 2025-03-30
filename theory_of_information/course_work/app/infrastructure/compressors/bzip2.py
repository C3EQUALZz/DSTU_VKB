import bz2
import logging
from pathlib import Path
from typing import (
    Final,
)

from typing_extensions import override

from app.application.cli.const import BACKUP_DIRECTORY_PATH
from app.domain.entities.file_objects import (
    CompressedFileObjectEntity,
    FileObjectEntity,
)

from app.domain.values.backup import CompressionType
from app.infrastructure.compressors.base import Compressor

logger = logging.getLogger(__name__)

CHUNK_SIZE: Final[int] = 1024 * 1024  # 1MB chunks


class Bzip2Compressor(Compressor):
    @override
    def compress(self, backup: FileObjectEntity) -> CompressedFileObjectEntity:
        source_path: Path = backup.file_path
        dest_path: Path = BACKUP_DIRECTORY_PATH / (source_path.name + ".bz2")

        with Path.open(source_path, "rb") as f_in, bz2.open(dest_path, "wb") as f_out:
            while chunk := f_in.read(CHUNK_SIZE):
                f_out.write(chunk)

        logger.info(f"Compressed {source_path} to {dest_path}")

        return CompressedFileObjectEntity(
            file_path=dest_path,
            compression_type=CompressionType("bzip2")
        )

    @override
    def decompress(self, backup: CompressedFileObjectEntity) -> FileObjectEntity:
        source_path: Path = backup.file_path
        dest_path: Path = source_path.with_suffix("")

        with bz2.open(source_path, "rb") as f_in, Path.open(dest_path, "wb") as f_out:
            while chunk := f_in.read(CHUNK_SIZE):
                f_out.write(chunk)

        logger.debug(f"Decompressed {source_path} to {dest_path}")

        return FileObjectEntity(file_path=dest_path)
