import pytest
from conditions.twenty_first.main import max_row_sum_index


# Тесты с корректными данными
@pytest.mark.parametrize(
    "matrix, expected",
    [
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2),  # Последняя строка имеет наибольшую сумму
        ([[10, 20], [30, 40], [50, 60]], 2),  # Последняя строка
        ([[1, 0], [0, 1], [1, 1]], 2),  # Первая и третья строки равны
        ([[-1, -2], [-3, -4], [-5, -6]], 0),  # Все отрицательные
        ([[5]], 0),  # Матрица 1x1
        ([[1, 2], [3, 0], [2, 2]], 2),  # Первая строка
    ],
)
def test_max_row_sum_index_valid(matrix, expected):
    assert max_row_sum_index(matrix) == expected


# Тесты на обработку ошибок
def test_max_row_sum_index_empty_matrix():
    with pytest.raises(ValueError):
        max_row_sum_index([])


def test_max_row_sum_index_empty_row():
    with pytest.raises(ValueError):
        max_row_sum_index([[1, 2], [], [3, 4]])


def test_max_row_sum_index_invalid_input():
    with pytest.raises(TypeError):
        max_row_sum_index("not a matrix")


def test_max_row_sum_index_non_rectangular_matrix():
    with pytest.raises(ValueError):
        max_row_sum_index([[1, 2], [3, 4, 5], [6, 7]])  # Разное количество элементов в строках
