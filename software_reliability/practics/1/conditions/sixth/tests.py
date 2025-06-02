import pytest

from conditions.sixth.main import octal_to_decimal


@pytest.mark.parametrize(
    "octal_str, expected",
    [
        ("0", 0),
        ("1", 1),
        ("77", 63),
        ("12", 10),
        ("377", 255),
        ("00012", 10),  # ведущие нули
    ]
)
def test_valid_octal_inputs(octal_str: str, expected: int) -> None:
    """Проверяет корректные вводы."""
    assert octal_to_decimal(octal_str) == expected


@pytest.mark.parametrize(
    "invalid_input",
    [
        "",
        "8",
        "9",
        "18",
        "abc",
        " 12",
        "12 ",
    ]
)
def test_invalid_octal_inputs(invalid_input: str) -> None:
    """Проверяет некорректные вводы."""
    with pytest.raises(ValueError):
        octal_to_decimal(invalid_input)
