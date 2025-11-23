"""Service for generating histograms."""

from collections import Counter
from collections.abc import Sequence
from pathlib import Path
from typing import Final

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

from theory_of_pseudorandom_generators.domain.common.services.base import DomainService


class HistogramService(DomainService):
    """Service for generating histograms of element distribution."""

    def get_data_from_file(self, file_path: Path) -> Sequence[int]:
        """Read decimal sequence from file.

        Supports different file formats:
        - Files with "Десятичные значения:" marker followed by tab-separated numbers
        - Files with just tab-separated numbers on last line
        - Files with space-separated numbers

        Args:
            file_path: Path to file with sequence

        Returns:
            List of decimal numbers
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]

            if not lines:
                msg = f"Файл {file_path} пуст"
                raise ValueError(msg)

            decimal_line = None

            # First, try to find "Десятичные значения:" marker
            for i, line in enumerate(lines):
                if "Десятичные значения" in line or "десятичные" in line.lower():
                    if i + 1 < len(lines):
                        decimal_line = lines[i + 1]
                        break

            # If no marker found, try to find tab-separated line (usually last meaningful line)
            if decimal_line is None:
                for line in reversed(lines):
                    line = line.strip()
                    if not line:
                        continue
                    # Skip header lines
                    if any(
                        keyword in line.lower()
                        for keyword in ["генератор", "период", "значение", "количество"]
                    ):
                        continue
                    # Check if it looks like tab-separated numbers
                    if "\t" in line:
                        # Verify it's numbers
                        parts = line.split("\t")
                        if all(part.strip().isdigit() for part in parts if part.strip()):
                            decimal_line = line
                            break
                    # Or space-separated numbers
                    elif " " in line:
                        parts = line.split()
                        if all(part.strip().isdigit() for part in parts if part.strip()):
                            decimal_line = line
                            break

            # Parse the found line
            if decimal_line:
                if "\t" in decimal_line:
                    values = [
                        int(x.strip())
                        for x in decimal_line.split("\t")
                        if x.strip() and x.strip().isdigit()
                    ]
                else:
                    values = [
                        int(x.strip())
                        for x in decimal_line.split()
                        if x.strip() and x.strip().isdigit()
                    ]
                if values:
                    return values

            # Fallback: try to parse all lines as numbers
            all_numbers = []
            for line in lines:
                # Skip non-numeric lines
                if any(
                    keyword in line.lower()
                    for keyword in ["генератор", "период", "значение", "количество", "десятичные"]
                ):
                    continue
                # Try tab-separated
                if "\t" in line:
                    parts = line.split("\t")
                    for part in parts:
                        if part.strip().isdigit():
                            all_numbers.append(int(part.strip()))
                # Try space-separated
                else:
                    parts = line.split()
                    for part in parts:
                        if part.strip().isdigit():
                            all_numbers.append(int(part.strip()))

            if all_numbers:
                return all_numbers

            msg = f"Не удалось найти числовые данные в файле {file_path}"
            raise ValueError(msg)

        except OSError as e:
            msg = f"Ошибка при чтении файла {file_path}: {e}"
            raise ValueError(msg) from e
        except ValueError as e:
            raise

    def create_histogram(
        self,
        data: Sequence[int],
        title: str,
        output_path: Path | None = None,
        show: bool = True,
    ) -> None:
        """Create histogram from data.

        Args:
            data: Sequence of numbers to analyze
            title: Chart title
            output_path: Optional path to save the histogram
            show: Whether to display the histogram
        """
        if not data:
            msg = "Данные для построения гистограммы пусты"
            raise ValueError(msg)

        # Count frequency of each value
        counter = Counter(data)
        unique_values = sorted(counter.keys())
        frequencies = [counter[val] for val in unique_values]

        # Create histogram
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(
            [str(val) for val in unique_values],
            frequencies,
            color="blue",
            edgecolor="black",
            alpha=0.7,
        )

        ax.set_xlabel("Значение", fontsize=12)
        ax.set_ylabel("Количество", fontsize=12)
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.grid(axis="y", alpha=0.3)

        # Set integer ticks on y-axis
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{int(height)}",
                ha="center",
                va="bottom",
                fontsize=8,
            )

        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches="tight")

        if show:
            plt.show()
        else:
            plt.close(fig)

    def calculate_statistics(self, data: Sequence[int]) -> dict[str, float]:
        """Calculate statistics for the sequence.

        Args:
            data: Sequence of numbers

        Returns:
            Dictionary with statistics
        """
        if not data:
            return {}

        counter = Counter(data)
        total = len(data)
        unique_count = len(counter)

        # Calculate frequencies
        frequencies = {val: count / total for val, count in counter.items()}

        # Expected frequency for uniform distribution
        expected_frequency = 1.0 / unique_count if unique_count > 0 else 0

        # Calculate uniformity measure (variance of frequencies)
        frequency_values = list(frequencies.values())
        mean_freq = sum(frequency_values) / len(frequency_values) if frequency_values else 0
        variance = (
            sum((f - mean_freq) ** 2 for f in frequency_values) / len(frequency_values)
            if frequency_values
            else 0
        )

        return {
            "total_elements": total,
            "unique_elements": unique_count,
            "expected_frequency": expected_frequency,
            "frequency_variance": variance,
            "frequencies": frequencies,
        }

