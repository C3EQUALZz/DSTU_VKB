import pytest

from .main import count_min_in_rows


def test_normal_matrix():
    matrix = [
        [1, 2, 3],
        [4, 0, 4],
        [5, 5, 5],
        [-1, 2, -1]
    ]
    assert count_min_in_rows(matrix) == [1, 1, 3, 2]


def test_single_element_rows():
    matrix = [[5], [-3], [0]]
    assert count_min_in_rows(matrix) == [1, 1, 1]


def test_negative_numbers():
    matrix = [
        [-5, -10, -5],
        [-2, -2, -2],
        [0, -1, -1]
    ]
    assert count_min_in_rows(matrix) == [1, 3, 2]


def test_duplicate_min_values():
    matrix = [
        [1, 1, 1, 1],
        [2, 2, 1, 1],
        [3, 1, 1, 2]
    ]
    assert count_min_in_rows(matrix) == [4, 2, 2]


def test_empty_matrix():
    with pytest.raises(ValueError) as exc_info:
        count_min_in_rows([])
    assert "Матрица пустая" in str(exc_info.value)


def test_matrix_with_empty_rows():
    with pytest.raises(ValueError) as exc_info:
        count_min_in_rows([[], [1, 2], []])
    assert "Матрица содержит пустые строки" in str(exc_info.value)


def test_irregular_matrix():
    with pytest.raises(ValueError):
        # Неправильная матрица (разные длины строк)
        count_min_in_rows([[1, 2], [3], [4, 5, 6]])
