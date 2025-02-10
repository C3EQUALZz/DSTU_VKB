# Объединить два отсортированных массива
from typing import List, TypeVar

T = TypeVar('T')

def merge_sorted_arrays(arr1: List[T], arr2: List[T]) -> List[T]:
    merged_array: List[T] = []
    i, j = 0, 0

    # Проходим по обоим массивам и добавляем меньший элемент в результирующий массив
    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            merged_array.append(arr1[i])
            i += 1
        else:
            merged_array.append(arr2[j])
            j += 1

    # Добавляем оставшиеся элементы из первого массива, если есть
    while i < len(arr1):
        merged_array.append(arr1[i])
        i += 1

    # Добавляем оставшиеся элементы из второго массива, если есть
    while j < len(arr2):
        merged_array.append(arr2[j])
        j += 1

    return merged_array

a = [1, 2, 3]
b = [4, 5, 6]
print(merge_sorted_arrays(a, b))