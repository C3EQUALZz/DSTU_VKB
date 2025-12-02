"""Command handler for plane distribution generation."""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import final

from theory_of_pseudorandom_generators.domain.methodology_for_assessing_the_quality_of_gpsp_distribution_on_plane.services.plane_distribution_service import (
    PlaneDistributionService,
)

logger: logging.Logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class MethodologyForAssessingTheQualityOfGpspDistributionOnPlaneCommand:
    """Command for generating plane distributions."""

    linear_congruent_file: Path | None = None
    square_congruent_file: Path | None = None
    fibonacci_file: Path | None = None
    geffe_file: Path | None = None
    output_path: Path | None = None
    show: bool = True


@final
class MethodologyForAssessingTheQualityOfGpspDistributionOnPlaneCommandHandler:
    """Handler for plane distribution generation command."""

    def __init__(self, plane_distribution_service: PlaneDistributionService) -> None:
        """Initialize handler with plane distribution service.

        Args:
            plane_distribution_service: Service for generating plane distributions
        """
        self._plane_distribution_service: PlaneDistributionService = (
            plane_distribution_service
        )

    def __call__(
        self,
        command: MethodologyForAssessingTheQualityOfGpspDistributionOnPlaneCommand,
    ) -> None:
        """Handle plane distribution generation command.

        Args:
            command: Command with file paths
        """
        logger.info("Начинается построение распределения на плоскости")

        sequences = []

        # Linear Congruent Generator
        if command.linear_congruent_file and command.linear_congruent_file.exists():
            try:
                data = self._plane_distribution_service.get_data_from_file(
                    command.linear_congruent_file
                )
                title = "Линейный генератор"
                sequences.append((title, data))
                logger.info("Загружены данные для линейного генератора: %s элементов", len(data))
            except Exception as e:
                logger.error("Ошибка при загрузке данных линейного генератора: %s", e)

        # Square Congruent Generator
        if command.square_congruent_file and command.square_congruent_file.exists():
            try:
                data = self._plane_distribution_service.get_data_from_file(
                    command.square_congruent_file
                )
                title = "Квадратичный генератор"
                sequences.append((title, data))
                logger.info("Загружены данные для квадратичного генератора: %s элементов", len(data))
            except Exception as e:
                logger.error("Ошибка при загрузке данных квадратичного генератора: %s", e)

        # Fibonacci Generator
        if command.fibonacci_file and command.fibonacci_file.exists():
            try:
                data = self._plane_distribution_service.get_data_from_file(
                    command.fibonacci_file
                )
                title = "Генератор Фибоначчи"
                sequences.append((title, data))
                logger.info("Загружены данные для генератора Фибоначчи: %s элементов", len(data))
            except Exception as e:
                logger.error("Ошибка при загрузке данных генератора Фибоначчи: %s", e)

        # Geffe Generator
        if command.geffe_file and command.geffe_file.exists():
            try:
                data = self._plane_distribution_service.get_data_from_file(
                    command.geffe_file
                )
                title = "Генератор Геффе"
                sequences.append((title, data))
                logger.info("Загружены данные для генератора Геффе: %s элементов", len(data))
            except Exception as e:
                logger.error("Ошибка при загрузке данных генератора Геффе: %s", e)

        if not sequences:
            logger.warning("Не найдено ни одного файла с данными для построения распределения")
            return

        # Analyze dependencies
        for title, data in sequences:
            if len(data) >= 2:
                stats = self._plane_distribution_service.analyze_dependence(data)
                logger.info("Анализ зависимости для %s:", title)
                logger.info("  Корреляция: %.6f", stats.get("correlation", 0))
                logger.info("  Уникальных пар: %s", stats.get("unique_pairs", 0))

        # Create distribution plots
        try:
            self._plane_distribution_service.create_multiple_distributions(
                sequences=sequences,
                output_path=command.output_path,
                show=command.show,
            )
            if command.output_path:
                logger.info("Распределение сохранено: %s", command.output_path)
        except Exception as e:
            logger.error("Ошибка при построении распределения: %s", e)



