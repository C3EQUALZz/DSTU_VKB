import logging
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from text_analyzer.application.dto import TrainingConfig
from text_analyzer.application.ports.classifier import SentimentClassifier
from text_analyzer.application.ports.dataset_loader import DatasetLoader
from text_analyzer.application.ports.text_preprocessor import TextPreprocessor
from text_analyzer.application.ports.visualizer import TrainingVisualizer
from text_analyzer.domain.entities import Review
from text_analyzer.domain.value_objects import Sentiment

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class VisualizeCommand:
    data_dir: Path
    model_dir: Path
    output_dir: Path
    config: TrainingConfig


@final
class VisualizeCommandHandler:
    def __init__(
        self,
        dataset_loader: DatasetLoader,
        text_preprocessor: TextPreprocessor,
        classifier: SentimentClassifier,
        visualizer: TrainingVisualizer,
    ) -> None:
        self._dataset_loader: Final[DatasetLoader] = dataset_loader
        self._text_preprocessor: Final[TextPreprocessor] = text_preprocessor
        self._classifier: Final[SentimentClassifier] = classifier
        self._visualizer: Final[TrainingVisualizer] = visualizer

    def __call__(self, data: VisualizeCommand) -> list[Path]:
        saved_plots: list[Path] = []

        reviews = self._dataset_loader.load_reviews(data.data_dir)
        balanced = self._balance(reviews)

        p1 = self._visualizer.plot_dataset_distribution(reviews, balanced, data.output_dir)
        saved_plots.append(p1)

        p2 = self._visualizer.plot_review_lengths(reviews, data.output_dir)
        saved_plots.append(p2)

        random.seed(42)
        random.shuffle(balanced)
        split_idx = int(len(balanced) * (1 - data.config.test_ratio))
        train_reviews = balanced[:split_idx]
        val_reviews = balanced[split_idx:]

        train_texts = [str(r.text) for r in train_reviews]
        val_texts = [str(r.text) for r in val_reviews]

        logger.info("Building vocabulary and encoding for visualization...")
        self._text_preprocessor.fit(train_texts, data.config.max_vocab_size)
        train_encoded = self._text_preprocessor.encode(train_texts, data.config.max_seq_length)
        val_encoded = self._text_preprocessor.encode(val_texts, data.config.max_seq_length)

        train_labels = [r.sentiment.to_label() for r in train_reviews]
        val_labels = [r.sentiment.to_label() for r in val_reviews]

        logger.info("Training model for visualization (this may take a moment)...")
        result = self._classifier.fit(
            train_sequences=train_encoded,
            train_labels=train_labels,
            val_sequences=val_encoded,
            val_labels=val_labels,
            vocab_size=self._text_preprocessor.vocab_size,
            config=data.config,
        )

        p3 = self._visualizer.plot_training_curves(result, data.output_dir)
        saved_plots.append(p3)

        predicted = self._classifier.predict(val_encoded)
        p4 = self._visualizer.plot_confusion_matrix(val_labels, predicted, data.output_dir)
        saved_plots.append(p4)

        return saved_plots

    @staticmethod
    def _balance(reviews: list[Review]) -> list[Review]:
        positive = [r for r in reviews if r.sentiment == Sentiment.POSITIVE]
        negative = [r for r in reviews if r.sentiment == Sentiment.NEGATIVE]
        max_count = max(len(positive), len(negative))
        random.seed(42)
        if len(positive) < max_count:
            positive = (positive * math.ceil(max_count / len(positive)))[:max_count]
        if len(negative) < max_count:
            negative = (negative * math.ceil(max_count / len(negative)))[:max_count]
        return positive + negative
