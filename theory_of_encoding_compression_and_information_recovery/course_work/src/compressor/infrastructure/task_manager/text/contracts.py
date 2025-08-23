from dataclasses import dataclass
from pathlib import Path

from compressor.domain.compressors.factories.text.base import CompressorType
from compressor.domain.users.values.user_id import UserID


@dataclass(frozen=True, slots=True, kw_only=True)
class FileInfoDTO:
    file_path: Path
    compressor_type: CompressorType
    user_id: UserID
