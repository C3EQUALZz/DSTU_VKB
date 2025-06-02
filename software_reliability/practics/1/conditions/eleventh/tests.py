import pytest

from conditions.eleventh.main import count_char


@pytest.mark.parametrize(
    "input_str, char, expected",
    [
        ("hello world", "l", 3),
        ("абракадабра", "а", 5),
        ("test", "x", 0),
        ("", "a", 0),
        ("aaaaa", "a", 5),
        ("caseSensitive", "S", 1),
        ("caseSensitive", "s", 2),
        ("  пробелы  ", " ", 4),
    ],
)
def test_count_char(input_str: str, char: str, expected: int) -> None:
    assert count_char(input_str, char) == expected


def test_count_char_invalid_char_length():
    with pytest.raises(ValueError):
        count_char("hello", "")


def test_count_char_invalid_char_multiple():
    with pytest.raises(ValueError):
        count_char("hello", "ab")
