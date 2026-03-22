from collections.abc import Sequence
from pathlib import Path
from typing import Protocol

from text_analyzer.application.dto import EvaluationResult, TrainingConfig, TrainingResult


class SentimentClassifier(Protocol):
    def fit(
        self,
        train_sequences: Sequence[Sequence[int]],
        train_labels: Sequence[int],
        val_sequences: Sequence[Sequence[int]],
        val_labels: Sequence[int],
        vocab_size: int,
        config: TrainingConfig,
    ) -> TrainingResult:
        """Train the model on provided data."""
        ...

    def evaluate(
        self,
        sequences: Sequence[Sequence[int]],
        labels: Sequence[int],
    ) -> EvaluationResult:
        """Evaluate the model on test data."""
        ...

    def predict(self, sequences: Sequence[Sequence[int]]) -> list[int]:
        """Return predicted labels (0 or 1) for given sequences."""
        ...

    def save_model(self, path: Path) -> None:
        """Save trained model to file."""
        ...

    def load_model(self, path: Path, vocab_size: int, config: TrainingConfig) -> None:
        """Load trained model from file."""
        ...
