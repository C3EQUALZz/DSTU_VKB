import logging
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from text_analyzer.application.dto import TrainingConfig, TrainingResult
from text_analyzer.application.ports.classifier import SentimentClassifier
from text_analyzer.application.ports.dataset_loader import DatasetLoader
from text_analyzer.application.ports.text_preprocessor import TextPreprocessor
from text_analyzer.domain.entities import Review
from text_analyzer.domain.value_objects import Sentiment

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class TrainModelCommand:
    data_dir: Path
    model_output_dir: Path
    config: TrainingConfig


@final
class TrainModelCommandHandler:
    def __init__(
        self,
        dataset_loader: DatasetLoader,
        text_preprocessor: TextPreprocessor,
        classifier: SentimentClassifier,
    ) -> None:
        self._dataset_loader: Final[DatasetLoader] = dataset_loader
        self._text_preprocessor: Final[TextPreprocessor] = text_preprocessor
        self._classifier: Final[SentimentClassifier] = classifier

    def __call__(self, data: TrainModelCommand) -> TrainingResult:
        logger.info("Loading reviews from %s", data.data_dir)
        reviews = self._dataset_loader.load_reviews(data.data_dir)
        logger.info("Loaded %d reviews", len(reviews))

        reviews = self._balance_classes(reviews)
        logger.info("After balancing: %d reviews", len(reviews))

        random.shuffle(reviews)
        split_idx = int(len(reviews) * (1 - data.config.test_ratio))
        train_reviews = reviews[:split_idx]
        val_reviews = reviews[split_idx:]

        pos_train = sum(1 for r in train_reviews if r.sentiment == Sentiment.POSITIVE)
        neg_train = len(train_reviews) - pos_train
        logger.info(
            "Train: %d (pos=%d, neg=%d), Val: %d",
            len(train_reviews), pos_train, neg_train, len(val_reviews),
        )

        train_texts = [str(r.text) for r in train_reviews]
        val_texts = [str(r.text) for r in val_reviews]

        logger.info("Building vocabulary (max_size=%d)", data.config.max_vocab_size)
        self._text_preprocessor.fit(train_texts, data.config.max_vocab_size)

        train_encoded = self._text_preprocessor.encode(train_texts, data.config.max_seq_length)
        val_encoded = self._text_preprocessor.encode(val_texts, data.config.max_seq_length)

        train_labels = [r.sentiment.to_label() for r in train_reviews]
        val_labels = [r.sentiment.to_label() for r in val_reviews]

        logger.info("Starting training for %d epochs", data.config.epochs)
        result = self._classifier.fit(
            train_sequences=train_encoded,
            train_labels=train_labels,
            val_sequences=val_encoded,
            val_labels=val_labels,
            vocab_size=self._text_preprocessor.vocab_size,
            config=data.config,
        )

        data.model_output_dir.mkdir(parents=True, exist_ok=True)
        self._classifier.save_model(data.model_output_dir / "model.pt")
        self._text_preprocessor.save(data.model_output_dir / "vocab.json")
        logger.info(
            "Training complete. Best val accuracy: %.2f%% (epoch %d)",
            result.best_val_accuracy * 100,
            result.best_epoch,
        )
        return result

    @staticmethod
    def _balance_classes(reviews: list[Review]) -> list[Review]:
        positive = [r for r in reviews if r.sentiment == Sentiment.POSITIVE]
        negative = [r for r in reviews if r.sentiment == Sentiment.NEGATIVE]

        logger.info("Before balancing: pos=%d, neg=%d", len(positive), len(negative))

        max_count = max(len(positive), len(negative))
        random.seed(42)

        if len(positive) < max_count:
            ratio = math.ceil(max_count / len(positive))
            positive = (positive * ratio)[:max_count]
        if len(negative) < max_count:
            ratio = math.ceil(max_count / len(negative))
            negative = (negative * ratio)[:max_count]

        return positive + negative
