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
from array import array, ArrayType
from collections import deque
from itertools import product
from typing import List, Tuple, Sequence, cast


class TravelingSalesmanGraph:
    def __init__(self, coordinates: Sequence[Tuple[float, float]]) -> None:
        self.num_vertices = len(coordinates)
        self.coordinates = coordinates
        self.distance_matrix: List[ArrayType[float]] = [array('d', [float('inf')] * self.num_vertices) for _ in
                                                        range(1 << self.num_vertices)]
        self._initialize_distance_matrix()

    def _initialize_distance_matrix(self) -> None:
        """Инициализация таблицы расстояний для динамического программирования."""
        self.distance_matrix[1][0] = 0  # Начальная вершина посещена, длина пути 0

        for mask, u in product(range(1 << self.num_vertices), range(self.num_vertices)):

            if not (mask & (1 << u)):  # Если вершина u не посещена
                continue
            current_distance: float = self.distance_matrix[mask][u]

            for v in filter(lambda vertex: not mask & (1 << vertex), range(self.num_vertices)):  # Генератор для вершин
                next_mask: int = mask | (1 << v)
                minimal_distance_matrix: float = self.distance_matrix[next_mask][v]
                min_distance: float = min(minimal_distance_matrix, current_distance + self._calculate_distance(u, v))
                self.distance_matrix[next_mask][v] = min_distance

    def _calculate_distance(self, u: int, v: int) -> float:
        """Вычисление расстояния между двумя вершинами."""
        return math.dist(self.coordinates[u], self.coordinates[v])

    def find_shortest_path_length(self) -> Tuple[float, int]:
        """Нахождение минимальной длины пути и конечной вершины."""
        final_mask: int = (1 << self.num_vertices) - 1
        return min(
            (self.distance_matrix[final_mask][u] + self._calculate_distance(u, 0), u)
            for u in range(1, self.num_vertices)
        )

    def reconstruct_path(self, end_vertex: int, final_mask: int) -> Sequence[int]:
        """Восстановление пути из таблицы динамического программирования."""
        path: deque[int] = deque()

        mask, current_vertex = final_mask, end_vertex
        while current_vertex != 0:
            path.appendleft(current_vertex)
            current_distance: float = self.distance_matrix[mask][current_vertex]
            current_vertex: int = next(
                prev_vertex for prev_vertex in range(self.num_vertices)
                if (mask & (1 << prev_vertex)) and math.isclose(
                    current_distance,
                    self.distance_matrix[mask ^ (1 << current_vertex)][prev_vertex] +
                    self._calculate_distance(prev_vertex, current_vertex)
                )
            )
            mask ^= (1 << path[0])

        return path


def find_optimal_tour(coordinates: Sequence[Tuple[float, float]]) -> Tuple[float, Sequence[int]]:
    """Основная логика для нахождения кратчайшего пути."""
    graph = TravelingSalesmanGraph(coordinates)

    shortest_path_length, end_vertex = graph.find_shortest_path_length()
    path = graph.reconstruct_path(end_vertex, (1 << graph.num_vertices) - 1)

    return shortest_path_length, [x + 1 for x in path]


def main() -> None:
    num_vertices = int(input())
    coordinates = cast(List[Tuple[int, int]], [tuple(map(float, input().split())) for _ in range(num_vertices)])
    shortest_path_length, optimal_path = find_optimal_tour(coordinates)
    print(f"{shortest_path_length:.14e}")
    print(' '.join(map(str, optimal_path)))


if __name__ == "__main__":
    main()
