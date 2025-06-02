import math

from conditions.ninth.main import calculate_series


# ----------------------------
# Тест 1: n > m → сумма равна 0
# ----------------------------
def test_empty_range():
    assert calculate_series(5, 3, 2) == 0.0


# ----------------------------
# Тест 2: Одно слагаемое (n = m)
# ----------------------------
def test_single_term():
    result = calculate_series(2, 1, 1)
    expected = (2 ** 2) / math.factorial(2)
    assert result == expected


# ----------------------------
# Тест 3: Множество слагаемых
# ----------------------------
def test_multiple_terms():
    result = calculate_series(1, 0, 2)
    expected = 1 + (1 ** 2) / math.factorial(2) + (1 ** 4) / math.factorial(4)
    assert abs(result - expected) < 1e-9  # Учет погрешности округления


# ----------------------------
# Тест 4: x = 0 → все слагаемые равны 0
# ----------------------------
def test_zero_x():
    result = calculate_series(0, 0, 5)
    assert result == 1.0


# ----------------------------
# Тест 5: Приближение к cosh(x)
# ----------------------------
def test_approximation_to_cosh():
    x = 1.0
    m = 10
    result = calculate_series(x, 0, m)
    expected = math.cosh(x)  # Косинус гиперболический — сумма ряда до бесконечности
    assert abs(result - expected) < 1e-5
