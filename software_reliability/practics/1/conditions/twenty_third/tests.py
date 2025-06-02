import pytest

from conditions.twenty_third.main import replace_second_chars


# Тесты на корректные входные данные
@pytest.mark.parametrize(
    "s, char, expected",
    [
        ("abcdef", "*", "a*c*e*"),
        ("a", "*", "a"),
        ("", "*", ""),
        ("hello world", "x", "hxlxoxwxrxd"),
        ("123456789", "#", "1#3#5#7#9"),
        ("abcdefghij", "Z", "aZcZeZgZiZ"),
        ("ab", "X", "aX"),
        ("abcde", "-", "a-c-e"),
    ],
)
def test_replace_second_chars_valid(s: str, char: str, expected: str) -> None:
    assert replace_second_chars(s, char) == expected


# Тесты на обработку ошибок
def test_replace_second_chars_invalid_char_length():
    with pytest.raises(ValueError):
        replace_second_chars("test", "")


def test_replace_second_chars_invalid_char_long():
    with pytest.raises(ValueError):
        replace_second_chars("test", "ab")


def test_replace_second_chars_invalid_char_not_str():
    with pytest.raises(ValueError):
        replace_second_chars("test", 123)  # тип не строка
