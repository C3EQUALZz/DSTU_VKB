from typing import Tuple

import pytest

from conditions.fourteenth.main import count_digits_and_sum


@pytest.mark.parametrize(
    "number, expected",
    [
        (1234, (4, 10)),
        (5, (1, 5)),
        (999, (3, 27)),
        (1001, (4, 2)),
        (1, (1, 1)),
        (987654321, (9, 45)),
    ],
)
def test_count_digits_and_sum_valid(number: int, expected: Tuple[int, int]) -> None:
    assert count_digits_and_sum(number) == expected


def test_count_digits_and_sum_zero():
    with pytest.raises(ValueError):
        count_digits_and_sum(0)


def test_count_digits_and_sum_negative():
    with pytest.raises(ValueError):
        count_digits_and_sum(-123)


def test_count_digits_and_sum_non_integer():
    with pytest.raises(ValueError):
        count_digits_and_sum(123.45)
