"""Service for running NIST tests."""

from pathlib import Path

from theory_of_pseudorandom_generators.domain.common.services.base import DomainService
from theory_of_pseudorandom_generators.domain.methodology_for_assessing_the_quality_of_gpsp_evaluation_tests_checking_unlinked_series.entities.nist_test import (
    BitFrequencyTest,
    BlockFrequencyTest,
    NISTTest,
    RunsTest,
)


class NISTTestService(DomainService):
    """Service for running NIST statistical tests."""

    def get_binary_sequence_from_file(self, file_path: Path) -> str:
        """Read binary sequence from file.

        Args:
            file_path: Path to file with binary sequence

        Returns:
            Binary sequence as string
        """
        try:
            with open(file_path, encoding="utf-8") as f:
                # Read first line (matching Java implementation)
                first_line = f.readline().strip()
                if not first_line:
                    msg = f"Файл {file_path} пуст"
                    raise ValueError(msg)
                return first_line
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
        n = sequence_length // block_size
        min_m = max(20, int(0.01 * n))

        if block_size < min_m:
            return False, f"m должно быть >= {min_m}"

        if block_size <= 0.01 * n:
            return False, "m должно быть > 0.01 * n"

        if n >= 100:
            return False, "n должно быть < 100"

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
        tests: list[NISTTest] = [
            BitFrequencyTest(),
            BlockFrequencyTest(block_size),
            RunsTest(),
        ]

        results = []
        for test in tests:
            try:
                p_value = test.test(sequence)
                is_success = test.is_successful(p_value, alpha)
                results.append(
                    {
                        "test_name": str(test),
                        "p_value": p_value,
                        "is_success": is_success,
                        "alpha": alpha,
                    }
                )
            except (ValueError, Exception) as e:
                results.append(
                    {
                        "test_name": str(test),
                        "p_value": None,
                        "is_success": False,
                        "error": str(e),
                    }
                )

        return results


