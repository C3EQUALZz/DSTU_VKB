from typing import List

import pytest

from conditions.sixteenth.main import count_positive


@pytest.mark.parametrize(
    "input_arr, expected",
    [
        ([1, 2, 3], 3),  # Все положительные
        ([-1, -2, -3], 0),  # Все отрицательные
        ([0, 0, 0], 0),  # Только нули
        ([1, -2, 0, 3], 2),  # Смешанные значения
        ([5], 1),  # Один элемент
        ([], 0),  # Пустой массив
        ([100, -50, 25, -25], 2),  # Разные числа
        ([0, -1, 2, -3, 4], 2),  # С нулями
        ([1, 1, 1, 1], 4),  # Все одинаковые положительные
    ],
)
def test_count_positive(input_arr: List[int], expected: int) -> None:
    assert count_positive(input_arr) == expected
