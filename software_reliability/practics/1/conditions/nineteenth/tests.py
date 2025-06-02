from typing import List

import pytest

from conditions.nineteenth.main import is_prime, get_primes_in_range


@pytest.mark.parametrize(
    "number, expected",
    [
        (2, True),
        (3, True),
        (4, False),
        (9, False),
        (17, True),
        (1, False),
        (0, False),
        (-5, False),
        (49, False),
        (149, True),
    ],
)
def test_is_prime(number: int, expected: bool) -> None:
    assert is_prime(number) == expected


@pytest.mark.parametrize(
    "n, m, expected",
    [
        (2, 10, [2, 3, 5, 7]),
        (10, 2, [2, 3, 5, 7]),  # Проверка, если n > m
        (20, 30, [23, 29]),
        (1, 1, []),
        (0, 2, [2]),
        (-5, 10, [2, 3, 5, 7]),
        (100, 105, [101, 103]),
        (11, 11, [11]),
        (1, 20, [2, 3, 5, 7, 11, 13, 17, 19]),
    ],
)
def test_get_primes_in_range(n: int, m: int, expected: List[int]) -> None:
    assert get_primes_in_range(n, m) == expected
