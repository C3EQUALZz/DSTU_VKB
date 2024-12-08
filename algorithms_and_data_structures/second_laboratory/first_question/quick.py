from random import randint
from typing import List

from algorithms_and_data_structures.core.types import CT


def quick_sort(lst: List[CT]) -> List[CT]:
    """
    Быстрая сортировка (сортировка Хоара)
    Сложность O(n * log(n))
    :param lst: Список, содержащий элементы, поддерживающие сравнение.
    :returns: Упорядоченный список по возрастанию.
    """
    if len(lst) > 1:
        x = lst[randint(0, len(lst) - 1)]
        low = [l for l in lst if l < x]
        eq = [l for l in lst if l == x]
        high = [l for l in lst if l > x]
        return quick_sort(low) + eq + quick_sort(high)
    return lst
