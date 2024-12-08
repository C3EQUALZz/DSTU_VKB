from typing import MutableSequence

from .base import CT


def insertion_sort(lst: MutableSequence[CT]) -> MutableSequence[CT]:
    """
    Сортировка вставками.
    Сложность O(n^2)
    :param lst: Список элементов, содержащий элементы, которые могут сравниваться.
    :returns: Упорядоченный список по возрастанию.
    """
    for i in range(1, len(lst)):
        for j in range(i, 0, -1):
            if lst[j] < lst[j - 1]:
                lst[j], lst[j - 1] = lst[j - 1], lst[j]
            else:
                break
    return lst
