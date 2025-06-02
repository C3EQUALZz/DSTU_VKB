import pytest
from typing import List
from conditions.thirteenth.main import sum_row


# Корректные входные данные
@pytest.mark.parametrize(
    "matrix, j, expected",
    [
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 0, 6),
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1, 15),
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 24),
        ([[10]], 0, 10),
        ([[-1, -2], [-3, -4]], 1, -7),
        ([[0, 0], [0, 0]], 0, 0),
    ]
)
def test_sum_row_valid(matrix: List[List[int]], j: int, expected: int) -> None:
    assert sum_row(matrix, j) == expected


# Неверный индекс строки
def test_sum_row_index_out_of_bounds() -> None:
    with pytest.raises(IndexError):
        sum_row([[1, 2], [3, 4]], 2)


# Отрицательный индекс
def test_sum_row_negative_index() -> None:
    with pytest.raises(IndexError):
        sum_row([[1, 2], [3, 4]], -1)


# Пустая матрица
def test_sum_row_empty_matrix() -> None:
    with pytest.raises(ValueError):
        sum_row([], 0)
