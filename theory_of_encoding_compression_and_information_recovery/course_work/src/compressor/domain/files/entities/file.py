from dataclasses import dataclass
from pathlib import Path

from compressor.domain.common.entities.base_entity import BaseEntity
from compressor.domain.files.values.file_id import FileID
from compressor.domain.files.values.file_size import FileSize


@dataclass(eq=False, kw_only=True)
class File(BaseEntity[FileID]):
    path: Path
    size: FileSize
    is_dir: bool