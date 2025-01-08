"""
Задача №3310. Индекс максимума на подотрезках

Реализуйте структуру данных для эффективного вычисления номера максимального из нескольких подряд идущих элементов массива.

Входные данные

В первой строке вводится одно натуральное число N (1≤N≤100000) — количество чисел в массиве.

Во второй строке вводятся N чисел от 1 до 100000 — элементы массива.

В третьей строке вводится одно натуральное число K (1≤K≤30000) — количество запросов на вычисление максимума.

В следующих K строках вводится по два числа — номера левого и правого элементов отрезка массива
(считается, что элементы массива нумеруются с единицы).

Выходные данные

Для каждого запроса выведите индекс максимального элемента на указанном отрезке массива.
Если максимальных элементов несколько, выведите любой их них.

Числа выводите в одну строку через пробел.
"""
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class ArrayElement:
    value: int
    index: int


def build_sparse_table(array: List[int]) -> Tuple[List[List[ArrayElement]], List[int]]:
    n = len(array)
    log_values = [0] * (n + 1)

    # Precompute logarithms
    for i in range(2, n + 1):
        log_values[i] = log_values[i // 2] + 1

    k = log_values[n] + 1
    sparse_table = [[ArrayElement(0, 0)] * k for _ in range(n)]

    # Initialize the sparse table
    for i in range(n):
        sparse_table[i][0] = ArrayElement(array[i], i)

    # Fill the sparse table
    for j in range(1, k):
        for i in range(n - (1 << j) + 1):
            if sparse_table[i][j - 1].value >= sparse_table[i + (1 << (j - 1))][j - 1].value:
                sparse_table[i][j] = sparse_table[i][j - 1]
            else:
                sparse_table[i][j] = sparse_table[i + (1 << (j - 1))][j - 1]

    return sparse_table, log_values


def query_max(sparse_table: List[List[ArrayElement]], log_values: List[int], left: int, right: int) -> ArrayElement:
    j = log_values[right - left + 1]
    left_max = sparse_table[left][j]
    right_max = sparse_table[right - (1 << j) + 1][j]
    return left_max if left_max.value >= right_max.value else right_max


def main() -> None:
    _ = int(input())
    array = list(map(int, input().split()))
    query_count = int(input())

    sparse_table, log_values = build_sparse_table(array)

    results = []
    for _ in range(query_count):
        left, right = map(int, input().split())
        left -= 1  # Convert to 0-based index
        right -= 1
        max_index = query_max(sparse_table, log_values, left, right).index + 1  # Convert back to 1-based index
        results.append(max_index)

    print(' '.join(map(str, results)))


if __name__ == "__main__":
    main()
