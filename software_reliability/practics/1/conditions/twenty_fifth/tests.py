import pytest

from conditions.twenty_fifth.main import hex_to_decimal


# Тесты на корректные значения
@pytest.mark.parametrize(
    "hex_str, expected",
    [
        ("0", 0),
        ("1", 1),
        ("A", 10),
        ("F", 15),
        ("FF", 255),
        ("1A", 26),
        ("10", 16),
        ("ABC", 2748),
        ("abcdef", 11259375),
        ("123456", 1193046),
        ("0000", 0),
        ("FFFFFFFF", 4294967295),
        ("aBcDeF", 11259375),
    ],
)
def test_hex_to_decimal_valid(hex_str: str, expected: int) -> None:
    assert hex_to_decimal(hex_str) == expected


# Тесты на некорректные значения
@pytest.mark.parametrize(
    "invalid_input",
    [
        "",
        "G",
        "1Z",
        "XYZ",
        "123G",
        "12 34",
        "12-34",
        "12.34",
        "abcdx",
    ],
)
def test_hex_to_decimal_invalid(invalid_input: str) -> None:
    with pytest.raises(ValueError):
        hex_to_decimal(invalid_input)
