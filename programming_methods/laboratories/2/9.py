"""
Задача №8. Банковские карты

Банк «Кисловодск» переходит на новый вид банковских карт. Для этого производятся одинаковые заготовки,
на которых есть специальное место для идентификации клиента. Изначально на этом месте записывается кодовое число X.
В банке с помощью специального прибора можно стирать некоторые цифры числа X.
Оставшиеся цифры, будучи записанными подряд, должны образовывать номер счета клиента.
Например, при X = 12013456789 номера счетов 5, 12, 17 или 12013456789 получить можно, а номера 22 или 71 получить нельзя.

Способ распределения номеров счетов в банке очень прост.
Счетам присваиваются последовательно номера 1, 2, …
Очевидно, что при таком способе в какой-то момент впервые найдется номер счета N,
который нельзя будет получить из цифр X указанным выше способом. Руководство банка хочет знать значение N.

Напишите программу, которая находила бы N по заданному X.

Входные данные

Вводится натуральное число X без ведущих нулей (1 ≤ X < 101000)

Выходные данные

Выведите искомое N без ведущих нулей.

ОДНО ИЗ ВОЗМОЖНЫХ РЕШЕНИЙ, НО НЕ ПРОХОДИТ ПО СКОРОСТЯМ.
"""
from bisect import bisect_right
from collections import defaultdict


def build_index(x: str) -> defaultdict:
    """Строит индекс для быстрого доступа к символам в строке."""
    index = defaultdict(list)
    for i, c in enumerate(x):
        index[c].append(i)
    return index


def can_form_number(n: str, index: defaultdict) -> bool:
    """Проверяет, можно ли построить число n из X с использованием индекса."""
    current_pos = -1
    for c in n:
        if c not in index:
            return False
        # Находим первую позицию символа c, которая больше current_pos с помощью bisect
        positions = index[c]
        i = bisect_right(positions, current_pos)
        if i == len(positions):
            return False
        current_pos = positions[i]
    return True


def find_missing_account_number(x: str) -> int:
    """Находит первое число N, которого нельзя получить из цифр X."""
    index = build_index(x)
    n = 1
    while True:
        if not can_form_number(str(n), index):
            return n
        n += 1


def main() -> None:
    x = input().strip()
    result = find_missing_account_number(x)
    print(result)


if __name__ == "__main__":
    main()
