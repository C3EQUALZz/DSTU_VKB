import logging
import zipfile
from pathlib import Path
from typing import Final, final

import httpx

logger: Final[logging.Logger] = logging.getLogger(__name__)


@final
class HttpDatasetDownloader:
    def download(self, url: str, output_dir: Path) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)
        zip_path = output_dir / "dataset.zip"

        if self._already_extracted(output_dir):
            logger.info("Dataset already exists at %s, skipping download", output_dir)
            return output_dir

        logger.info("Downloading %s", url)
        with httpx.stream("GET", url, follow_redirects=True, timeout=120.0) as response:
            response.raise_for_status()
            with zip_path.open("wb") as f:
                for chunk in response.iter_bytes(chunk_size=8192):
                    f.write(chunk)

        logger.info("Extracting archive to %s", output_dir)
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(output_dir)

        zip_path.unlink()
        logger.info("Download and extraction complete")
        return output_dir

    @staticmethod
    def _already_extracted(output_dir: Path) -> bool:
        txt_files = list(output_dir.glob("*.txt"))
        return len(txt_files) >= 2
