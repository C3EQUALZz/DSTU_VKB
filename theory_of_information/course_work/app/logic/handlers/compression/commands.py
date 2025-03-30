from typing import TYPE_CHECKING

from app.domain.entities.file_objects import (
    CompressedFileObjectEntity,
    FileObjectEntity,
)
from app.domain.values.backup import CompressionType
from app.infrastructure.services.compressor import CompressorService
from app.logic.commands.compression import (
    CompressFileCommand,
    DecompressFileCommand,
)
from app.logic.handlers.compression.base import CompressionCommandHandler

if TYPE_CHECKING:
    from app.infrastructure.compressors.base import Compressor


class CompressFileCommandHandler(CompressionCommandHandler[CompressFileCommand]):
    def __call__(self, command: CompressFileCommand) -> CompressedFileObjectEntity:
        compressor: Compressor = self._factory.create(command.compress_type)

        compressor_service: CompressorService = CompressorService(compressor)
        file_object = FileObjectEntity(command.src_file_path)
        return compressor_service.compress(file_object)


class DecompressFileCommandHandler(CompressionCommandHandler[DecompressFileCommand]):
    def __call__(self, command: DecompressFileCommand) -> FileObjectEntity:
        compressor: Compressor = self._factory.create(command.compress_type)
        compressor_service: CompressorService = CompressorService(compressor)

        file_object: CompressedFileObjectEntity = CompressedFileObjectEntity(
            command.src_file_path,
            CompressionType(command.compress_type),
        )

        return compressor_service.decompress(file_object)
