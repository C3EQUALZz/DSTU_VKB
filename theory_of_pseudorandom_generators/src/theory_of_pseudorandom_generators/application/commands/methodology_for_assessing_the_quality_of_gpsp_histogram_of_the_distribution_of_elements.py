"""Command handler for histogram generation."""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import final

from theory_of_pseudorandom_generators.domain.methodology_for_assessing_the_quality_of_gpsp_histogram_of_the_distribution_of_elements.services.histogram_service import (
    HistogramService,
)

logger: logging.Logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class MethodologyForAssessingTheQualityOfGpspHistogramOfTheDistributionOfElementsCommand:
    """Command for generating histograms."""

    linear_congruent_file: Path | None = None
    square_congruent_file: Path | None = None
    fibonacci_file: Path | None = None
    geffe_file: Path | None = None
    output_dir: Path | None = None
    show: bool = True


@final
class MethodologyForAssessingTheQualityOfGpspHistogramOfTheDistributionOfElementsCommandHandler:
    """Handler for histogram generation command."""

    def __init__(self, histogram_service: HistogramService) -> None:
        """Initialize handler with histogram service.

        Args:
            histogram_service: Service for generating histograms
        """
        self._histogram_service: HistogramService = histogram_service

    def __call__(
        self,
        command: MethodologyForAssessingTheQualityOfGpspHistogramOfTheDistributionOfElementsCommand,
    ) -> None:
        """Handle histogram generation command.

        Args:
            command: Command with file paths
        """
        logger.info("Начинается построение гистограмм распределения элементов")

        generators = []

        # Linear Congruent Generator
        if command.linear_congruent_file and command.linear_congruent_file.exists():
            try:
                data = self._histogram_service.get_data_from_file(
                    command.linear_congruent_file
                )
                title = "Линейный конгруэнтный генератор"
                generators.append((title, data, "linear_congruent"))
                logger.info("Загружены данные для линейного конгруэнтного генератора")
            except Exception as e:
                logger.error("Ошибка при загрузке данных линейного генератора: %s", e)

        # Square Congruent Generator
        if command.square_congruent_file and command.square_congruent_file.exists():
            try:
                data = self._histogram_service.get_data_from_file(
                    command.square_congruent_file
                )
                title = "Квадратичный конгруэнтный генератор"
                generators.append((title, data, "square_congruent"))
                logger.info("Загружены данные для квадратичного конгруэнтного генератора")
            except Exception as e:
                logger.error("Ошибка при загрузке данных квадратичного генератора: %s", e)

        # Fibonacci Generator
        if command.fibonacci_file and command.fibonacci_file.exists():
            try:
                data = self._histogram_service.get_data_from_file(command.fibonacci_file)
                title = "Генератор Фибоначчи"
                generators.append((title, data, "fibonacci"))
                logger.info("Загружены данные для генератора Фибоначчи")
            except Exception as e:
                logger.error("Ошибка при загрузке данных генератора Фибоначчи: %s", e)

        # Geffe Generator
        if command.geffe_file and command.geffe_file.exists():
            try:
                data = self._histogram_service.get_data_from_file(command.geffe_file)
                title = "Генератор Геффе"
                generators.append((title, data, "geffe"))
                logger.info("Загружены данные для генератора Геффе")
            except Exception as e:
                logger.error("Ошибка при загрузке данных генератора Геффе: %s", e)

        if not generators:
            logger.warning("Не найдено ни одного файла с данными для построения гистограмм")
            return

        # Generate histograms
        for title, data, name in generators:
            logger.info("Построение гистограммы для: %s", title)
            logger.info("Количество элементов: %s", len(data))

            # Calculate statistics
            stats = self._histogram_service.calculate_statistics(data)
            logger.info("Уникальных элементов: %s", stats.get("unique_elements", 0))
            logger.info("Ожидаемая частота (равномерное распределение): %.6f", stats.get("expected_frequency", 0))
            logger.info("Дисперсия частот: %.6f", stats.get("frequency_variance", 0))

            # Create histogram
            output_path = None
            if command.output_dir:
                command.output_dir.mkdir(parents=True, exist_ok=True)
                output_path = command.output_dir / f"{name}_histogram.png"

            try:
                self._histogram_service.create_histogram(
                    data=data,
                    title=title,
                    output_path=output_path,
                    show=command.show,
                )
                if output_path:
                    logger.info("Гистограмма сохранена: %s", output_path)
            except Exception as e:
                logger.error("Ошибка при построении гистограммы для %s: %s", title, e)

