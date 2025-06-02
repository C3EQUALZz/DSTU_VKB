import pytest

from conditions.twenty_second.main import binary_to_decimal


# Тесты на корректные входы
@pytest.mark.parametrize(
    "binary_str, expected",
    [
        ("0", 0),
        ("1", 1),
        ("10", 2),
        ("11", 3),
        ("101", 5),
        ("1111", 15),
        ("0001", 1),
        ("1101", 13),
        ("0000", 0),
        ("100000", 32),
    ],
)
def test_binary_to_decimal_valid(binary_str, expected):
    assert binary_to_decimal(binary_str) == expected


# Тесты на некорректные входы
@pytest.mark.parametrize(
    "invalid_input",
    [
        "",
        "2",
        "12",
        "102",
        "abc",
        "1 0 1",
        "10a",
    ],
)
def test_binary_to_decimal_invalid(invalid_input):
    with pytest.raises(ValueError):
        binary_to_decimal(invalid_input)
