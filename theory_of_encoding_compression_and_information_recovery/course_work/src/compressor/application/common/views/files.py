from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True, kw_only=True)
class CompressedFileView:
    path: Path
    file_id: str
    name: str
    size: float
    compression_type: str
