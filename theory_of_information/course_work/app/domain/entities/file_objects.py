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
class FileObjectEntity(BaseEntity):
    """
    Entity that describes a file object.
    This entity has only one field: file_path.
    """
    file_path: Path


@dataclass(eq=False)
class CompressedFileObjectEntity(BaseEntity):
    """
    Entity that describes file which was compressed.
    There are several fields:
    - file_path: path to file.
    - compression_type: type of compressed file.
    """
    file_path: Path
    compression_type: CompressionType


@dataclass(eq=False)
class FileStatistic(BaseEntity):
    """
    Entity that describes file statistics.
    There are several fields:
    - name: Name of file.
    - size: Size of file.
    - type_of_file: Type of file. It can be only directory or usual file.
    - extension: Extension of file. If it is directory or usual file.
    - permissions: Permissions of file.
    """
    name: str
    size: SizeOfFile
    type_of_file: TypeOfFile
    extension: str
    permissions: PermissionsOfFile
