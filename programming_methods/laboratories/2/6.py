"""
Задача №1664. Суперсумма

Дано N натуральных чисел.
Требуется для каждого числа найти количество вариантов разбиения его на сумму двух других чисел из данного набора.

Входные данные

В первой строке дано число N (1 ≤ N ≤ 10000). Далее заданы N натуральных чисел, не превосходящих 10^9.
Для каждого числа количество разбиений меньше 2^31.

Выходные данные

Вывести N чисел – количество разбиений, в порядке, соответствующем исходному.
"""
from collections import Counter
from typing import List, Generator


def count_partitions(numbers: List[int]) -> Generator[int, None, None]:
    count_map = Counter(numbers)  # Подсчитываем количество каждого числа

    for number in numbers:
        count = sum(
            count_map[x] * (count_map[x] - 1) // 2 if x == (number - x) else count_map[x] * count_map.get(number - x, 0)
            for x in count_map
            if x <= number // 2  # Условие для x, чтобы избежать дублирования
        )
        yield count


def main():
    n = int(input())
    numbers = [int(input()) for _ in range(n)]

    partitions = count_partitions(numbers)

    for result in partitions:
        print(result)


if __name__ == "__main__":
    main()
