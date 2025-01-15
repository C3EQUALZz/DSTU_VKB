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
    """
    Мысли страшное творят в час ночи, зачем я для этого датакласс решить сделал....
    """
    value: int
    index: int


def build_sparse_table(array: List[int]) -> Tuple[List[List[ArrayElement]], List[int]]:
    """
    Создает разреженную таблицу для эффективного поиска максимума на подотрезках массива.

    Алгоритм работы:
        1. Создается массив логарифмов для быстрого вычисления степеней двойки.
        2. Строится разреженная таблица, где каждый элемент хранит значение максимума и его индекс
           для всех подотрезков массива длиной 2^k, начиная с k=0 (по сути, для каждого элемента в массиве).
        3. Затем таблица заполняется для всех более длинных подотрезков (длина 2^k), используя уже вычисленные максимумы для меньших подотрезков.

    :param array: Входной массив целых чисел.
    :returns: Кортеж, где первый элемент - разреженная таблица, где каждый элемент представляет собой максимальное
     значение и его индекс для подотрезков. Второй элемент - массив логарифмов для быстрого доступа к значениям.
    """
    n: int = len(array)
    log_values: List[int] = [0] * (n + 1)

    # Предварительное вычисление логарифмов
    for i in range(2, n + 1):
        log_values[i] = log_values[i // 2] + 1

    max_power_of_two: int = log_values[n] + 1
    sparse_table: List[List[ArrayElement]] = [[ArrayElement(0, 0)] * max_power_of_two for _ in range(n)]

    # Инициализация разреженной таблицы
    for i in range(n):
        sparse_table[i][0] = ArrayElement(array[i], i)

    # Строим таблицу для отрезков длиной 2^j
    for j in range(1, max_power_of_two):
        for i in range(n - (1 << j) + 1): # (1 << j) = 2^j
            if sparse_table[i][j - 1].value >= sparse_table[i + (1 << (j - 1))][j - 1].value:
                sparse_table[i][j] = sparse_table[i][j - 1]
            else:
                sparse_table[i][j] = sparse_table[i + (1 << (j - 1))][j - 1]

    return sparse_table, log_values


def query_max(sparse_table: List[List[ArrayElement]], log_values: List[int], left: int, right: int) -> int:
    """
    Находит индекс максимального элемента на подотрезке массива.

    Алгоритм:
        1. Используем разреженную таблицу для поиска максимума на подотрезке.
        2. Сначала находим максимумы для двух отрезков, которые покрывают наш диапазон.
        3. Затем возвращаем индекс максимума из этих двух отрезков.

    :param sparse_table: Разреженная таблица, созданная функцией build_sparse_table.
    :param log_values: Массив логарифмов для быстрого доступа.
    :param left: Левый индекс подотрезка (0-индексированный).
    :param right: Правый индекс подотрезка (0-индексированный).
    :returns: Индекс максимального элемента на подотрезке (1-индексированный).
    """
    # Определяем наибольшую степень двойки, которая укладывается в отрезок
    max_power_of_two_in_range: int = log_values[right - left + 1]

    # Определяем максимальные элементы для двух подотрезков
    left_max: ArrayElement = sparse_table[left][max_power_of_two_in_range]
    right_max: ArrayElement = sparse_table[right - (1 << max_power_of_two_in_range) + 1][max_power_of_two_in_range]

    # Возвращаем индекс максимального элемента
    max_element: ArrayElement = left_max if left_max.value >= right_max.value else right_max

    return max_element.index + 1


def main() -> None:
    _: int = int(input())
    array: List[int] = list(map(int, input().split()))
    query_count: int = int(input())

    sparse_table, log_values = build_sparse_table(array)

    results: List[int] = []
    for _ in range(query_count):
        left, right = map(lambda x: int(x) - 1, input().split())
        max_index = query_max(sparse_table, log_values, left, right)
        results.append(max_index)

    print(' '.join(map(str, results)))


if __name__ == "__main__":
    main()
