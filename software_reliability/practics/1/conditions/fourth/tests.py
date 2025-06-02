import pytest

from conditions.fourth.main import combinations


# Параметризованные тесты для корректных значений
@pytest.mark.parametrize("n, k, expected", [
    # Базовые случаи
    (0, 0, 1),  # C(0,0) = 1
    (5, 0, 1),  # C(5,0) = 1
    (5, 5, 1),  # C(5,5) = 1
    (7, 2, 21),  # C(7,2) = 21

    # Свойство симметрии
    (10, 3, 120),  # C(10,3) = 120
    (10, 7, 120),  # C(10,7) = 120 (симметрия)

    # Большие числа
    (20, 10, 184756),
    (15, 7, 6435),

    # Граничные случаи
    (1, 0, 1),
    (1, 1, 1),
    (2, 1, 2),
])
def test_combinations_valid(n: int, k: int, expected: int) -> None:
    assert combinations(n, k) == expected


# Тесты для недопустимых значений
@pytest.mark.parametrize("n, k", [
    (-1, 5),  # Отрицательное n
    (5, -1),  # Отрицательное k
    (-5, -2),  # Оба отрицательные
])
def test_combinations_negative(n: int, k: int) -> None:
    with pytest.raises(ValueError) as exc_info:
        combinations(n, k)
    assert "неотрицательными" in str(exc_info.value)


# Тесты для случаев k > n
@pytest.mark.parametrize("n, k", [
    (5, 6),  # k > n
    (0, 1),  # k > n (для n=0)
    (3, 10),  # k значительно больше n
])
def test_combinations_k_greater_than_n(n: int, k: int) -> None:
    assert combinations(n, k) == 0


# Тесты для больших значений (проверка переполнения)
def test_large_values():
    assert combinations(100, 50) == 100891344545564193334812497256
    assert combinations(1000, 1) == 1000
    assert combinations(1000, 999) == 1000  # Симметрия
