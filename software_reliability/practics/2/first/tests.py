import pytest
from octal_converter import octal_to_decimal


# Тесты для корректных значений
def test_valid_octal_strings():
    assert octal_to_decimal('12') == 10
    assert octal_to_decimal('0o12') == 10
    assert octal_to_decimal('0O12') == 10
    assert octal_to_decimal('0') == 0
    assert octal_to_decimal('0o0') == 0
    assert octal_to_decimal('777') == 511
    assert octal_to_decimal('0o755') == 493
    assert octal_to_decimal('10') == 8
    assert octal_to_decimal('100') == 64


# Тесты для пустых строк
def test_empty_string():
    assert octal_to_decimal('') == 0
    assert octal_to_decimal('0o') == 0


# Тесты для некорректных значений
def test_invalid_strings():
    with pytest.raises(ValueError):
        octal_to_decimal('8')  # Недопустимая цифра

    with pytest.raises(ValueError):
        octal_to_decimal('0o89')  # Недопустимая цифра

    with pytest.raises(ValueError):
        octal_to_decimal('12a')  # Недопустимый символ

    with pytest.raises(ValueError):
        octal_to_decimal('0o12!')  # Недопустимый символ