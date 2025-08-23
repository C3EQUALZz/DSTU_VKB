from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from compressor.application.common.ports.file.file_query_gateway import FileQueryGateway
from compressor.application.common.views.files import CompressedFileView
from compressor.domain.compressors.factories.text.base import TextFileCompressorFactory, CompressorType
from compressor.domain.compressors.services.base import Compressor
from compressor.domain.files.entities.compressed_file import CompressedFile
from compressor.domain.files.entities.file import File


@dataclass(frozen=True, slots=True)
class CompressTextFileCommand:
    compressor_type: str
    path: Path


@final
class CompressTextFileCommandHandler:
    def __init__(
            self,
            file_compressor_factory: TextFileCompressorFactory,
            file_query_gateway: FileQueryGateway
    ) -> None:
        self._file_compressor_factory: Final[TextFileCompressorFactory] = file_compressor_factory
        self._file_query_gateway: Final[FileQueryGateway] = file_query_gateway

    async def __call__(self, data: CompressTextFileCommand) -> CompressedFileView:
        file: File = await self._file_query_gateway.read_by_path(path=data.path)
        compressor_type: CompressorType = CompressorType(data.compressor_type)
        compressor: Compressor = self._file_compressor_factory.create(compressor_type=compressor_type)
        compressed_file: CompressedFile = compressor.compress(file=file)

        return CompressedFileView(
            path=compressed_file.path,
            name=compressed_file.path.name,
            size=compressed_file.size.value,
            compression_type=compressed_file.compression_type,
        )
