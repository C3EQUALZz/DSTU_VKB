import logging
import tempfile
from io import BytesIO
from pathlib import Path
from typing import Final

from typing_extensions import override

from compressor.domain.compressors.services.base import Compressor
from compressor.domain.compressors.services.gunzip.facade import GunZipCompressor
from compressor.domain.compressors.services.pigz.configuration import Configuration
from compressor.domain.compressors.services.pigz.pigz_file import PigzFile
from compressor.domain.files.entities.compressed_file import CompressedFile
from compressor.domain.files.entities.file import File
from compressor.domain.files.services.file_service import FileService
from compressor.domain.files.values.compression_type import CompressionType
from compressor.domain.files.values.file_name import FileName

logger: Final[logging.Logger] = logging.getLogger(__name__)


class PigzCompressor(Compressor):
    def __init__(self, file_service: FileService, gzip_compressor: GunZipCompressor) -> None:
        super().__init__()
        self._file_service: Final[FileService] = file_service
        self._gzip_compressor: Final[GunZipCompressor] = gzip_compressor
        self._pigz_configuration: Final[Configuration] = Configuration()

    @override
    def compress(self, file: File) -> CompressedFile:
        data: BytesIO
        converted_source_path_to_path: Path = Path(file.file_name.value)

        dest_path: FileName = FileName(
            str(converted_source_path_to_path.with_suffix(converted_source_path_to_path.suffix + ".gzip"))
        )

        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            file.data.seek(0)
            temp_file.write(file.data.read())
            temp_file.flush()

            pigz_file = PigzFile(Path(temp_file.name), configuration=self._pigz_configuration)
            pigz_file.process_compression_target()

            logger.debug("Compressed to %s", temp_file.name)

            temp_file.seek(0)
            data = BytesIO(temp_file.read())

            data.seek(0)

            return self._file_service.create_compressed_file(
                file_name=dest_path, compression_type=CompressionType.GZIP, data=data
            )

    @override
    def decompress(self, file: CompressedFile) -> File:
        return self._gzip_compressor.decompress(file=file)
