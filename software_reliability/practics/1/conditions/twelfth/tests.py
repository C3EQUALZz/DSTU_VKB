from typing import List

import pytest

from conditions.twelfth.main import replace_min_abs


@pytest.mark.parametrize(
    "input_arr, expected",
    [
        ([4, -3, 2, 5], [2, -3, 2, 5]),  # Минимум по модулю: 2
        ([10, 1, -8, 3, 0], [0, 1, 0, 3, 0]),  # Минимум по модулю: 0
        ([], []),  # Пустой массив
        ([5], [5]),  # Один элемент
        ([3, -1, 2], [-1, -1, -1]),  # Минимум по модулю: -1
        ([-5, -4, -3, -2, -1], [-1, -4, -1, -2, -1]),  # Все отрицательные
        ([1, 2, 3, 4, 5], [1, 2, 1, 4, 1]),  # Минимум по модулю: 1
        ([100, 99, 98, 97], [97, 99, 97, 97]),  # Разные значения
    ],
)
def test_replace_min_abs(input_arr: List[int], expected: List[int]) -> None:
    assert replace_min_abs(input_arr) == expected
