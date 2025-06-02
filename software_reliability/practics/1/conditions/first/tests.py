import pytest

from conditions.first.main import reverse


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("hello", "olleh"),
        ("", ""),
        ("hello world", "dlrow olleh"),
        ("12345!@#", "#@!54321"),
        ("a", "a"),
        ("ab", "ba"),
        ("привет", "тевирп"),
        ("😊🚀", "🚀😊"),
    ],
)
def test_reverse(input_str: str, expected: str) -> None:
    """
    Проверяет, что функция reverse корректно переворачивает строку.
    """
    assert reverse(input_str) == expected
