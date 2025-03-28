import gzip
import logging
from pathlib import Path
from typing import Final

from typing_extensions import override

from app.domain.entities.file_objects import FileObject, CompressedFileObject
from app.domain.values.backup import CompressionType
from app.infrastructure.compressors.base import Compressor

logger = logging.getLogger(__name__)

CHUNK_SIZE: Final[int] = 64 * 1024  # 64KB

BACKUP_DIRECTORY_PATH = Path(__file__).resolve().parent.parent.parent.parent / "tmp"
BACKUP_DIRECTORY_PATH.mkdir(exist_ok=True)


class GunZipCompressor(Compressor):
    @override
    def compress(self, backup: FileObject, tmp_directory: Path = BACKUP_DIRECTORY_PATH) -> CompressedFileObject:
        source_path: Path = backup.file_path
        dest_path: Path = BACKUP_DIRECTORY_PATH / (source_path.name + '.gz')

        with open(source_path, 'rb') as f_in:
            with gzip.open(dest_path, 'wb') as f_out:
                while chunk := f_in.read(CHUNK_SIZE):
                    f_out.write(chunk)

        logger.debug(f"Compressed {source_path} to {dest_path}")

        return CompressedFileObject(
            file_path=dest_path,
            compression_type=CompressionType('gzip')
        )

    @override
    def decompress(self, backup: CompressedFileObject) -> FileObject:
        source_path: Path = backup.file_path
        dest_path: Path = source_path.with_suffix('')

        with gzip.open(source_path, 'rb') as f_in:
            with open(dest_path, 'wb') as f_out:
                while chunk := f_in.read(CHUNK_SIZE):
                    f_out.write(chunk)

        logger.debug(f"Decompressed {source_path} to {dest_path}")

        return FileObject(file_path=dest_path)
