"""
Что такое куча? Двоичная куча - это просто структура данных, позволяющая быстро (за логарифмическое время) добавлять элементы
и извлекать элемент с максимальным приоритетом. Например, максимальный по значению.

Говоря коротко, это бинарное дерево, для которого выполняется следующее свойство: приоритет каждой вершины больше её потомков.
То есть максимальный элемент всегда находится на вершине кучи. В таком случае структура называется max-heap.

Двоичная куча обычно хранится в виде одномерного массива, где каждого потомка у узла можно найти по такому правилу:
2 * i + 1 - левый, а правый 2 * i + 2.

Высота кучи можно узнать, как log(N)
"""

import heapq
from typing import Iterable


def heapq_max(data: Iterable[int]) -> None:
    heap = []

    for number in data:
        heapq.heappush(heap, -number)

    while heap:
        print(-heapq.heappop(heap))


def heapq_min(data: Iterable[int]) -> None:
    heap = []

    for number in data:
        heapq.heappush(heap, number)

    while heap:
        print(heapq.heappop(heap))


def main() -> None:
    heapq_max([1, 2, 3])


if __name__ == '__main__':
    main()
