from pathlib import Path
from typing import Protocol


class DatasetDownloader(Protocol):
    def download(self, url: str, output_dir: Path) -> Path:
        """Download and extract dataset archive. Returns path to extracted directory."""
        ...
