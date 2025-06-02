import pytest

from conditions.twenty_fourth.main import matrix_operation


# --- Тесты на корректные данные ---

@pytest.mark.parametrize(
    "a, b, operation, expected",
    [
        # a              # b             # operation # expected
        ([[1, 2], [3, 4]], [[3, 4], [5, 6]], "add", [[4, 6], [8, 10]]),
        ([[5, 6], [3, 4]], [[3, 4], [1, 0]], "subtract", [[2, 2], [2, 4]]),
        ([[1, 2, 3], [4, 5, 6]], [[4, 5, 6], [7, 8, 9]], "add", [[5, 7, 9], [11, 13, 15]]),
        ([[10, 20], [5, 10]], [[5, 10], [0, 5]], "subtract", [[5, 10], [5, 5]]),
        ([[1, 0], [0, 1]], [[0, 1], [1, 0]], "add", [[1, 1], [1, 1]]),
        ([[1.5, 2.5], [3.5, 4.5]], [[2.5, 0.0], [0.0, 0.5]], "add", [[4.0, 2.5], [3.5, 5.0]]),
        ([[5, 6, 7], [1, 2, 3]], [[1, 2, 3], [4, 5, 6]], "subtract", [[4, 4, 4], [-3, -3, -3]]),
        ([[1, 2], [3, 4]], [[3, 4], [5, 6]], "subtract", [[-2, -2], [-2, -2]]),
        ([[10, 20], [30, 40]], [[1, 2], [3, 4]], "add", [[11, 22], [33, 44]]),
        ([[100, 200], [300, 400]], [[10, 20], [30, 40]], "subtract", [[90, 180], [270, 360]]),
    ],
)
def test_matrix_operation_valid(a, b, operation, expected):
    assert matrix_operation(a, b, operation) == expected


# --- Тесты на ошибки ---

def test_matrix_operation_invalid_operation():
    with pytest.raises(ValueError):
        matrix_operation([[1, 2], [3, 4]], [[5, 6], [7, 8]], "multiply")


def test_matrix_operation_mismatched_rows():
    with pytest.raises(TypeError):
        matrix_operation([[1, 2], [3, 4]], [[5]][[6]], "add")


def test_matrix_operation_mismatched_columns():
    with pytest.raises(ValueError):
        matrix_operation([[1, 2], [3, 4]], [[5, 6, 7], [8, 9, 10]], "add")


def test_matrix_operation_empty_a():
    with pytest.raises(ValueError):
        matrix_operation([], [[1, 2], [3, 4]], "add")


def test_matrix_operation_empty_b():
    with pytest.raises(ValueError):
        matrix_operation([[1, 2], [3, 4]], [], "add")


def test_matrix_operation_invalid_operation_type():
    with pytest.raises(ValueError):
        matrix_operation([[1, 2], [3, 4]], [[5, 6], [7, 8]], "invalid")
