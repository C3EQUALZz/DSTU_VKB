from pathlib import Path
from typing import Protocol

from text_analyzer.domain.entities import Review


class DatasetLoader(Protocol):
    def load_reviews(self, data_dir: Path) -> list[Review]:
        """Load all reviews from the dataset directory."""
        ...
