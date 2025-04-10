from typing import List, TypeVar

from prettytable import PrettyTable

from programming_methods.lections.first_doc.fifth_block.core.base import \
    BaseUnWeightedGraph

T = TypeVar("T")


class OrientedGraph(BaseUnWeightedGraph[T]):
    def add_edge(self, u: T, v: T) -> None:
        self._graph[u].append(v)

    def __str__(self) -> str:
        """
        Вывод на печать матрицы смежности.
        :returns: Возвращает на печать строковый вид матрицы.
        """
        n: int = len(self._graph)

        matrix: List[List[int]] = [[0 for _ in range(n)] for _ in range(n)]

        for vertex1 in self._graph:
            for vertex2 in self.get_neighbors(vertex1):
                index1 = ord(vertex1) - 65
                index2 = ord(vertex2) - 65
                matrix[index1][index2] = 1

        table = PrettyTable()
        table.field_names = [" "] + [chr(x + 65) for x in range(n)]

        for index, row in enumerate(matrix):
            table.add_row([chr(index + 65)] + row)

        return str(table)
