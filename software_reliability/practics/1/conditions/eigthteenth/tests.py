import pytest
from conditions.eigthteenth.main import replace_colons


@pytest.mark.parametrize(
    "s, pos, expected",
    [
        ("a:b:c", 2, "a:b.c"),  # Замена начиная с индекса 2
        ("a:b:c", 0, "a.b.c"),  # Замена с начала строки
        ("a:b:c", 10, "a:b:c"),  # Позиция за пределами строки
        (":::", 1, ":.."),  # Замена с середины строки
        ("no colons", 0, "no colons"),  # Нет двоеточий
        ("", 0, ""),  # Пустая строка
        (":a::b:", -1, ".a..b."),  # Отрицательная позиция
        (":a::b:", 5, ":a::b."),  # Позиция за пределами двоеточий
        ("::::", 0, "...."),  # Все символы — двоеточия
        ("abc:def:ghi", 4, "abc:def.ghi"),  # Замена только части строки
    ],
)
def test_replace_colons(s: str, pos: int, expected: str) -> None:
    assert replace_colons(s, pos) == expected
