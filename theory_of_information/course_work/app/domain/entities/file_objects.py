from dataclasses import dataclass
from pathlib import Path

from app.domain.entities.base import BaseEntity
from app.domain.values.backup import CompressionType
from app.domain.values.file_objects import (
    PermissionsOfFile,
    SizeOfFile,
    TypeOfFile,
)


@dataclass(eq=False)
class FileObject(BaseEntity):
    file_path: Path


@dataclass(eq=False)
class CompressedFileObject(BaseEntity):
    file_path: Path
    compression_type: CompressionType


@dataclass(eq=False)
class FileStatistic(BaseEntity):
    name: str
    size: SizeOfFile
    type_of_file: TypeOfFile
    extension: str
    permissions: PermissionsOfFile
