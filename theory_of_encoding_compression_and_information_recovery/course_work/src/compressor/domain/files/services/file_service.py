import logging
from io import BytesIO
from typing import TYPE_CHECKING, Final

from compressor.domain.common.services.base import DomainService
from compressor.domain.files.entities.compressed_file import CompressedFile
from compressor.domain.files.entities.file import File
from compressor.domain.files.ports.file_id_generator import FileIDGenerator
from compressor.domain.files.values.compression_type import CompressionType
from compressor.domain.files.values.file_name import FileName
from compressor.domain.files.values.file_size import FileSize

if TYPE_CHECKING:
    from compressor.domain.files.values.file_id import FileID

logger: Final[logging.Logger] = logging.getLogger(__name__)


class FileService(DomainService):
    def __init__(self, file_id_generator: FileIDGenerator) -> None:
        super().__init__()
        self._file_id_generator: Final[FileIDGenerator] = file_id_generator

    def create(self, data: BytesIO, file_name: FileName) -> File:
        logger.debug("Started file creation in FileService")
        file_id: FileID = self._file_id_generator()

        new_entity: File = File(
            id=file_id,
            file_name=file_name,
            size=FileSize(len(data.getvalue())),
            data=data,
        )

        logger.debug("Successfully created file: %s", new_entity)

        return new_entity

    def create_compressed_file(
        self, data: BytesIO, file_name: FileName, compression_type: CompressionType
    ) -> CompressedFile:
        logger.debug("Started compressed file creation in FileService")

        file_id: FileID = self._file_id_generator()

        new_entity: CompressedFile = CompressedFile(
            id=file_id,
            file_name=file_name,
            size=FileSize(len(data.getvalue())),
            compression_type=compression_type,
            data=data,
        )

        logger.debug("Successfully created file: %s", new_entity)

        return new_entity

    def calculate_compression_ratio(self, compressed_file: CompressedFile, file: File) -> FileSize:
        return compressed_file.size / file.size
