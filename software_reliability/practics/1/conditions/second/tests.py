import pytest

from conditions.second.main import reverse_number


@pytest.mark.parametrize("input_num, expected", [
    # Обычные числа
    (123, 321),
    (100, 1),
    (5, 5),
    (1200, 21),
    (987654321, 123456789),

    # Граничные значения
    (1, 1),
    (10, 1),
    (999, 999),
    (100000000, 1),

    # Числа с нечетным количеством цифр
    (12345, 54321),
    (101, 101),

    # Числа с повторяющимися цифрами
    (111, 111),
    (121, 121),
    (112233, 332211),
])
def test_reverse_number_valid(input_num, expected):
    """Тестирование корректных натуральных чисел"""
    assert reverse_number(input_num) == expected


# Тесты для недопустимых значений
@pytest.mark.parametrize("invalid_input", [
    -5,  # Отрицательные числа
    0,  # Ноль
    -100,  # Большое отрицательное
    -1,  # Граничное отрицательное
])
def test_reverse_number_invalid(invalid_input):
    """Тестирование обработки недопустимых значений"""
    with pytest.raises(ValueError) as exc_info:
        reverse_number(invalid_input)
    assert "натуральное число" in str(exc_info.value).lower()


# Тесты для проверки типа данных
@pytest.mark.parametrize("non_integer", [
    12.5,  # Float
    "123",  # String
    [123],  # List
    None,  # None
    True,  # Boolean
])
def test_reverse_number_type_error(non_integer):
    """Тестирование обработки нецелочисленных значений"""
    with pytest.raises(TypeError):
        reverse_number(non_integer)
