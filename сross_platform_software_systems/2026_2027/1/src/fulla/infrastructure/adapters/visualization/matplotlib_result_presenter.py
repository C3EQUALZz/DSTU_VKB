import logging
from collections.abc import Sequence
from typing import Final, final

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from tabulate import tabulate

from fulla.domain.shape_recognition.value_objects.activation_type import ActivationType
from fulla.domain.shape_recognition.value_objects.dataset import PreparedDataset
from fulla.domain.shape_recognition.value_objects.experiment_result import ExperimentResult

logger: Final[logging.Logger] = logging.getLogger(__name__)

CLASS_NAMES: Final[tuple[str, ...]] = ("Треугольник", "Круг", "Квадрат")
IMG_HEIGHT: Final[int] = 20
IMG_WIDTH: Final[int] = 20


@final
class MatplotlibResultPresenter:
    """Presents experiment results via console table and matplotlib charts."""

    def show_dataset_info(self, dataset: PreparedDataset) -> None:
        logger.info(
            "Dataset: %d train / %d test, input_size=%d",
            dataset.train_count,
            dataset.test_count,
            dataset.input_size,
        )

        fig, axes = plt.subplots(1, 6, figsize=(12, 2))
        fig.suptitle("Примеры изображений из датасета", fontsize=14)
        rng = np.random.RandomState(42)
        indices = rng.choice(dataset.train_count, 6, replace=False)

        for ax, idx in zip(axes, indices, strict=False):
            ax.imshow(
                dataset.x_train[idx].reshape(IMG_HEIGHT, IMG_WIDTH),
                cmap="gray",
            )
            ax.set_title(CLASS_NAMES[dataset.y_train[idx]], fontsize=10)
            ax.axis("off")

        plt.tight_layout()
        plt.savefig("samples.png", dpi=100, bbox_inches="tight")
        plt.close(fig)

    def show_results(self, results: Sequence[ExperimentResult]) -> None:
        self._print_table(results)
        self._plot_loss_curves(results)
        self._plot_accuracy_bars(results)
        self._print_best(results)

    # ── Private helpers ──────────────────────────────────────────────

    @staticmethod
    def _print_table(results: Sequence[ExperimentResult]) -> None:
        print("\n" + "=" * 70)  # noqa: T201
        print("  РЕЗУЛЬТАТЫ ЭКСПЕРИМЕНТОВ")  # noqa: T201
        print("=" * 70)  # noqa: T201

        table_data: list[list[str | int]] = [
            [
                r.hyper_parameters.hidden_neurons,
                r.hyper_parameters.activation.value,
                r.hyper_parameters.batch_size,
                f"{r.accuracy_percent:.2f}%",
            ]
            for r in results
        ]

        print(  # noqa: T201
            tabulate(
                table_data,
                headers=["Нейроны", "Активация", "Batch size", "Точность"],
                tablefmt="fancy_grid",
                stralign="center",
                numalign="center",
            ),
        )

    @staticmethod
    def _plot_loss_curves(results: Sequence[ExperimentResult]) -> None:
        neurons_set: list[int] = sorted({r.hyper_parameters.hidden_neurons for r in results})
        activations_set: list[ActivationType] = sorted(
            {r.hyper_parameters.activation for r in results},
            key=lambda a: a.value,
        )

        fig, axes = plt.subplots(
            len(neurons_set),
            len(activations_set),
            figsize=(14, 4 * len(neurons_set)),
            squeeze=False,
        )
        fig.suptitle("Кривые обучения (Loss) для разных конфигураций", fontsize=16, y=1.02)

        for i, neurons in enumerate(neurons_set):
            for j, activation in enumerate(activations_set):
                ax = axes[i][j]
                matching = [
                    r
                    for r in results
                    if r.hyper_parameters.hidden_neurons == neurons and r.hyper_parameters.activation == activation
                ]
                for r in matching:
                    ax.plot(
                        r.loss_history,
                        label=f"bs={r.hyper_parameters.batch_size} ({r.accuracy_percent:.1f}%)",
                    )
                ax.set_title(f"Нейронов: {neurons}, Активация: {activation.value}")
                ax.set_xlabel("Эпоха")
                ax.set_ylabel("Loss")
                ax.legend(fontsize=8)
                ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig("loss_curves.png", dpi=120, bbox_inches="tight")
        plt.close(fig)

    @staticmethod
    def _plot_accuracy_bars(results: Sequence[ExperimentResult]) -> None:
        fig, ax = plt.subplots(figsize=(16, 6))

        labels: list[str] = [
            f"n={r.hyper_parameters.hidden_neurons}\n"
            f"{r.hyper_parameters.activation.value}\n"
            f"bs={r.hyper_parameters.batch_size}"
            for r in results
        ]
        accuracies: list[float] = [r.accuracy_percent for r in results]
        colors: list[str] = [
            "#4CAF50" if r.hyper_parameters.activation == ActivationType.RELU else "#FF9800" for r in results
        ]

        bars = ax.bar(range(len(accuracies)), accuracies, color=colors, edgecolor="black", linewidth=0.5)

        for bar, acc in zip(bars, accuracies, strict=False):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5,
                f"{acc:.1f}%",
                ha="center",
                va="bottom",
                fontsize=7,
                fontweight="bold",
            )

        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, fontsize=7, ha="center")
        ax.set_ylabel("Точность (%)")
        ax.set_title("Сравнение точности моделей для разных гиперпараметров", fontsize=14)
        ax.set_ylim(0, 105)
        ax.grid(axis="y", alpha=0.3)

        legend_elements = [
            Patch(facecolor="#4CAF50", edgecolor="black", label="ReLU"),
            Patch(facecolor="#FF9800", edgecolor="black", label="Linear"),
        ]
        ax.legend(handles=legend_elements, loc="lower right", fontsize=10)

        plt.tight_layout()
        plt.savefig("accuracy_comparison.png", dpi=120, bbox_inches="tight")
        plt.close(fig)

    @staticmethod
    def _print_best(results: Sequence[ExperimentResult]) -> None:
        best: ExperimentResult = max(results, key=lambda r: r.accuracy)
        print("\n🏆  Лучшая конфигурация:")  # noqa: T201
        print(f"    Нейроны:    {best.hyper_parameters.hidden_neurons}")  # noqa: T201
        print(f"    Активация:  {best.hyper_parameters.activation.value}")  # noqa: T201
        print(f"    Batch size: {best.hyper_parameters.batch_size}")  # noqa: T201
        print(f"    Точность:   {best.accuracy_percent:.2f}%")  # noqa: T201

