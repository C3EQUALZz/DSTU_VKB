"""
Задача №3785. Задача коммивояжёра --- 2

На плоскости заданы координаты n (4≤n≤15) разных вершин.

Найти кратчайший замкнутый маршрут, начинающийся и заканчивающийся в 1-й вершине и посещающий все остальные вершины по одному разу.
Разрешается (если так оказывается выгодно) «проезжать через вершину, не останавливаясь» (см. пример 1).

Длина маршрута считается как сумма длин составляющих его рёбер, длины отдельных рёбер считаются согласно обычной
евклидовой метрике, как sqrt((xa-xb)^2 - (ya-yb)^2).

Входные данные

Первая строка содержит количество вершин n (4≤n≤15).
Каждая из следующих n строк содержит по два разделённых пробелом числа с плавающей точкой — x- и y-координаты соответствующей вершины.

Выходные данные

Первая строка должна содержать единственное число (с плавающей точкой) — найденную минимальную длину замкнутого тура.
Вторая строка должна содержать перестановку чисел 2, 3, ..., N — порядок, в котором надо посещать эти вершины.
Числа внутри второй строки должны разделяться одинарными пробелами.

Примечание

Задача с такими ограничениями, по идее, должна решаться хоть методом ветвей и границ, хоть динамическим программированием
по подмножествам. Но она, по идее, не должна решаться одними лишь отсечениями поиска с возвратом (backtracking),
не пытающегося оценивать возможный диапазон длины ещё не построенной части пути.
"""

import math
from itertools import combinations
from typing import List, Tuple


def reconstruct_path(memoization_table, bits: int, parent: int, n: int) -> List[int]:
    path = []
    for _ in range(n - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = memoization_table[(bits, parent)]
        bits = new_bits
    path.append(0)
    return list(reversed(path))


def tsp_dynamic_programming(points: List[Tuple[float, float]]) -> Tuple[float, List[int]]:
    n = len(points)
    dist_matrix = [[math.dist(points[i], points[j]) for j in range(n)] for i in range(n)]

    # memoization table, where keys are pairs (set of visited vertices, current vertex)
    # Set initial values where the first vertex is already visited
    memoization_table = {(1 << k, k): (dist_matrix[0][k], 0) for k in range(1, n)}

    # Iterate over subsets of vertices
    for subset_size in range(2, n):
        for subset in combinations(range(1, n), subset_size):
            # Set bits for all vertices in the subset
            bits = sum(1 << bit for bit in subset)

            # Find the shortest path to this subset ending at vertex k
            for k in subset:
                prev = bits & ~(1 << k)
                memoization_table[(bits, k)] = min(
                    (memoization_table[(prev, m)][0] + dist_matrix[m][k], m)
                    for m in subset if m != 0 and m != k
                )

    # We're returning to the first vertex, complete the tour
    bits = (2 ** n - 1) - 1
    opt, parent = min((memoization_table[(bits, k)][0] + dist_matrix[k][0], k) for k in range(1, n))

    path = reconstruct_path(memoization_table, bits, parent, n)

    return opt, path


def main() -> None:
    n = int(input())
    points = [tuple(map(float, input().split())) for _ in range(n)]
    min_length, min_path = tsp_dynamic_programming(points)
    print('{:.15E}'.format(min_length))
    print(' '.join(map(lambda x: str(x + 1), min_path[1:])))


if __name__ == '__main__':
    main()
