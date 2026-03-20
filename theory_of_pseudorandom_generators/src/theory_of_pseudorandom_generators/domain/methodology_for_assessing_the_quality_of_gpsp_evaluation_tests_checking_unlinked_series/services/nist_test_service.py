"""Service for running NIST tests."""

import logging
import re
from pathlib import Path

from theory_of_pseudorandom_generators.domain.common.services.base import DomainService
from theory_of_pseudorandom_generators.domain.methodology_for_assessing_the_quality_of_gpsp_evaluation_tests_checking_unlinked_series.entities.nist_test import (
    BitFrequencyTest,
    BlockFrequencyTest,
    NISTTest,
    RunsTest,
)

logger = logging.getLogger(__name__)


class NISTTestService(DomainService):
    """Service for running NIST statistical tests."""

    def get_binary_sequence_from_file(self, file_path: Path) -> str:
        """Read binary sequence from file.

        Args:
            file_path: Path to file with decimal numbers (will be converted to binary)

        Returns:
            Binary sequence as string (concatenated binary representations)
        """
        logger.info("Чтение двоичной последовательности из файла: %s", file_path)
        try:
            with open(file_path, encoding="utf-8") as f:
                first_line = f.readline().strip()
                if not first_line:
                    msg = f"Файл {file_path} пуст"
                    raise ValueError(msg)

                # Split by whitespace (spaces, tabs, etc.)
                numbers = re.split(r'\s+', first_line)
                logger.info("Найдено элементов для преобразования: %d", len(numbers))

                # Convert each decimal number to binary and concatenate
                binary_parts = []
                for num_str in numbers:
                    if num_str.strip():  # Skip empty strings
                        try:
                            decimal_num = int(num_str.strip())
                            # Convert to binary and remove '0b' prefix
                            binary_str = bin(decimal_num)[2:]
                            binary_parts.append(binary_str)
                        except ValueError as e:
                            msg = f"Не удалось преобразовать '{num_str}' в число: {e}"
                            raise ValueError(msg) from e

                if not binary_parts:
                    msg = f"Не найдено чисел в файле {file_path}"
                    raise ValueError(msg)

                # Concatenate all binary representations
                sequence = ''.join(binary_parts)
                logger.info("Длина итоговой двоичной последовательности: %d", len(sequence))
                return sequence
        except OSError as e:
            msg = f"Ошибка при чтении файла {file_path}: {e}"
            raise ValueError(msg) from e

    def validate_block_size(self, sequence_length: int, block_size: int) -> tuple[bool, str | None]:
        """Validate block size parameter.

        Args:
            sequence_length: Length of the sequence
            block_size: Block size (m)

        Returns:
            Tuple of (is_valid, error_message)
        """
        logger.info("Валидация размера блока: длина последовательности=%d, block_size=%d", 
                     sequence_length, block_size)
        n = sequence_length // block_size
        min_m = max(20, int(0.01 * n))
        logger.info("Вычисленные параметры: n=%d, min_m=%d", n, min_m)

        if block_size < min_m:
            logger.info("Проверка не пройдена: block_size (%d) < min_m (%d)", block_size, min_m)
            return False, f"m должно быть >= {min_m}"

        if block_size <= 0.01 * n:
            logger.info("Проверка не пройдена: block_size (%d) <= 0.01 * n (%.2f)", 
                         block_size, 0.01 * n)
            return False, "m должно быть > 0.01 * n"

        if n >= 100:
            logger.info("Проверка не пройдена: n (%d) >= 100", n)
            return False, "n должно быть < 100"

        logger.info("Все проверки пройдены")
        return True, None

    def run_tests(
        self,
        sequence: str,
        block_size: int,
        alpha: float = 0.01,
    ) -> list[dict[str, str | float | bool]]:
        """Run all NIST tests on a sequence.

        Args:
            sequence: Binary sequence
            block_size: Block size for BlockFrequencyTest
            alpha: Significance level

        Returns:
            List of test results with name, p-value, and success status
        """
        logger.info("Запуск NIST тестов: длина последовательности=%d, block_size=%d, alpha=%.4f",
                    len(sequence), block_size, alpha)
        tests: list[NISTTest] = [
            BitFrequencyTest(),
            BlockFrequencyTest(block_size),
            RunsTest(),
        ]
        logger.info("Создано %d тестов для выполнения", len(tests))

        results = []
        for test in tests:
            try:
                logger.info("Выполнение теста: %s", str(test))
                p_value = test.test(sequence)
                is_success = test.is_successful(p_value, alpha)
                logger.info("Тест '%s': p_value=%.6f, is_success=%s", 
                             str(test), p_value, is_success)
                results.append(
                    {
                        "test_name": str(test),
                        "p_value": p_value,
                        "is_success": is_success,
                        "alpha": alpha,
                    }
                )
            except (ValueError, Exception) as e:
                logger.exception("Ошибка при выполнении теста %s: %s", str(test), e)
                results.append(
                    {
                        "test_name": str(test),
                        "p_value": None,
                        "is_success": False,
                        "error": str(e),
                    }
                )

        logger.info("NIST тесты завершены. Успешно: %d из %d", 
                    sum(1 for r in results if r.get("is_success", False)), len(results))
        return results



