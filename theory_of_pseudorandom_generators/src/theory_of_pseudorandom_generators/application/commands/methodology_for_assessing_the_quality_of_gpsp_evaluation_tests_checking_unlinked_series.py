"""Command handler for NIST tests."""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import final

from prettytable import PrettyTable

from theory_of_pseudorandom_generators.domain.methodology_for_assessing_the_quality_of_gpsp_evaluation_tests_checking_unlinked_series.services.nist_test_service import (
    NISTTestService,
)

logger: logging.Logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class MethodologyForAssessingTheQualityOfGpspEvaluationTestsCheckingUnlinkedSeriesCommand:
    """Command for running NIST tests."""

    linear_congruent_file: Path | None = None
    square_congruent_file: Path | None = None
    fibonacci_file: Path | None = None
    geffe_file: Path | None = None
    block_size: int
    alpha: float = 0.01
    max_bits: int = 0


@final
class MethodologyForAssessingTheQualityOfGpspEvaluationTestsCheckingUnlinkedSeriesCommandHandler:
    """Handler for NIST tests command."""

    def __init__(self, nist_test_service: NISTTestService) -> None:
        """Initialize handler with NIST test service.

        Args:
            nist_test_service: Service for running NIST tests
        """
        self._nist_test_service: NISTTestService = nist_test_service

    def __call__(
        self,
        command: MethodologyForAssessingTheQualityOfGpspEvaluationTestsCheckingUnlinkedSeriesCommand,
    ) -> None:
        """Handle NIST tests command.

        Args:
            command: Command with file paths and parameters
        """
        logger.info("Начинается проверка несцепленных серий")

        generators = []

        # Linear Congruent Generator
        if command.linear_congruent_file and command.linear_congruent_file.exists():
            generators.append(("LinearCongruent", command.linear_congruent_file))

        # Square Congruent Generator
        if command.square_congruent_file and command.square_congruent_file.exists():
            generators.append(("SquareCongruent", command.square_congruent_file))

        # Fibonacci Generator
        if command.fibonacci_file and command.fibonacci_file.exists():
            generators.append(("Fibonacci", command.fibonacci_file))

        # Geffe Generator
        if command.geffe_file and command.geffe_file.exists():
            generators.append(("Geffen", command.geffe_file))

        if not generators:
            logger.warning("Не найдено ни одного файла с последовательностью")
            return

        # Process each generator
        for generator_name, file_path in generators:
            logger.info("\nГенератор: %s", generator_name)
            try:
                sequence = self._nist_test_service.get_binary_sequence_from_file(
                    file_path
                )
                if command.max_bits and command.max_bits > 0:
                    sequence = sequence[: command.max_bits]
                logger.info(
                    "Последовательность (%s бит): %s", len(sequence), sequence[:100] + ("..." if len(sequence) > 100 else "")
                )

                # Validate block size
                is_valid, error_msg = self._nist_test_service.validate_block_size(
                    len(sequence), command.block_size
                )
                if not is_valid:
                    logger.error("Ошибка валидации: %s", error_msg)
                    continue

                # Run tests
                results = self._nist_test_service.run_tests(
                    sequence=sequence,
                    block_size=command.block_size,
                    alpha=command.alpha,
                )

                # Detailed per-test output
                for idx, result in enumerate(results, start=1):
                    logger.info("\nТест %s: %s", idx, result["test_name"])
                    if "error" in result:
                        logger.info("  Ошибка: %s", result["error"])
                    else:
                        logger.info("  p-value: %s", result["p_value"])
                        logger.info("  alpha : %s", result.get("alpha", command.alpha))
                        status = "success" if result["is_success"] else "failure"
                        logger.info("  Результат: %s", status)

                # Summary table using PrettyTable
                table = PrettyTable(["№", "Тест", "p-value", "alpha", "Результат"])
                table.align["Тест"] = "l"
                table.align["p-value"] = "r"
                table.align["alpha"] = "r"
                table.align["Результат"] = "l"

                for idx, result in enumerate(results, start=1):
                    name = str(result["test_name"])
                    if "error" in result:
                        p_val = "-"
                        alpha = (
                            f"{result.get('alpha', command.alpha):.2g}"
                            if result.get("alpha")
                            else "-"
                        )
                        status = f"error: {result['error']}"
                    else:
                        p_val = (
                            f"{result['p_value']:.8f}"
                            if isinstance(result["p_value"], (int, float))
                            else str(result["p_value"])
                        )
                        alpha = f"{result.get('alpha', command.alpha):.2g}"
                        status = "success" if result["is_success"] else "failure"
                    table.add_row([idx, name, p_val, alpha, status])

                logger.info("\nСводная таблица результатов для %s:\n%s", generator_name, table)

            except Exception as e:
                logger.error("Ошибка при обработке генератора %s: %s", generator_name, e)



