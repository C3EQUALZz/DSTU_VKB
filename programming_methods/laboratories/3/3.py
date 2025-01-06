"""
Задача №1794. Наибольшая возрастающая подпоследовательность за O(n*log(n)) с восстановлением ответа

Числовая последовательность задана рекуррентной формулой: ai+1=(k∗ai+b)mod m.
Найдите её наибольшую возрастающую подпоследовательность.

Входные данные

Программа получает на вход пять целых чисел: длину последовательности n(1≤n≤10^5),
начальный элемент последовательности a1, параметры k, b, m для вычисления последующих членов
последовательности (1≤m≤10^4, 0≤k<m, 0≤b<m, 0≤a1<m).

Выходные данные

Требуется вывести наибольшую возрастающую подпоследовательность данной последовательности, разделяя числа пробелами.
Если таких последовательностей несколько, необходимо вывести одну (любую) из них.
"""

from bisect import bisect_left
from typing import List


def longest_increasing_subsequence(sequence: List[int]) -> List[int]:
    """Находит наибольшую возрастающую подпоследовательность."""

    # Массив для хранения наибольшей возрастающей подпоследовательности
    lis = []
    # Массив для восстановления последовательности
    prev_index = [-1] * len(sequence)
    indices = []

    for i, value in enumerate(sequence):
        pos = bisect_left(lis, value)

        # Если значение больше всех элементов в lis, добавляем его
        if pos == len(lis):
            lis.append(value)
            indices.append(i)
        else:
            lis[pos] = value
            indices[pos] = i

        # Восстанавливаем индексы
        if pos > 0:
            prev_index[i] = indices[pos - 1]

    # Восстанавливаем саму последовательность
    result = []
    k = indices[-1]
    while k != -1:
        result.append(sequence[k])
        k = prev_index[k]

    return result[::-1]  # Возвращаем в правильном порядке


def main() -> None:
    n, a1, k, b, m = map(int, input().split())

    # Генерируем последовательность
    sequence = [0] * n
    sequence[0] = a1
    for i in range(1, n):
        sequence[i] = (k * sequence[i - 1] + b) % m

    # Находим наибольшую возрастающую подпоследовательность
    lis = longest_increasing_subsequence(sequence)

    # Выводим результат
    print(" ".join(map(str, lis)))


if __name__ == "__main__":
    main()
