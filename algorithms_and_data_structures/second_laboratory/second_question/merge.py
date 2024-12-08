from typing import List

from algorithms_and_data_structures.core.types import CT


def __merge(left: List[CT], right: List[CT]) -> List[CT]:
    """Сливает два отсортированных списка в один отсортированный список."""
    merged: List[CT] = []

    # Итерация по спискам left и right до тех пор, пока один из них не станет пустым
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Добавляем оставшиеся элементы, если они есть
    merged.extend(left[i:] + right[j:])

    return merged


def merge_sort(arr: List[CT]) -> List[CT]:
    """Сортирует массив с помощью алгоритма сортировки слиянием."""
    # Базовый случай
    if len(arr) <= 1:
        return arr

    # Рекурсивно делим массив на две половины
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    # Сливаем отсортированные половины
    return __merge(left_half, right_half)
