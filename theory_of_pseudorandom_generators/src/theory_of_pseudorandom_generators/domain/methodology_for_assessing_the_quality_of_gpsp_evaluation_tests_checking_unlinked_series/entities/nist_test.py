"""NIST test interface and implementations."""

from abc import ABC, abstractmethod
from typing import Protocol

import numpy as np
from scipy.special import erfc, gammainc


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
        seq = np.array([int(bit) for bit in sequence])
        n = len(seq)
        # Transform: 0 -> -1, 1 -> 1
        sum_transformed = np.sum(2 * seq - 1)
        s_obs = abs(sum_transformed) / np.sqrt(n)
        s_obs /= np.sqrt(2)
        return float(erfc(s_obs))

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
        n = len(sequence) // self.block_size
        if len(sequence) < self.block_size * n:
            msg = "Последовательность не подходит для этого теста"
            raise ValueError(msg)

        # Split into blocks
        blocks = []
        for i in range(n):
            block_str = sequence[i * self.block_size : (i + 1) * self.block_size]
            block = np.array([int(bit) for bit in block_str])
            blocks.append(block)

        # Calculate chi-square statistic
        chi_square = 4.0 * self.block_size
        for block in blocks:
            proportion = np.mean(block)
            chi_square += (proportion - 0.5) ** 2

        # Calculate p-value using incomplete gamma function
        # Gamma.incompleteGamma(n/2, chi_square/2) in Java
        # scipy.special.gammainc(a, x) = lower incomplete gamma / gamma(a)
        # We need upper incomplete gamma: 1 - gammainc(n/2, chi_square/2)
        p_value = 1.0 - gammainc(n / 2.0, chi_square / 2.0)
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
        seq = np.array([int(bit) for bit in sequence])
        n = len(seq)
        one_count = np.mean(seq)

        # Check if sequence passes preliminary test
        if abs(one_count - 0.5) >= 2 / np.sqrt(n):
            return 0.0

        # Count runs (transitions)
        v_n_obs = 0
        for i in range(len(seq) - 1):
            if seq[i] != seq[i + 1]:
                v_n_obs += 1
        v_n_obs += 1

        # Calculate p-value
        numerator = v_n_obs - 2 * n * one_count * (1 - one_count)
        numerator = abs(numerator)
        denominator = 2 * np.sqrt(2 * n) * one_count * (1 - one_count)
        p_value_normalized = numerator / denominator
        return float(erfc(p_value_normalized))

    def is_successful(self, p_value: float, alpha: float) -> bool:
        """Check if test passed."""
        return p_value >= alpha

    def __str__(self) -> str:
        return "Тест на последовательность одинаковых бит"

