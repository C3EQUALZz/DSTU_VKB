import logging
from pathlib import Path
from typing import Final

from compressor.domain.common.services.base import DomainService
from compressor.domain.files.entities.compressed_file import CompressedFile
from compressor.domain.files.entities.file import File
from compressor.domain.files.errors.file import FileDoesntExistError
from compressor.domain.files.ports.file_id_generator import FileIDGenerator
from compressor.domain.files.values.compression_type import CompressionType
from compressor.domain.files.values.file_size import FileSize

logger: Final[logging.Logger] = logging.getLogger(__name__)


class FileService(DomainService):
    def __init__(self, file_id_generator: FileIDGenerator) -> None:
        super().__init__()
        self._file_id_generator: Final[FileIDGenerator] = file_id_generator

    def create(self, path: Path) -> File:
        logger.debug("Started file creation in FileService")

        if not path.exists():
            raise FileDoesntExistError("File with current path does not exist: {}".format(path))

        is_dir: bool = path.is_dir()

        new_entity: File = File(
            id=self._file_id_generator(path),
            path=path,
            size=FileSize(path.stat().st_size),
            is_dir=is_dir
        )

        logger.debug("Successfully created file: %s", new_entity)

        return new_entity

    def create_compressed_file(self, path: Path, compression_type: CompressionType) -> CompressedFile:
        logger.debug("Started compressed file creation in FileService")

        if not path.exists():
            raise FileDoesntExistError("File with current path does not exist: {}".format(path))

        is_dir: bool = path.is_dir()

        new_entity: CompressedFile = CompressedFile(
            id=self._file_id_generator(path),
            path=path,
            size=FileSize(path.stat().st_size),
            is_dir=is_dir,
            compression_type=compression_type
        )


    def calculate_compression_ratio(self, compressed_file: CompressedFile, file: File) -> FileSize:
        return compressed_file.size / file.size
