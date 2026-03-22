from pathlib import Path
from typing import Protocol

from text_analyzer.application.dto import TrainingResult
from text_analyzer.domain.entities import Review


class TrainingVisualizer(Protocol):
    def plot_training_curves(
        self,
        result: TrainingResult,
        output_dir: Path,
    ) -> Path:
        """Plot loss and accuracy curves. Returns path to saved figure."""
        ...

    def plot_dataset_distribution(
        self,
        reviews: list[Review],
        balanced_reviews: list[Review],
        output_dir: Path,
    ) -> Path:
        """Plot class distribution before and after balancing. Returns path to saved figure."""
        ...

    def plot_confusion_matrix(
        self,
        true_labels: list[int],
        predicted_labels: list[int],
        output_dir: Path,
    ) -> Path:
        """Plot confusion matrix. Returns path to saved figure."""
        ...

    def plot_review_lengths(
        self,
        reviews: list[Review],
        output_dir: Path,
    ) -> Path:
        """Plot histogram of review lengths. Returns path to saved figure."""
        ...
