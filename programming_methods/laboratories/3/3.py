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
