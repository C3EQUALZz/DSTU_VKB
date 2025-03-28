from app.domain.entities.file_objects import CompressedFileObject, FileObject
from app.domain.values.backup import CompressionType
from app.infrastructure.compressors.base import Compressor
from app.infrastructure.services.compressor import CompressorService
from app.logic.commands.compression import CompressFileCommand, DecompressFileCommand
from app.logic.handlers.compression.base import CompressionCommandHandler


class CompressFileCommandHandler(CompressionCommandHandler[CompressFileCommand]):
    def __call__(self, command: CompressFileCommand) -> CompressedFileObject:
        compressor: Compressor = self._factory.create(command.compress_type)

        compressor_service: CompressorService = CompressorService(compressor)
        file_object = FileObject(command.src_file_path)
        return compressor_service.compress(file_object)


class DecompressFileCommandHandler(CompressionCommandHandler[DecompressFileCommand]):
    def __call__(self, command: DecompressFileCommand) -> FileObject:
        compressor: Compressor = self._factory.create(command.compress_type)
        compressor_service: CompressorService = CompressorService(compressor)

        file_object: CompressedFileObject = CompressedFileObject(
            command.src_file_path,
            CompressionType(command.compress_type),
        )

        return compressor_service.decompress(file_object)
