import logging
from collections.abc import Sequence
from typing import Final, final

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from tabulate import tabulate

from fulla.domain.price_prediction.value_objects.regression_activation_type import RegressionActivationType
from fulla.domain.price_prediction.value_objects.regression_dataset import RegressionDataset
from fulla.domain.price_prediction.value_objects.regression_result import RegressionResult

logger: Final[logging.Logger] = logging.getLogger(__name__)


@final
class MatplotlibRegressionResultPresenter:
    """Presents regression experiment results via console table and matplotlib charts."""

    def show_dataset_info(self, dataset: RegressionDataset) -> None:
        logger.info(
            "Dataset: %d train / %d test, features=%d (%s)",
            dataset.train_count,
            dataset.test_count,
            dataset.input_size,
            ", ".join(dataset.feature_names),
        )

        # Plot feature distributions
        fig, axes = plt.subplots(2, 4, figsize=(16, 6))
        fig.suptitle("Распределение признаков (California Housing)", fontsize=14)
        for i, (ax, name) in enumerate(zip(axes.flat, dataset.feature_names, strict=False)):
            ax.hist(dataset.x_train[:, i], bins=40, alpha=0.7, color="steelblue", edgecolor="black", linewidth=0.3)
            ax.set_title(name, fontsize=10)
            ax.tick_params(labelsize=7)
        plt.tight_layout()
        plt.savefig("regression_features.png", dpi=100, bbox_inches="tight")
        plt.close(fig)

        # Plot target distribution
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.hist(dataset.y_train, bins=50, alpha=0.7, color="coral", edgecolor="black", linewidth=0.3)
        ax.set_title("Распределение целевой переменной (MedHouseVal)", fontsize=13)
        ax.set_xlabel("Median House Value ($100k)")
        ax.set_ylabel("Число образцов")
        plt.tight_layout()
        plt.savefig("regression_target_distribution.png", dpi=100, bbox_inches="tight")
        plt.close(fig)

    def show_results(self, results: Sequence[RegressionResult]) -> None:
        self._print_table(results)
        self._plot_loss_curves(results)
        self._plot_mse_bars(results)
        self._print_best(results)

    # ── Private helpers ──────────────────────────────────────────────

    @staticmethod
    def _print_table(results: Sequence[RegressionResult]) -> None:
        print("\n" + "=" * 90)  # noqa: T201
        print("  РЕЗУЛЬТАТЫ ЭКСПЕРИМЕНТОВ (РЕГРЕССИЯ)")  # noqa: T201
        print("=" * 90)  # noqa: T201

        table_data: list[list[str | int | float]] = [
            [
                r.hyper_parameters.hidden_neurons,
                r.hyper_parameters.num_hidden_layers,
                r.hyper_parameters.activation.value,
                r.hyper_parameters.batch_size,
                r.hyper_parameters.learning_rate,
                f"{r.mse:.4f}",
                f"{r.mae:.4f}",
                f"{r.r2_score:.4f}",
            ]
            for r in results
        ]

        print(  # noqa: T201
            tabulate(
                table_data,
                headers=[
                    "Нейроны", "Слои", "Активация", "Batch", "LR",
                    "MSE", "MAE", "R²",
                ],
                tablefmt="fancy_grid",
                stralign="center",
                numalign="center",
            ),
        )

    @staticmethod
    def _plot_loss_curves(results: Sequence[RegressionResult]) -> None:
        activations_set: list[RegressionActivationType] = sorted(
            {r.hyper_parameters.activation for r in results},
            key=lambda a: a.value,
        )
        layers_set: list[int] = sorted({r.hyper_parameters.num_hidden_layers for r in results})

        fig, axes = plt.subplots(
            len(layers_set),
            len(activations_set),
            figsize=(7 * len(activations_set), 4 * len(layers_set)),
            squeeze=False,
        )
        fig.suptitle("Кривые обучения (MSE Loss) для разных конфигураций", fontsize=16, y=1.02)

        for i, num_layers in enumerate(layers_set):
            for j, activation in enumerate(activations_set):
                ax = axes[i][j]
                matching = [
                    r for r in results
                    if r.hyper_parameters.num_hidden_layers == num_layers
                    and r.hyper_parameters.activation == activation
                ]
                for r in matching:
                    label = (
                        f"n={r.hyper_parameters.hidden_neurons}, "
                        f"bs={r.hyper_parameters.batch_size} "
                        f"(MSE={r.mse:.3f})"
                    )
                    ax.plot(r.loss_history, label=label)

                ax.set_title(f"Слоёв: {num_layers}, Активация: {activation.value}")
                ax.set_xlabel("Эпоха")
                ax.set_ylabel("MSE Loss")
                ax.legend(fontsize=6)
                ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig("regression_loss_curves.png", dpi=120, bbox_inches="tight")
        plt.close(fig)

    @staticmethod
    def _plot_mse_bars(results: Sequence[RegressionResult]) -> None:
        # Sort by MSE ascending (best first)
        sorted_results = sorted(results, key=lambda r: r.mse)

        fig, ax = plt.subplots(figsize=(max(16, len(sorted_results) * 0.8), 7))

        labels: list[str] = [
            f"n={r.hyper_parameters.hidden_neurons}\n"
            f"L={r.hyper_parameters.num_hidden_layers}\n"
            f"{r.hyper_parameters.activation.value}\n"
            f"bs={r.hyper_parameters.batch_size}"
            for r in sorted_results
        ]
        mse_values: list[float] = [r.mse for r in sorted_results]

        color_map: dict[RegressionActivationType, str] = {
            RegressionActivationType.RELU: "#4CAF50",
            RegressionActivationType.TANH: "#FF9800",
            RegressionActivationType.LEAKY_RELU: "#2196F3",
        }
        colors: list[str] = [
            color_map.get(r.hyper_parameters.activation, "#9E9E9E") for r in sorted_results
        ]

        bars = ax.bar(range(len(mse_values)), mse_values, color=colors, edgecolor="black", linewidth=0.5)

        for bar, mse_val in zip(bars, mse_values, strict=False):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.005,
                f"{mse_val:.3f}",
                ha="center",
                va="bottom",
                fontsize=6,
                fontweight="bold",
            )

        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, fontsize=6, ha="center")
        ax.set_ylabel("MSE")
        ax.set_title("Сравнение MSE моделей (отсортировано по возрастанию)", fontsize=14)
        ax.grid(axis="y", alpha=0.3)

        legend_elements = [
            Patch(facecolor=c, edgecolor="black", label=a.value)
            for a, c in color_map.items()
        ]
        ax.legend(handles=legend_elements, loc="upper right", fontsize=10)

        plt.tight_layout()
        plt.savefig("regression_mse_comparison.png", dpi=120, bbox_inches="tight")
        plt.close(fig)

    @staticmethod
    def _print_best(results: Sequence[RegressionResult]) -> None:
        best: RegressionResult = min(results, key=lambda r: r.mse)
        print("\n🏆  Лучшая конфигурация (минимальный MSE):")  # noqa: T201
        print(f"    Нейроны:    {best.hyper_parameters.hidden_neurons}")  # noqa: T201
        print(f"    Слои:       {best.hyper_parameters.num_hidden_layers}")  # noqa: T201
        print(f"    Активация:  {best.hyper_parameters.activation.value}")  # noqa: T201
        print(f"    Batch size: {best.hyper_parameters.batch_size}")  # noqa: T201
        print(f"    LR:         {best.hyper_parameters.learning_rate}")  # noqa: T201
        print(f"    MSE:        {best.mse:.4f}")  # noqa: T201
        print(f"    MAE:        {best.mae:.4f}")  # noqa: T201
        print(f"    R²:         {best.r2_score:.4f}")  # noqa: T201

