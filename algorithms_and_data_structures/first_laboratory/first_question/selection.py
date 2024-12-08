from typing import MutableSequence

from .base import CT


def selection_sort(lst: MutableSequence[CT]) -> MutableSequence[CT]:
    """
    Сортировка вставками.
    Сложность O(n^2)
    :param lst: Список элементов, содержащий элементы, которые могут сравниваться.
    :returns: Упорядоченный список по возрастанию.
    """
    for i in range(len(lst)):
        min_index: int = i
        for j in range(i + 1, len(lst)):
            if lst[j] < lst[min_index]:
                min_index = j
        lst[i], lst[min_index] = lst[min_index], lst[i]
    return lst
