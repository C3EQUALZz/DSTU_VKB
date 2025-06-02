import pytest

from conditions.eighth.main import trace, print_matrix, read_matrix


# ----------------------------
# Тесты для функции `trace`
# ----------------------------

@pytest.mark.parametrize(
    "matrix, expected",
    [
        ([[1, 2], [3, 4]], 5),  # 1 + 4 = 5
        ([[5, 0], [0, 5]], 10),  # 5 + 5 = 10
        ([[10]], 10),  # Матрица 1x1
        ([[0, 0, 0], [0, 0, 0], [0, 0, 0]], 0),  # Нулевая матрица
        ([[-1, 2], [3, -4]], -5),  # Отрицательные числа
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 15),  # 1 + 5 + 9 = 15
    ]
)
def test_trace(matrix, expected):
    assert trace(matrix) == expected


# ----------------------------
# Тесты для функции `print_matrix`
# ----------------------------

# Используем `capfd` для захвата вывода в консоль
def test_print_matrix(capfd):
    matrix = [[1, 2], [3, 4]]
    print_matrix(matrix)
    captured = capfd.readouterr()
    assert captured.out == "1 2\n3 4\n"


def test_print_matrix_single_element(capfd):
    matrix = [[42]]
    print_matrix(matrix)
    captured = capfd.readouterr()
    assert captured.out == "42\n"


def test_print_matrix_empty(capfd):
    matrix = []
    print_matrix(matrix)
    captured = capfd.readouterr()
    assert captured.out == ""  # Пустая матрица — ничего не выводится


# ----------------------------
# Тесты для функции `read_matrix`
# ----------------------------

# Используем `monkeypatch` для имитации ввода пользователя
def test_read_matrix_2x2(monkeypatch):
    inputs = ["1 2", "3 4"]
    monkeypatch.setattr('builtins.input', lambda: inputs.pop(0))
    assert read_matrix(2) == [[1, 2], [3, 4]]


def test_read_matrix_1x1(monkeypatch):
    inputs = ["5"]
    monkeypatch.setattr('builtins.input', lambda: inputs.pop(0))
    assert read_matrix(1) == [[5]]


def test_read_matrix_3x3(monkeypatch):
    inputs = ["1 2 3", "4 5 6", "7 8 9"]
    monkeypatch.setattr('builtins.input', lambda: inputs.pop(0))
    assert read_matrix(3) == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


# ----------------------------
# Тесты на обработку ошибок
# ----------------------------

def test_read_matrix_invalid_input(monkeypatch):
    inputs = ["1 a", "3 4"]  # Некорректная строка
    monkeypatch.setattr('builtins.input', lambda: inputs.pop(0))
    with pytest.raises(ValueError):
        read_matrix(2)
