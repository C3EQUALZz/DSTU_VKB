import logging
from pathlib import Path
from typing import Final, final

from text_analyzer.domain.entities import Review
from text_analyzer.domain.errors import EmptyReviewTextError
from text_analyzer.domain.value_objects import Sentiment

logger: Final[logging.Logger] = logging.getLogger(__name__)

_POSITIVE_KEYWORDS: Final[tuple[str, ...]] = ("позитивн", "positive", "pos")
_NEGATIVE_KEYWORDS: Final[tuple[str, ...]] = ("негативн", "negative", "neg")


@final
class FileDatasetLoader:
    def load_reviews(self, data_dir: Path) -> list[Review]:
        reviews: list[Review] = []

        for txt_file in sorted(data_dir.glob("*.txt")):
            sentiment = self._detect_sentiment(txt_file.name)
            if sentiment is None:
                logger.warning("Cannot detect sentiment for file: %s, skipping", txt_file.name)
                continue

            file_reviews = self._load_file(txt_file, sentiment)
            logger.info("Loaded %d reviews from %s (%s)", len(file_reviews), txt_file.name, sentiment.value)
            reviews.extend(file_reviews)

        if not reviews:
            msg = f"No reviews found in {data_dir}"
            raise FileNotFoundError(msg)

        return reviews

    @staticmethod
    def _detect_sentiment(filename: str) -> Sentiment | None:
        lower = filename.lower()
        if any(kw in lower for kw in _POSITIVE_KEYWORDS):
            return Sentiment.POSITIVE
        if any(kw in lower for kw in _NEGATIVE_KEYWORDS):
            return Sentiment.NEGATIVE
        return None

    @staticmethod
    def _load_file(path: Path, sentiment: Sentiment) -> list[Review]:
        reviews: list[Review] = []
        text = path.read_text(encoding="utf-8")

        for line in text.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            try:
                reviews.append(Review.create(stripped, sentiment))
            except EmptyReviewTextError:
                continue

        return reviews
