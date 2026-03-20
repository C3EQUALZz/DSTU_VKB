"""NIST test interface and implementations."""

import logging
from typing import Protocol

import numpy as np
from scipy.special import erfc, gammainc

logger = logging.getLogger(__name__)


class NISTTest(Protocol):
    """Protocol for NIST statistical tests."""

    def test(self, sequence: str) -> float:
        """Run the test on a binary sequence.

        Args:
            sequence: Binary sequence as string

        Returns:
            P-value of the test
        """
        ...

    def is_successful(self, p_value: float, alpha: float) -> bool:
        """Check if test passed.

        Args:
            p_value: Calculated p-value
            alpha: Significance level

        Returns:
            True if test passed (p-value >= alpha)
        """
        ...

    def __str__(self) -> str:
        """Return test name."""
        ...


class BitFrequencyTest:
    """Frequency (Monobit) Test - проверяет баланс единиц и нулей."""

    def test(self, sequence: str) -> float:
        """Run frequency test.

        Args:
            sequence: Binary sequence

        Returns:
            P-value
        """
        logger.info("Запуск частотно-побитового теста")
        seq = np.array([int(bit) for bit in sequence])
        n = len(seq)
        logger.info("Длина последовательности: n=%d", n)
        # Transform: 0 -> -1, 1 -> 1
        sum_transformed = np.sum(2 * seq - 1)
        logger.info("Сумма преобразованных значений (0→-1, 1→1): %d", sum_transformed)
        s_obs = abs(sum_transformed) / np.sqrt(n)
        s_obs /= np.sqrt(2)
        logger.info("Статистика s_obs (мера отклонения от идеального баланса 0.5): %.6f", s_obs)
        p_value = float(erfc(s_obs))
        logger.info("P-value (вероятность случайного получения такого отклонения): %.6f", p_value)
        return p_value

    def is_successful(self, p_value: float, alpha: float) -> bool:
        """Check if test passed."""
        return p_value >= alpha

    def __str__(self) -> str:
        return "Частотно-побитовый тест"


class BlockFrequencyTest:
    """Frequency Test within a Block - проверяет частоту единиц в блоках."""

    def __init__(self, block_size: int) -> None:
        """Initialize test with block size.

        Args:
            block_size: Size of each block (m)
        """
        self.block_size = block_size

    def test(self, sequence: str) -> float:
        """Run block frequency test.

        Args:
            sequence: Binary sequence

        Returns:
            P-value

        Raises:
            ValueError: If sequence is too short
        """
        logger.info("Запуск частотно-блочного теста с размером блока=%d", self.block_size)
        n = len(sequence) // self.block_size
        if len(sequence) < self.block_size * n:
            msg = "Последовательность не подходит для этого теста"
            raise ValueError(msg)

        logger.info("Количество блоков: n=%d", n)
        # Split into blocks
        blocks = []
        for i in range(n):
            block_str = sequence[i * self.block_size : (i + 1) * self.block_size]
            block = np.array([int(bit) for bit in block_str])
            blocks.append(block)

        # Calculate chi-square statistic
        chi_square = 4.0 * self.block_size
        logger.info("Начальное значение chi_square: %.6f", chi_square)
        for i, block in enumerate(blocks):
            proportion = np.mean(block)
            chi_square += (proportion - 0.5) ** 2
            logger.info("Блок %d: доля единиц=%.6f", i, proportion)
        logger.info("Итоговое chi_square (мера отклонения долей единиц в блоках от 0.5): %.6f", chi_square)

        # Calculate p-value using incomplete gamma function
        # Gamma.incompleteGamma(n/2, chi_square/2) in Java
        # scipy.special.gammainc(a, x) = lower incomplete gamma / gamma(a)
        # We need upper incomplete gamma: 1 - gammainc(n/2, chi_square/2)
        p_value = 1.0 - gammainc(n / 2.0, chi_square / 2.0)
        logger.info("P-value (вероятность случайного получения такого отклонения): %.6f", p_value)
        return float(p_value)

    def is_successful(self, p_value: float, alpha: float) -> bool:
        """Check if test passed."""
        return p_value >= alpha

    def __str__(self) -> str:
        return "Частотно-блочный тест"


class RunsTest:
    """Runs Test - проверяет последовательность одинаковых бит."""

    def test(self, sequence: str) -> float:
        """Run runs test.

        Args:
            sequence: Binary sequence

        Returns:
            P-value
        """
        logger.info("Запуск теста на последовательность одинаковых бит")
        seq = np.array([int(bit) for bit in sequence])
        n = len(seq)
        one_count = np.mean(seq)
        logger.info("Длина последовательности: n=%d, доля единиц: %.6f", n, one_count)

        # Check if sequence passes preliminary test
        if abs(one_count - 0.5) >= 2 / np.sqrt(n):
            logger.info("Предварительная проверка не пройдена: |%.6f - 0.5| >= 2/sqrt(%d)", one_count, n)
            return 0.0
        logger.info("Предварительная проверка пройдена")

        # Count runs (transitions)
        v_n_obs = 0
        for i in range(len(seq) - 1):
            if seq[i] != seq[i + 1]:
                v_n_obs += 1
        v_n_obs += 1
        logger.info("Количество серий v_n_obs (число последовательностей одинаковых бит): %d", v_n_obs)

        # Calculate p-value
        numerator = v_n_obs - 2 * n * one_count * (1 - one_count)
        numerator = abs(numerator)
        denominator = 2 * np.sqrt(2 * n) * one_count * (1 - one_count)
        p_value_normalized = numerator / denominator
        logger.info("Числитель (отклонение числа серий от ожидаемого): %.6f, Знаменатель (нормировочный коэффициент): %.6f, Нормализованное значение: %.6f", 
                     numerator, denominator, p_value_normalized)
        p_value = float(erfc(p_value_normalized))
        logger.info("P-value (вероятность случайного получения такого отклонения): %.6f", p_value)
        return p_value

    def is_successful(self, p_value: float, alpha: float) -> bool:
        """Check if test passed."""
        return p_value >= alpha

    def __str__(self) -> str:
        return "Тест на последовательность одинаковых бит"



