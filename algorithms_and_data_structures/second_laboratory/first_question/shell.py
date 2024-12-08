from typing import List

from algorithms_and_data_structures.core.types import CT


def shell_sort(lst: List[CT]) -> List[CT]:
    """
    Сортировка Шелла.
    Сложность варьируется от O(n^2) до O(n*log(n)).
    :param lst: Список, содержащий элементы, поддерживающие сравнение.
    :returns: Упорядоченный список по возрастанию.
    """
    move = len(lst) // 2
    while move > 0:
        for i in range(len(lst) - move):
            if lst[i] > lst[i + move]:
                lst[i], lst[i + move] = lst[i + move], lst[i]
        move //= 2
    return lst
