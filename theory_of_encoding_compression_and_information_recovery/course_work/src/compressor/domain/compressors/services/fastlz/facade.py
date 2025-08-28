import logging
from io import BytesIO
from pathlib import Path
from typing import Final

from typing_extensions import override

from compressor.domain.compressors.errors import CantDecompressThisFileError
from compressor.domain.compressors.services.base import Compressor
from compressor.domain.compressors.services.fastlz.interface import FastLzInterface
from compressor.domain.files.entities.compressed_file import CompressedFile
from compressor.domain.files.entities.file import File
from compressor.domain.files.services.file_service import FileService
from compressor.domain.files.values.compression_type import CompressionType
from compressor.domain.files.values.file_name import FileName

logger: Final[logging.Logger] = logging.getLogger(__name__)


class FastLZCompressor(Compressor):
    def __init__(self, file_service: FileService) -> None:
        super().__init__()
        self._compressor: Final[FastLzInterface] = FastLzInterface()
        self._file_service: Final[FileService] = file_service

    @override
    def compress(self, file: File) -> CompressedFile:
        source_path: FileName = file.file_name

        converted_source_path_to_path: Path = Path(source_path.value)

        dest_path: FileName = FileName(
            str(converted_source_path_to_path.with_suffix(converted_source_path_to_path.suffix + ".fastlz"))
        )
        data: BytesIO = BytesIO()

        data_for_compression: bytearray = bytearray(file.data.read())
        data.write(bytes(self._compressor.compress(data_for_compression, level=2)))

        logger.info(
            "Compressed %s to %s",
            source_path,
            dest_path,
        )

        return self._file_service.create_compressed_file(
            file_name=dest_path, compression_type=CompressionType.FASTLZ, data=data
        )

    @override
    def decompress(self, file: CompressedFile) -> File:
        converted_path: Path = Path(file.file_name.value)
        msg: str

        if not converted_path.suffix.endswith(CompressionType.FASTLZ):
            msg = f"Expected .fastlz file, not {converted_path.suffix}"
            raise CantDecompressThisFileError(msg)

        dest_path: Path = converted_path.with_suffix("")
        data: BytesIO = BytesIO()

        data_for_decompression: bytearray = bytearray(file.data.read())
        data.write(bytes(self._compressor.decompress(data_for_decompression)))

        logger.debug("Decompressed %s to %s", converted_path, dest_path)
        data.seek(0)

        return self._file_service.create(
            file_name=FileName(str(dest_path)),
            data=data,
        )
