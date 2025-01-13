"""
Задача №180. Цикл

Дан ориентированный граф. Определить, есть ли в нем цикл отрицательного веса, и если да, то вывести его.
Входные данные

В первой строке содержится число N (1 <= N <= 100) – количество вершин графа.
В следующих N строках находится по N чисел – матрица смежности графа.
Веса ребер по модулю меньше 100000. Если ребра нет, соответствующее значение равно 100000.

Выходные данные

В первой строке выведите "YES", если цикл существует, или "NO", в противном случае.
При наличии цикла выведите во второй строке количество вершин в нем (считая одинаковые – первую и последнюю),
а в третьей строке – вершины, входящие в этот цикл, в порядке обхода. Если циклов несколько, то выведите любой из них.

НЕ ПРОХОДИТ НА 100 БАЛЛОВ ПО ПАМЯТИ!
"""
from array import array, ArrayType
from collections import deque
from itertools import chain
from typing import Final, Sequence, Dict, List, Tuple

INF: Final[float] = float('inf')


def restore_cycle(path: Sequence[int], start_index: int) -> Sequence[int]:
    if start_index == -1:
        return []

    cycle_start = path[path.index(start_index)]
    p = deque([cycle_start])
    cycle = path[cycle_start]

    while cycle != cycle_start:
        p.appendleft(cycle)
        cycle = path[cycle]

    p.appendleft(cycle_start)

    return p


def main() -> None:
    n: int = int(input())

    graph: Dict[int, List[Tuple[int, int]]] = {
        i: [(j, w) for j, w in enumerate(map(int, input().split())) if w < 100000]
        for i in range(n)
    }

    distance: ArrayType[float] = array("d", [INF] * n)
    path: ArrayType[int] = array("i", [-1] * n)

    cycle: int = -1

    # Алгоритм Беллмана-Форда
    # Тут слишком сильные временные рамки, поэтому если выносить в отдельную функцию, то вместо 20 тестов будет 16 пройдено.
    for k in filter(lambda x: distance[x] == INF, range(n)):
        distance[k] = 0
        for _ in range(n):
            cycle = -1

            for u, (v, weight) in chain.from_iterable(((u, edge) for edge in edges) for u, edges in graph.items()):
                if distance[u] < INF and distance[v] > distance[u] + weight:
                    distance[v] = distance[u] + weight
                    path[v] = u
                    cycle = v

    result = restore_cycle(path, cycle)

    if result:
        print("YES", len(result), " ".join(str(node + 1) for node in result), sep="\n")
    else:
        print("NO")


if __name__ == '__main__':
    main()
