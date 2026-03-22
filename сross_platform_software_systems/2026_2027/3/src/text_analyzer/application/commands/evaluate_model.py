import logging
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from text_analyzer.application.dto import EvaluationResult, TrainingConfig
from text_analyzer.application.ports.classifier import SentimentClassifier
from text_analyzer.application.ports.dataset_loader import DatasetLoader
from text_analyzer.application.ports.text_preprocessor import TextPreprocessor
from text_analyzer.domain.entities import Review
from text_analyzer.domain.value_objects import Sentiment

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class EvaluateModelCommand:
    data_dir: Path
    model_dir: Path
    config: TrainingConfig


@final
class EvaluateModelCommandHandler:
    def __init__(
        self,
        dataset_loader: DatasetLoader,
        text_preprocessor: TextPreprocessor,
        classifier: SentimentClassifier,
    ) -> None:
        self._dataset_loader: Final[DatasetLoader] = dataset_loader
        self._text_preprocessor: Final[TextPreprocessor] = text_preprocessor
        self._classifier: Final[SentimentClassifier] = classifier

    def __call__(self, data: EvaluateModelCommand) -> EvaluationResult:
        logger.info("Loading model from %s", data.model_dir)
        self._text_preprocessor.load(data.model_dir / "vocab.json")
        self._classifier.load_model(
            data.model_dir / "model.pt",
            vocab_size=self._text_preprocessor.vocab_size,
            config=data.config,
        )

        reviews = self._dataset_loader.load_reviews(data.data_dir)
        reviews = self._balance_and_split(reviews, data.config.test_ratio)

        texts = [str(r.text) for r in reviews]
        encoded = self._text_preprocessor.encode(texts, data.config.max_seq_length)
        labels = [r.sentiment.to_label() for r in reviews]

        result = self._classifier.evaluate(encoded, labels)
        logger.info(
            "Evaluation: accuracy=%.2f%%, loss=%.4f (%d/%d correct)",
            result.accuracy * 100,
            result.loss,
            result.correct_predictions,
            result.total_samples,
        )
        return result

    @staticmethod
    def _balance_and_split(reviews: list[Review], test_ratio: float) -> list[Review]:
        positive = [r for r in reviews if r.sentiment == Sentiment.POSITIVE]
        negative = [r for r in reviews if r.sentiment == Sentiment.NEGATIVE]

        max_count = max(len(positive), len(negative))
        random.seed(42)

        if len(positive) < max_count:
            ratio = math.ceil(max_count / len(positive))
            positive = (positive * ratio)[:max_count]
        if len(negative) < max_count:
            ratio = math.ceil(max_count / len(negative))
            negative = (negative * ratio)[:max_count]

        all_reviews = positive + negative
        random.shuffle(all_reviews)
        split_idx = int(len(all_reviews) * (1 - test_ratio))
        return all_reviews[split_idx:]
