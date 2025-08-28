from dataclasses import dataclass
from io import BytesIO


@dataclass(frozen=True, slots=True, kw_only=True)
class CompressedFileView:
    data: BytesIO
    file_id: str
    name: str
    size: float
    compression_type: str


@dataclass(frozen=True, slots=True, kw_only=True)
class DecompressedFileView:
    data: BytesIO
    file_id: str
    name: str
    size: float
    compression_type: str
