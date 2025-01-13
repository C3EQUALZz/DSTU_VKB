"""
Задача №111623. Продавец

На плоскости заданы координаты n (4≤n≤20) разных вершин.

Найти кратчайший замкнутый маршрут, начинающийся и заканчивающийся в 1-й вершине и посещающий все остальные вершины по одному разу.
Разрешается (если так оказывается выгодно) «проезжать через вершину, не останавливаясь» (см. пример 1).

Длина маршрута считается как сумма длин составляющих его рёбер, длины отдельных рёбер считаются согласно обычной евклидовой метрике, как .

Входные данные

Первая строка содержит количество вершин n (4≤n≤20).
Каждая из следующих n строк содержит по два разделённых пробелом числа с плавающей точкой — x- и y-координаты соответствующей вершины.

Выходные данные

Первая строка должна содержать единственное число (с плавающей точкой) — найденную минимальную длину замкнутого тура.
Вторая строка должна содержать перестановку чисел 2, 3, ..., N — порядок, в котором надо посещать эти вершины.
Числа внутри второй строки должны разделяться одинарными пробелами.
"""

from itertools import permutations
import math


def find_shortest_path(coords):
    n = len(coords)
    min_path_length = float('inf')
    min_path = []

    for perm in permutations(range(1, n)):
        current_path = [0] + list(perm) + [0]
        current_length = sum(math.dist(coords[current_path[i]], coords[current_path[i + 1]]) for i in range(n))

        if current_length < min_path_length:
            min_path_length = current_length
            min_path = perm

    return min_path_length, min_path


def main() -> None:
    n = int(input())
    coords = [tuple(map(float, input().split())) for _ in range(n)]

    min_path_length, min_path = find_shortest_path(coords)
    print(f"{min_path_length:.12e}")
    print(' '.join(map(lambda x: str(x + 1), min_path)))


if __name__ == '__main__':
    main()
