"""Регрессионные и граничные проверки, обнаруживающие пропуск элемента."""

import pytest

from average import average
from average_legacy import average as legacy_average


def test_regression_includes_last_element():
    assert average([10, 20, 30, 40]) == 25.0


def test_legacy_reproduces_missing_last_element():
    assert legacy_average([10, 20, 30, 40]) == 15.0


@pytest.mark.parametrize(("values", "expected"), [
    ([40], 40.0), ([10, 30], 20.0), ([0, 0, 90], 30.0),
    ([-10, -20, -30], -20.0), ([-10, 10], 0.0),
    ([1.5, 2.5], 2.0), ([0, 0, 0], 0.0), ([2, 2, 2], 2.0),
])
def test_average_cases(values, expected):
    assert average(values) == pytest.approx(expected)


def test_empty_list_is_rejected():
    with pytest.raises(ValueError, match="Список"):
        average([])


def test_input_is_not_modified():
    values = [10, 20, 30, 40]
    average(values)
    assert values == [10, 20, 30, 40]
