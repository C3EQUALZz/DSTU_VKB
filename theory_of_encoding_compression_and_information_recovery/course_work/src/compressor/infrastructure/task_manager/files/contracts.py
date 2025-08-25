from dataclasses import dataclass

from compressor.domain.compressors.factories.text.base import CompressorType
from compressor.domain.files.values.file_id import FileID
from compressor.domain.files.values.file_name import FileName
from compressor.domain.users.values.user_id import UserID


@dataclass(frozen=True, slots=True, kw_only=True)
class FileInfoDTO:
    file_name: FileName
    file_id: FileID
    compressor_type: CompressorType
    user_id: UserID
