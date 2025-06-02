import pytest
from conditions.twentieth.main import area_triangle


# Тесты на корректные значения
@pytest.mark.parametrize(
    "a, b, c, expected",
    [
        ((0, 0), (4, 0), (0, 3), 6.0),  # Прямоугольный треугольник
        ((0, 0), (2, 0), (1, 2), 2.0),  # Произвольный треугольник
        ((0, 0), (0, 0), (0, 0), 0.0),  # Вырожденный треугольник
        ((1, 1), (3, 4), (5, 2), 5.0),  # Треугольник с целыми координатами
        ((0, 0), (0, 5), (5, 0), 12.5),  # Прямоугольный треугольник (катеты 5)
        ((2, 2), (4, 2), (3, 5), 3.0),  # Треугольник с дробными координатами
    ],
)
def test_area_triangle_valid(a, b, c, expected):
    assert abs(area_triangle(a, b, c) - expected) < 1e-6


# Тесты на вырожденные случаи
def test_area_triangle_degenerate():
    assert area_triangle((0, 0), (1, 1), (2, 2)) == 0.0  # Все точки на одной прямой
    assert area_triangle((5, 5), (5, 5), (5, 5)) == 0.0  # Все точки совпадают


# Тесты на некорректные входные данные
def test_area_triangle_invalid_inputs():
    with pytest.raises(TypeError):
        area_triangle((0, 0), (4, 0), (0, "3"))  # Некорректный тип
    with pytest.raises(ValueError):
        area_triangle((0, 0), (4, 0), (0,))  # Недостаток координат
    with pytest.raises(ValueError):
        area_triangle((0, 0, 0), (4, 0), (0, 3))  # Слишком много координат
