from typing import MutableSequence

from algorithms_and_data_structures.core.types import CT


def bubble_sort(lst: MutableSequence[CT]) -> MutableSequence[CT]:
    """
    Сортировка пузырьком.
    Сложность O(n^2)
    :param lst: Список, содержащий элементы, поддерживающие сравнение.
    :returns: Упорядоченный список по возрастанию.
    """
    for i in range(len(lst) - 1):
        flag: bool = True
        for j in range(len(lst) - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                flag = False
        if flag:
            break
    return lst
