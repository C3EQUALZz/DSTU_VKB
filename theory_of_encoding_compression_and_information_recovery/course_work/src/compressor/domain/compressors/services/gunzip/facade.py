import gzip
import logging
from io import BytesIO
from pathlib import Path
from typing import Final

from typing_extensions import override

from compressor.domain.compressors.errors import CantDecompressThisFileError
from compressor.domain.compressors.services.base import Compressor
from compressor.domain.compressors.services.gunzip.configuration import GunZipConfiguration
from compressor.domain.files.entities.compressed_file import CompressedFile
from compressor.domain.files.entities.file import File
from compressor.domain.files.services.file_service import FileService
from compressor.domain.files.values.compression_type import CompressionType
from compressor.domain.files.values.file_name import FileName

logger: Final[logging.Logger] = logging.getLogger(__name__)


class GunZipCompressor(Compressor):
    def __init__(self, file_service: FileService) -> None:
        super().__init__()
        self._file_service: Final[FileService] = file_service
        self._gunzip_configuration: GunZipConfiguration = GunZipConfiguration()

    @override
    def compress(self, file: File) -> CompressedFile:
        source_path: FileName = file.file_name
        converted_source_path_to_path: Path = Path(source_path.value)

        dest_path: FileName = FileName(
            str(converted_source_path_to_path.with_suffix(converted_source_path_to_path.suffix + ".gz"))
        )

        data: BytesIO = BytesIO()

        with gzip.open(data, "wb") as f_out:
            while chunk := file.data.read(self._gunzip_configuration.CHUNK_SIZE):
                f_out.write(chunk)

        logger.debug("Compressed %s to %s", source_path, dest_path)
        data.seek(0)

        return self._file_service.create_compressed_file(
            file_name=FileName(str(dest_path)), compression_type=CompressionType.GZIP, data=data
        )

    @override
    def decompress(self, file: CompressedFile) -> File:
        converted_path: Path = Path(file.file_name.value)
        msg: str

        if not converted_path.suffix.endswith(CompressionType.GZIP):
            msg = f"Expected .gzip file, not '{converted_path.suffix}'"
            raise CantDecompressThisFileError(msg)

        dest_path: Path = converted_path.with_suffix("")
        data: BytesIO = BytesIO()

        with gzip.open(file.data, "rb") as f_in:
            while chunk := f_in.read(self._gunzip_configuration.CHUNK_SIZE):
                data.write(chunk)

        logger.debug("Decompressed %s to %s", converted_path, dest_path)
        data.seek(0)

        return self._file_service.create(
            file_name=FileName(str(dest_path)),
            data=data,
        )
