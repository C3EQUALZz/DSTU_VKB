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
from collections import deque
from typing import Iterable, List, Sequence


def longest_increasing_subsequence(sequence: Sequence[int]) -> Iterable[int]:
    """
    Находит наибольшую возрастающую подпоследовательность.

    Алгоритм основан на комбинации бинарного поиска и динамического программирования.
    Он работает следующим образом:

    1. Инициализируются три списка:
       - `largest_increasing_subsequence`: хранит текущие элементы наибольшей возрастающей подпоследовательности.
       - `prev_index`: используется для восстановления последовательности, где каждый элемент хранит индекс предыдущего
        элемента в НАП.
       - `indices`: хранит индексы элементов в `sequence`, соответствующие элементам в `largest_increasing_subsequence`.

    2. Для каждого элемента `value` в последовательности:
       - Используется `bisect_left` для нахождения позиции `pos`, где `value` может быть вставлен
        в `largest_increasing_subsequence`, чтобы сохранить его отсортированным.
       - Если `value` больше всех элементов в `largest_increasing_subsequence`, он добавляется в конец списка.
       - В противном случае, элемент в `largest_increasing_subsequence` на позиции `pos` заменяется на `value`,
        и обновляется соответствующий индекс в `indices`.

    3. Восстанавливаются индексы предыдущих элементов, чтобы можно было восстановить саму последовательность.

    4. После обработки всех элементов, последовательность восстанавливается, начиная с последнего элемента НАП,
     используя `prev_index`.

    5. Возвращается наибольшая возрастающая подпоследовательность в правильном порядке.

    :param sequence: Последовательность из условия задачи.
    :returns: Наибольшая возрастающая подпоследовательность.
    """
    largest_increasing_subsequence: List[int] = []
    prev_index: List[int] = [-1] * len(sequence)
    indices: List[int] = []

    for i, value in enumerate(sequence):
        pos = bisect_left(largest_increasing_subsequence, value)

        # Если значение больше всех элементов в lis, добавляем его
        if pos == len(largest_increasing_subsequence):
            largest_increasing_subsequence.append(value)
            indices.append(i)
        else:
            largest_increasing_subsequence[pos] = value
            indices[pos] = i

        # Восстанавливаем индексы
        if pos > 0:
            prev_index[i] = indices[pos - 1]

    # Восстанавливаем саму последовательность
    result: deque[int] = deque()
    k = indices[-1]
    while k != -1:
        result.append(sequence[k])
        k = prev_index[k]

    result.reverse()

    return result


def main() -> None:
    n, a1, k, b, m = map(int, input().split())

    # Генерируем последовательность по формуле, которая дана в условии
    sequence = [0] * n
    sequence[0] = a1
    for i in range(1, n):
        sequence[i] = (k * sequence[i - 1] + b) % m

    lis = longest_increasing_subsequence(sequence)

    print(" ".join(map(str, lis)))


if __name__ == "__main__":
    main()
