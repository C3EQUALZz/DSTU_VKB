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

РЕШЕНИЕ НЕ ПРОХОДИТ ПО СКОРОСТИ ИЗ-ЗА PYTHON.
"""
import math
from array import array
from collections import deque
from itertools import product
from typing import List, Tuple, Sequence, cast


def calculate_distance(
        u: int,
        v: int,
        coords: Sequence[Tuple[float, float]]
) -> float:
    """Вычисление расстояния между двумя вершинами."""
    return math.dist(coords[u], coords[v])


def initialize_dp_table(
        n: int,
        coords: Sequence[Tuple[float, float]]
) -> Sequence[array]:
    """Инициализация таблицы динамического программирования."""
    distance_table = [array('d', [float('inf')] * n) for _ in range(1 << n)]
    distance_table[1][0] = 0  # Начальная вершина посещена, длина пути 0

    for mask, u in product(range(1 << n), range(n)):
        if not (mask & (1 << u)):  # Если вершина u не посещена
            continue
        dp_mask_u = distance_table[mask][u]
        for v in filter(lambda vertex: not mask & (1 << vertex), range(n)):  # Генератор для вершин
            next_mask = mask | (1 << v)
            distance_table[next_mask][v] = min(distance_table[next_mask][v], dp_mask_u + calculate_distance(u, v, coords))

    return distance_table


def find_min_path_length(
        n: int,
        coords: Sequence[Tuple[float, float]],
        distance_table: Sequence[array]
) -> Tuple[float, int]:
    """Нахождение минимальной длины пути и конечной вершины."""
    last_mask = (1 << n) - 1
    return min((distance_table[last_mask][u] + calculate_distance(u, 0, coords), u) for u in range(1, n))


def reconstruct_path(
        n: int,
        coords: Sequence[Tuple[float, float]],
        distance_table: Sequence[array],
        end_vertex: int,
        last_mask: int
) -> Sequence[int]:
    """Восстановление пути из таблицы dp."""
    path = deque()

    mask, current_vertex = last_mask, end_vertex
    while current_vertex != 0:
        path.appendleft(current_vertex)
        current_distance = distance_table[mask][current_vertex]
        current_vertex = next(
            prev_vertex for prev_vertex in range(n)
            if (mask & (1 << prev_vertex)) and math.isclose(
                current_distance,
                distance_table[mask ^ (1 << current_vertex)][prev_vertex] +
                calculate_distance(prev_vertex, current_vertex, coords)
            )
        )
        mask ^= (1 << path[0])

    return path


def find_shortest_path(coords: Sequence[Tuple[float, float]]) -> Tuple[float, Sequence[int]]:
    """Основная логика для нахождения кратчайшего пути."""
    n = len(coords)

    dp = initialize_dp_table(n, coords)

    min_path_length, end_vertex = find_min_path_length(n, coords, dp)

    path = reconstruct_path(n, coords, dp, end_vertex, (1 << n) - 1)

    # Преобразование пути к нужному формату
    return min_path_length, [x + 1 for x in path]


def main() -> None:
    n = int(input())
    coords = cast(List[Tuple[int, int]], [tuple(map(float, input().split())) for _ in range(n)])
    min_path_length, min_path = find_shortest_path(coords)
    print(f"{min_path_length:.14e}")
    print(' '.join(map(str, min_path)))


if __name__ == "__main__":
    main()
