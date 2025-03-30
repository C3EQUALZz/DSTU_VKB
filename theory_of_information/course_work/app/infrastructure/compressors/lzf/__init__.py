import logging
from pathlib import Path

from typing_extensions import override

from app.application.cli.const import BACKUP_DIRECTORY_PATH
from app.domain.entities.file_objects import FileObject, CompressedFileObject
from app.domain.values.backup import CompressionType
from app.infrastructure.compressors.base import Compressor
from app.infrastructure.compressors.lzf.interface import LzfInterface

logger = logging.getLogger(__name__)

class LzfCompressor(Compressor):
    def __init__(self) -> None:
        self._compressor = LzfInterface()

    @override
    def compress(self, backup: FileObject) -> CompressedFileObject:
        source_path: Path = backup.file_path
        dest_path: Path = BACKUP_DIRECTORY_PATH / (source_path.name + ".lzf")

        with Path.open(source_path, "rb") as f_in, open(dest_path, "wb") as f_out:
            data: bytearray = bytearray(f_in.read())
            f_out.write(bytes(self._compressor.compress(data)))

        logger.info(f"Compressed {source_path} to {dest_path}")

        return CompressedFileObject(
            dest_path,
            compression_type=CompressionType("lzf")
        )

    @override
    def decompress(self, compressed_backup: CompressedFileObject) -> FileObject:
        source_path: Path = compressed_backup.file_path
        dest_path: Path = source_path.with_suffix("")

        with Path.open(source_path, "rb") as f_in, Path.open(dest_path, "wb") as f_out:
            data: bytearray = bytearray(f_in.read())
            f_out.write(bytes(self._compressor.decompress(data)))

        logger.debug(f"Decompressed {source_path} to {dest_path}")

        return FileObject(file_path=dest_path)
