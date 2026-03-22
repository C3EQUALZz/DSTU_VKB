import logging
from pathlib import Path
from typing import Final, final

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from text_analyzer.application.dto import TrainingResult
from text_analyzer.domain.entities import Review
from text_analyzer.domain.value_objects import Sentiment

matplotlib.use("Agg")

logger: Final[logging.Logger] = logging.getLogger(__name__)


@final
class MatplotlibVisualizer:
    def plot_training_curves(self, result: TrainingResult, output_dir: Path) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        epochs = range(1, len(result.train_losses) + 1)

        ax1.plot(epochs, result.train_losses, "b-o", label="Train Loss", markersize=3)
        ax1.plot(epochs, result.val_losses, "r-o", label="Validation Loss", markersize=3)
        ax1.axvline(x=result.best_epoch, color="g", linestyle="--", alpha=0.7, label=f"Best epoch ({result.best_epoch})")
        ax1.set_xlabel("Epoch")
        ax1.set_ylabel("Loss (BCEWithLogitsLoss)")
        ax1.set_title("Training and Validation Loss")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        ax2.plot(epochs, [a * 100 for a in result.val_accuracies], "g-o", label="Validation Accuracy", markersize=3)
        ax2.axhline(y=result.best_val_accuracy * 100, color="r", linestyle="--", alpha=0.7,
                     label=f"Best: {result.best_val_accuracy * 100:.2f}%")
        ax2.axhline(y=85, color="orange", linestyle=":", alpha=0.5, label="Target: 85%")
        ax2.axhline(y=90, color="orange", linestyle=":", alpha=0.5, label="Target: 90%")
        ax2.fill_between(epochs, 85, 90, alpha=0.1, color="orange", label="Target range")
        ax2.set_xlabel("Epoch")
        ax2.set_ylabel("Accuracy (%)")
        ax2.set_title("Validation Accuracy")
        ax2.legend(loc="lower right")
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        path = output_dir / "training_curves.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        logger.info("Training curves saved to %s", path)
        return path

    def plot_dataset_distribution(
        self,
        reviews: list[Review],
        balanced_reviews: list[Review],
        output_dir: Path,
    ) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)

        orig_pos = sum(1 for r in reviews if r.sentiment == Sentiment.POSITIVE)
        orig_neg = len(reviews) - orig_pos
        bal_pos = sum(1 for r in balanced_reviews if r.sentiment == Sentiment.POSITIVE)
        bal_neg = len(balanced_reviews) - bal_pos

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        colors = ["#2ecc71", "#e74c3c"]
        labels = ["Positive", "Negative"]

        bars1 = ax1.bar(labels, [orig_pos, orig_neg], color=colors, edgecolor="black", linewidth=0.5)
        ax1.set_title(f"Original Dataset ({len(reviews)} reviews)")
        ax1.set_ylabel("Number of Reviews")
        for bar, val in zip(bars1, [orig_pos, orig_neg]):
            ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 20,
                     str(val), ha="center", va="bottom", fontweight="bold")
        ax1.grid(True, alpha=0.3, axis="y")

        bars2 = ax2.bar(labels, [bal_pos, bal_neg], color=colors, edgecolor="black", linewidth=0.5)
        ax2.set_title(f"Balanced Dataset ({len(balanced_reviews)} reviews)")
        ax2.set_ylabel("Number of Reviews")
        for bar, val in zip(bars2, [bal_pos, bal_neg]):
            ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 20,
                     str(val), ha="center", va="bottom", fontweight="bold")
        ax2.grid(True, alpha=0.3, axis="y")

        plt.tight_layout()
        path = output_dir / "dataset_distribution.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        logger.info("Dataset distribution saved to %s", path)
        return path

    def plot_confusion_matrix(
        self,
        true_labels: list[int],
        predicted_labels: list[int],
        output_dir: Path,
    ) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)

        tp = sum(1 for t, p in zip(true_labels, predicted_labels) if t == 1 and p == 1)
        tn = sum(1 for t, p in zip(true_labels, predicted_labels) if t == 0 and p == 0)
        fp = sum(1 for t, p in zip(true_labels, predicted_labels) if t == 0 and p == 1)
        fn = sum(1 for t, p in zip(true_labels, predicted_labels) if t == 1 and p == 0)

        cm = np.array([[tn, fp], [fn, tp]])
        total = len(true_labels)
        accuracy = (tp + tn) / total

        fig, ax = plt.subplots(figsize=(7, 6))
        im = ax.imshow(cm, interpolation="nearest", cmap="Blues")
        ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

        class_names = ["Negative", "Positive"]
        ax.set(
            xticks=[0, 1], yticks=[0, 1],
            xticklabels=class_names, yticklabels=class_names,
            xlabel="Predicted Label", ylabel="True Label",
            title=f"Confusion Matrix (Accuracy: {accuracy * 100:.2f}%)",
        )

        thresh = cm.max() / 2.0
        for i in range(2):
            for j in range(2):
                color = "white" if cm[i, j] > thresh else "black"
                pct = cm[i, j] / total * 100
                ax.text(j, i, f"{cm[i, j]}\n({pct:.1f}%)",
                        ha="center", va="center", color=color, fontsize=14)

        plt.tight_layout()
        path = output_dir / "confusion_matrix.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        logger.info("Confusion matrix saved to %s", path)
        return path

    def plot_review_lengths(self, reviews: list[Review], output_dir: Path) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)

        pos_lengths = [len(str(r.text).split()) for r in reviews if r.sentiment == Sentiment.POSITIVE]
        neg_lengths = [len(str(r.text).split()) for r in reviews if r.sentiment == Sentiment.NEGATIVE]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        ax1.hist(pos_lengths, bins=40, color="#2ecc71", alpha=0.7, edgecolor="black", linewidth=0.5, label="Positive")
        ax1.hist(neg_lengths, bins=40, color="#e74c3c", alpha=0.7, edgecolor="black", linewidth=0.5, label="Negative")
        ax1.set_xlabel("Number of Words")
        ax1.set_ylabel("Number of Reviews")
        ax1.set_title("Distribution of Review Lengths")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        all_lengths = pos_lengths + neg_lengths
        stats = {
            "": ["Positive", "Negative", "All"],
            "Count": [len(pos_lengths), len(neg_lengths), len(all_lengths)],
            "Mean": [f"{np.mean(pos_lengths):.1f}", f"{np.mean(neg_lengths):.1f}", f"{np.mean(all_lengths):.1f}"],
            "Median": [f"{np.median(pos_lengths):.0f}", f"{np.median(neg_lengths):.0f}", f"{np.median(all_lengths):.0f}"],
            "Max": [max(pos_lengths), max(neg_lengths), max(all_lengths)],
        }

        ax2.axis("off")
        table = ax2.table(
            cellText=list(zip(*[stats[k] for k in stats])),
            colLabels=list(stats.keys()),
            loc="center",
            cellLoc="center",
        )
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1.2, 1.8)
        ax2.set_title("Review Length Statistics", pad=20)

        plt.tight_layout()
        path = output_dir / "review_lengths.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        logger.info("Review lengths plot saved to %s", path)
        return path
