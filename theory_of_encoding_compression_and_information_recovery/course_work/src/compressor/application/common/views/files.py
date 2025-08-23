from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True, kw_only=True)
class CompressedFileView:
    path: Path
    name: str
    size: float
    compression_type: str
