"""
Задача №1792. НВП с восстановлением ответа

Дана последовательность, требуется найти её наибольшую возрастающую подпоследовательность.

Входные данные

В первой строке входных данных задано число N- длина последовательности (1 ≤ N≤ 1000).
Во второй строке задается сама последовательность (разделитель - пробел).
Элементы последовательности - целые числа, не превосходящие 10000 по модулю.

Выходные данные

Требуется вывести наибольшую возрастающую подпоследовательность данной последовательности.
Если таких подпоследовательностей несколько, необходимо вывести одну (любую) из них.
"""
from typing import List


def longest_increasing_subsequence(sequence: List[int]) -> List[int]:
    """Находит наибольшую возрастающую подпоследовательность."""
    n = len(sequence)
    dp = [1] * n  # Массив для хранения длины LIS до каждого элемента
    prev_index = [-1] * n  # Массив для восстановления последовательности

    # Заполняем массив dp
    for i in range(n):
        for j in range(i):
            if sequence[j] < sequence[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev_index[i] = j

    # Находим максимальную длину и индекс последнего элемента LCS
    max_length = max(dp)
    max_index = dp.index(max_length)

    # Восстанавливаем саму последовательность
    lis = []
    while max_index != -1:
        lis.append(sequence[max_index])
        max_index = prev_index[max_index]

    return lis[::-1]  # Возвращаем в правильном порядке


def main() -> None:
    _ = int(input())
    sequence = list(map(int, input().split()))

    lis = longest_increasing_subsequence(sequence)

    # Выводим результат
    print(' '.join(map(str, lis)))


if __name__ == "__main__":
    main()
