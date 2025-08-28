import logging
from typing import TYPE_CHECKING, Final

from compressor.application.common.ports.storage import FileStorage, FileStorageDTO
from compressor.application.common.views.files import CompressedFileView, DecompressedFileView
from compressor.application.errors.compressor import FileForCompressionNotFoundError
from compressor.application.services.files.contracts import CompressTextFileDTO, DecompressTextFileDTO
from compressor.domain.compressors.factories.text.base import FileCompressorFactory
from compressor.domain.files.services.file_service import FileService
from compressor.domain.files.values.compression_type import CompressionType

if TYPE_CHECKING:
    from compressor.domain.compressors.services.base import Compressor
    from compressor.domain.files.entities.compressed_file import CompressedFile
    from compressor.domain.files.entities.file import File

logger: Final[logging.Logger] = logging.getLogger(__name__)


class FileCompressorService:
    def __init__(
        self,
        file_compressor_factory: FileCompressorFactory,
        file_storage: FileStorage,
        file_service: FileService,
    ) -> None:
        self._file_compressor_factory: Final[FileCompressorFactory] = file_compressor_factory
        self._file_storage: Final[FileStorage] = file_storage
        self._file_service: Final[FileService] = file_service

    async def compress(self, dto: CompressTextFileDTO) -> CompressedFileView:
        logger.info("Started file compression, file id: %s, compressor type: %s", dto.file_id, dto.compressor_type)

        file_info: FileStorageDTO | None = await self._file_storage.read_by_id(file_id=dto.file_id)

        if file_info is None:
            msg: str = f"Cant find the file with id: {dto.file_id}"
            raise FileForCompressionNotFoundError(msg)

        logger.info("File was found in storage, file id: %s", file_info.file_id)

        file: File = self._file_service.create(data=file_info.data, file_name=file_info.name)

        logger.info("Started creating of file compressor with type: %s", dto.compressor_type)
        compressor: Compressor = self._file_compressor_factory.create(compressor_type=dto.compressor_type)
        logger.info("Compressor was created: %s", compressor)

        compressed_file: CompressedFile = compressor.compress(file=file)

        return CompressedFileView(
            file_id=compressed_file.id,
            name=compressed_file.file_name.value,
            size=compressed_file.size.value,
            compression_type=compressed_file.compression_type,
            data=compressed_file.data,
        )

    async def decompress(self, dto: DecompressTextFileDTO) -> DecompressedFileView:
        logger.info("Started file decompression, file id %s, compressor type: %s", dto.file_id, dto.compressor_type)

        file_info: FileStorageDTO | None = await self._file_storage.read_by_id(file_id=dto.file_id)

        if file_info is None:
            msg: str = f"Cant find the file with id: {dto.file_id}"
            raise FileForCompressionNotFoundError(msg)

        logger.info("File was found in storage, file id: %s", file_info.file_id)

        file: CompressedFile = self._file_service.create_compressed_file(
            data=file_info.data, file_name=file_info.name, compression_type=CompressionType(dto.compressor_type.value)
        )

        logger.info("Started creating of file compressor with type: %s", dto.compressor_type)
        compressor: Compressor = self._file_compressor_factory.create(compressor_type=dto.compressor_type)
        logger.info("Compressor was created: %s", compressor)

        decompressed_file: File = compressor.decompress(file=file)

        return DecompressedFileView(
            file_id=decompressed_file.id,
            name=decompressed_file.file_name.value,
            size=decompressed_file.size.value,
            compression_type=CompressionType(dto.compressor_type.value),
            data=decompressed_file.data,
        )
