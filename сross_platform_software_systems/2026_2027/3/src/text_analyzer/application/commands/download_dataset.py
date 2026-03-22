import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from text_analyzer.application.ports.dataset_downloader import DatasetDownloader

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class DownloadDatasetCommand:
    url: str
    output_dir: Path


@final
class DownloadDatasetCommandHandler:
    def __init__(self, dataset_downloader: DatasetDownloader) -> None:
        self._dataset_downloader: Final[DatasetDownloader] = dataset_downloader

    def __call__(self, data: DownloadDatasetCommand) -> Path:
        logger.info("Downloading dataset from %s", data.url)
        result_path = self._dataset_downloader.download(data.url, data.output_dir)
        logger.info("Dataset extracted to %s", result_path)
        return result_path
