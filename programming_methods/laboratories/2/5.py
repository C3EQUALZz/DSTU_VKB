"""
Задача №111728. Левый и правый двоичный поиск

Дано два списка чисел, числа в первом списке упорядочены по неубыванию.
Для каждого числа из второго списка определите номер первого и последнего появления этого числа в первом списке.

Входные данные

В первой строке входных данных записано два числа N и M (1≤N,M≤20000).
Во второй строке записано N упорядоченных по неубыванию целых чисел — элементы первого списка.
В третьей строке записаны M целых неотрицательных чисел - элементы второго списка.
Все числа в списках - целые 32-битные знаковые.

Выходные данные

Программа должна вывести M строчек.
Для каждого числа из второго списка нужно вывести номер его первого и последнего вхождения в первый список.
Нумерация начинается с единицы. Если число не входит в первый список, нужно вывести одно число 0.
"""

import bisect
from typing import List, Tuple, Sequence, Union
from collections import deque


def find_first_and_last_occurrences(
        sorted_list: Sequence[int],
        search_list: Sequence[int]
) -> deque[Union[Tuple[int, int], Tuple[int]]]:
    """
    Находит первое и последнее вхождение каждого числа из search_list в отсортированном списке sorted_list.
    Здесь задача заключается в том, чтобы

    :param sorted_list: Список целых чисел, отсортированный по неубыванию.
    :param search_list: Список целых чисел, для которых нужно найти вхождения в sorted_list.
    :return: Список кортежей, где каждый кортеж содержит индексы первого и последнего вхождения числа из search_list
     в sorted_list. Если число не найдено, возвращается кортеж (0,).
    """

    results: deque[Union[Tuple[int, int], Tuple[int]]] = deque()

    for number in search_list:
        first_index = bisect.bisect_left(sorted_list, number)

        if first_index >= len(sorted_list) or sorted_list[first_index] != number:
            results.append((0,))
        else:
            last_index = bisect.bisect_right(sorted_list, number) - 1
            results.append((first_index + 1, last_index + 1))  # +1 для единичной нумерации

    return results


def main() -> None:
    _, _ = map(int, input().split())
    sorted_list: List[int] = list(map(int, input().split()))
    search_list: List[int] = list(map(int, input().split()))

    occurrences = find_first_and_last_occurrences(sorted_list, search_list)

    for result in occurrences:
        print(*result)


if __name__ == "__main__":
    main()
