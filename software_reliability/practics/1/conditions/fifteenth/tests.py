import pytest

from conditions.fifteenth.main import extract_digits


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("a1b2c3", "123"),
        ("abc", ""),
        ("123", "123"),
        ("", ""),
        ("!@#1a9Z", "19"),
        ("12a34b56", "123456"),
        ("0a0b0c", "000"),
        ("ABC123XYZ", "123"),
        ("12 34 56", "123456"),  # Пробелы игнорируются
        ("Привет123Мир", "123"),
    ],
)
def test_extract_digits(input_str: str, expected: str) -> None:
    assert extract_digits(input_str) == expected
