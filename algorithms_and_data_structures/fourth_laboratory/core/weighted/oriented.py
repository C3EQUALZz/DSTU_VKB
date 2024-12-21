from typing import TypeVar, List

from prettytable import PrettyTable

from algorithms_and_data_structures.fourth_laboratory.core.base import BaseWeightedGraph

T = TypeVar('T')


class OrientedGraph(BaseWeightedGraph[T]):
    def add_edge(self, u: T, v: T, weight: float) -> None:
        self._graph[u].append(v)
        self._weights[u][v] = weight

    def __str__(self) -> str:
        n: int = len(self._graph)
        vertices = list(self._graph.keys())
        index_map = {vertex: idx for idx, vertex in enumerate(vertices)}

        # Создаем матрицу смежности с весами
        matrix: List[List[float]] = [[0 for _ in range(n)] for _ in range(n)]

        for vertex1 in self._graph:
            for vertex2 in self.get_neighbors(vertex1):
                weight = self.get_weight(vertex1, vertex2)
                index1 = index_map[vertex1]
                index2 = index_map[vertex2]
                matrix[index1][index2] = weight

        # Создаем таблицу
        table = PrettyTable()
        table.field_names = [' '] + vertices  # Заголовки столбцов

        for index, row in enumerate(matrix):
            table.add_row([vertices[index]] + row)  # Добавляем строки с весами

        return str(table)
