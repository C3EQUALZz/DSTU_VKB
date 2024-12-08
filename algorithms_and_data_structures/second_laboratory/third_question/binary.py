from typing import Sequence

from algorithms_and_data_structures.core.types import CT


def binary_search(search_list: Sequence[CT], search_value: CT) -> int:
    """
    Алгоритм бинарного поиска, который нужен для поиска значения.
    :param search_list: Последовательность, в которой мы будем делать поиск нашего значения.
    :param search_value: Значение, которое надо искать в последовательности.
    :returns: Индекс элемента, в ином случае -1, если не найден.
    """
    high, low, middle = len(search_list) - 1, 0, 0

    while low <= high and middle != search_value:
        middle = (low + high) // 2
        guess = search_list[middle]

        if guess == search_value:
            return middle
        elif guess > search_value:
            high = middle - 1
        else:
            low = middle + 1

    return -1
