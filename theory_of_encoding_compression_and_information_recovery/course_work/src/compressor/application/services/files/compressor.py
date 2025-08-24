from typing import Final

from compressor.application.common.ports.storage import FileStorage, FileStorageDTO
from compressor.application.common.views.files import CompressedFileView
from compressor.application.services.files.contracts import CompressTextFileDTO
from compressor.domain.compressors.factories.text.base import FileCompressorFactory
from compressor.domain.compressors.services.base import Compressor
from compressor.domain.files.entities.compressed_file import CompressedFile
from compressor.domain.files.entities.file import File
from compressor.domain.files.services.file_service import FileService


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
        file_info: FileStorageDTO | None = await self._file_storage.read_by_id(file_id=dto.file_id)

        if file_info is None:
            raise ...

        file: File = self._file_service.create(
            data=file_info.data,
            path=file_info.path
        )

        compressor: Compressor = self._file_compressor_factory.create(compressor_type=dto.compressor_type)
        compressed_file: CompressedFile = compressor.compress(file=file)

        return CompressedFileView(
            file_id=compressed_file.id,
            path=compressed_file.path,
            name=compressed_file.path.name,
            size=compressed_file.size.value,
            compression_type=compressed_file.compression_type,
        )
