"""Service for generating histograms."""

import logging
from collections import Counter
from collections.abc import Sequence
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")  # Use non-interactive backend

from theory_of_pseudorandom_generators.domain.common.services.base import DomainService

logger: logging.Logger = logging.getLogger(__name__)


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
            with open(file_path, encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]

            if not lines:
                msg = f"Файл {file_path} пуст"
                raise ValueError(msg)

            decimal_line = None

            # First, try to find "Десятичные значения:" marker
            for i, line in enumerate(lines):
                if "Десятичные значения" in line or "десятичные" in line.lower():
                    # Берем следующую непустую строку после маркера
                    for j in range(i + 1, len(lines)):
                        next_line = lines[j].strip()
                        if not next_line:
                            continue
                        # Проверяем, что это строка с числами (табуляция или пробелы)
                        if "\t" in next_line or (next_line and all(c.isdigit() or c.isspace() or c == '\t' for c in next_line)):
                            decimal_line = next_line
                            break
                    if decimal_line:
                        break

            # If no marker found, try to find tab-separated line (usually last meaningful line)
            if decimal_line is None:
                for line in reversed(lines):
                    line = line.strip()
                    if not line:
                        continue
                    # Skip header lines and intermediate results (lines with "->" or ".")
                    if any(
                        keyword in line.lower()
                        for keyword in ["генератор", "период", "значение", "количество", "->"]
                    ) or "." in line and "->" in line:
                        continue
                    # Check if it looks like tab-separated numbers
                    if "\t" in line:
                        # Verify it's numbers
                        parts = line.split("\t")
                        if parts and all(part.strip().isdigit() for part in parts if part.strip()):
                            decimal_line = line
                            break
                    # Or space-separated numbers (but not single numbers from intermediate results)
                    elif " " in line and not line.startswith(("0.", "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")):
                        parts = line.split()
                        # Проверяем, что это не промежуточные результаты (не должно быть "->")
                        if "->" not in line and all(part.strip().isdigit() for part in parts if part.strip()):
                            decimal_line = line
                            break

            # Parse the found line
            if decimal_line:
                logger.debug("Найдена строка с десятичными значениями (первые 100 символов): %s", decimal_line[:100])
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
                logger.info("Прочитано десятичных чисел из файла: %s", len(values))
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
        except ValueError:
            raise

    def create_histogram(
        self,
        data: Sequence[int],
        title: str,
        output_path: Path | None = None,
        show: bool = True,
        bins: int | None = None,
    ) -> None:
        """Create histogram from data.

        Args:
            data: Sequence of numbers to analyze
            title: Chart title
            output_path: Optional path to save the histogram
            show: Whether to display the histogram
            bins: Optional number of bins (use Matplotlib hist)
        """
        if not data:
            msg = "Данные для построения гистограммы пусты"
            raise ValueError(msg)
        total = len(data)

        if bins is not None and bins > 0:
            fig_width = 12 if bins <= 50 else 16
            fig_height = 6
            fig, ax = plt.subplots(figsize=(fig_width, fig_height))
            ax.hist(
                data,
                bins=bins,
                weights=[1 / total] * total,
                color="blue",
                edgecolor="black",
                alpha=0.7,
            )
            ax.set_xlabel("Значение", fontsize=12)
            ax.set_ylabel("Частота", fontsize=12)
            ax.set_title(title, fontsize=14, fontweight="bold")
            ax.grid(axis="y", alpha=0.3)
            plt.tight_layout()

            if output_path:
                plt.savefig(output_path, dpi=300, bbox_inches="tight")

            if show:
                plt.show()
            else:
                plt.close(fig)
            return

        # Count frequency of each value
        counter = Counter(data)
        unique_values = sorted(counter.keys())
        frequencies = [counter[val] / total for val in unique_values]

        # Определяем размер фигуры в зависимости от количества уникальных значений
        num_unique = len(unique_values)
        if num_unique > 100:
            # Для большого количества значений увеличиваем ширину и уменьшаем размер шрифта
            fig_width = max(20, num_unique * 0.15)
            fig_height = 8
            font_size = 6
            rotation_angle = 90  # Вертикальные подписи для лучшей читаемости
        elif num_unique > 50:
            fig_width = 16
            fig_height = 7
            font_size = 7
            rotation_angle = 75
        else:
            fig_width = 12
            fig_height = 6
            font_size = 8
            rotation_angle = 45

        # Create histogram
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        bars = ax.bar(
            [str(val) for val in unique_values],
            frequencies,
            color="blue",
            edgecolor="black",
            alpha=0.7,
        )

        ax.set_xlabel("Значение", fontsize=12)
        ax.set_ylabel("Частота", fontsize=12)
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.grid(axis="y", alpha=0.3)

        # Add value labels on bars (только если не слишком много значений)
        if num_unique <= 100:
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height,
                    f"{height:.3f}",
                    ha="center",
                    va="bottom",
                    fontsize=font_size,
                )

        # Настройка подписей на оси X
        # Если значений много, показываем только каждое N-е значение
        if num_unique > 50:
            # Показываем примерно 30-40 подписей максимум
            step = max(1, num_unique // 40)
            tick_positions = list(range(0, num_unique, step))
            tick_labels = [str(unique_values[i]) for i in tick_positions]
            ax.set_xticks(tick_positions)
            ax.set_xticklabels(tick_labels, rotation=rotation_angle, ha="right", fontsize=font_size)
        else:
            plt.xticks(rotation=rotation_angle, ha="right", fontsize=font_size)
        
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

