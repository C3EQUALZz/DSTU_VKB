"""Service for generating plane distributions."""

import math
from collections.abc import Sequence
from pathlib import Path
from typing import Final

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

from theory_of_pseudorandom_generators.domain.common.services.base import DomainService


class PlaneDistributionService(DomainService):
    """Service for generating 2D distributions of PRNG sequences."""

    def get_data_from_file(self, file_path: Path) -> Sequence[int]:
        """Read decimal sequence from file.

        Args:
            file_path: Path to file with sequence

        Returns:
            List of decimal numbers
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                # Read first line with tab-separated values (matching Java implementation)
                first_line = f.readline().strip()
                if not first_line:
                    msg = f"Файл {file_path} пуст"
                    raise ValueError(msg)

                # Parse tab-separated values
                if "\t" in first_line:
                    values = [
                        int(x.strip())
                        for x in first_line.split("\t")
                        if x.strip() and x.strip().isdigit()
                    ]
                else:
                    # Fallback: try space-separated
                    values = [
                        int(x.strip())
                        for x in first_line.split()
                        if x.strip() and x.strip().isdigit()
                    ]

                if not values:
                    msg = f"Не удалось найти числовые данные в файле {file_path}"
                    raise ValueError(msg)

                return values

        except OSError as e:
            msg = f"Ошибка при чтении файла {file_path}: {e}"
            raise ValueError(msg) from e
        except ValueError as e:
            raise

    def create_plane_distribution(
        self,
        data: Sequence[int],
        title: str,
        output_path: Path | None = None,
        show: bool = True,
    ) -> None:
        """Create 2D distribution plot (x[i] vs x[i+1]).

        Args:
            data: Sequence of numbers
            title: Plot title
            output_path: Optional path to save the plot
            show: Whether to display the plot
        """
        if len(data) < 2:
            msg = "Недостаточно данных для построения распределения (нужно минимум 2 элемента)"
            raise ValueError(msg)

        # X coordinates: elements from index 0 to n-1
        # Y coordinates: elements from index 1 to n
        x_coords = list(data[:-1])
        y_coords = list(data[1:])

        # Create scatter plot
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.scatter(x_coords, y_coords, s=10, alpha=0.6, c="blue", edgecolors="black", linewidths=0.5)

        ax.set_xlabel("x[i]", fontsize=12)
        ax.set_ylabel("x[i+1]", fontsize=12)
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches="tight")

        if show:
            plt.show()
        else:
            plt.close(fig)

    def create_multiple_distributions(
        self,
        sequences: list[tuple[str, Sequence[int]]],
        output_path: Path | None = None,
        show: bool = True,
    ) -> None:
        """Create multiple 2D distribution plots in subplots.

        Args:
            sequences: List of (title, data) tuples
            output_path: Optional path to save the plot
            show: Whether to display the plot
        """
        if not sequences:
            msg = "Нет последовательностей для построения"
            raise ValueError(msg)

        # Calculate grid dimensions (similar to Java implementation)
        n = len(sequences)
        # Find the largest factor <= sqrt(n)
        width = int(math.sqrt(n))
        while n % width != 0:
            width -= 1
        height = n // width

        # Create subplots
        fig, axes = plt.subplots(height, width, figsize=(width * 5, height * 5))
        if n == 1:
            axes = [axes]
        elif height == 1:
            axes = [axes] if width == 1 else axes
        else:
            axes = axes.flatten()

        for idx, (title, data) in enumerate(sequences):
            if len(data) < 2:
                continue

            ax = axes[idx] if n > 1 else axes[0]

            # X coordinates: elements from index 0 to n-1
            # Y coordinates: elements from index 1 to n
            x_coords = list(data[:-1])
            y_coords = list(data[1:])

            ax.scatter(x_coords, y_coords, s=10, alpha=0.6, c="blue", edgecolors="black", linewidths=0.5)
            ax.set_xlabel("x[i]", fontsize=10)
            ax.set_ylabel("x[i+1]", fontsize=10)
            ax.set_title(title, fontsize=12, fontweight="bold")
            ax.grid(True, alpha=0.3)

        # Hide unused subplots
        for idx in range(n, len(axes)):
            axes[idx].set_visible(False)

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches="tight")

        if show:
            plt.show()
        else:
            plt.close(fig)

    def analyze_dependence(self, data: Sequence[int]) -> dict[str, float]:
        """Analyze dependence between consecutive elements.

        Args:
            data: Sequence of numbers

        Returns:
            Dictionary with dependence metrics
        """
        if len(data) < 2:
            return {}

        x_coords = list(data[:-1])
        y_coords = list(data[1:])

        # Calculate correlation coefficient
        n = len(x_coords)
        mean_x = sum(x_coords) / n
        mean_y = sum(y_coords) / n

        numerator = sum((x_coords[i] - mean_x) * (y_coords[i] - mean_y) for i in range(n))
        sum_sq_x = sum((x - mean_x) ** 2 for x in x_coords)
        sum_sq_y = sum((y - mean_y) ** 2 for y in y_coords)

        if sum_sq_x == 0 or sum_sq_y == 0:
            correlation = 0.0
        else:
            correlation = numerator / math.sqrt(sum_sq_x * sum_sq_y)

        return {
            "correlation": correlation,
            "sequence_length": len(data),
            "unique_pairs": len(set(zip(x_coords, y_coords))),
        }

