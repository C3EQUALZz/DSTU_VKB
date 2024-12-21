from typing import TypeVar, List

from algorithms_and_data_structures.fourth_laboratory.first_question.core.base import BaseGraph

T = TypeVar('T')


class NonOrientedGraph(BaseGraph[T]):
    """
    Класс, который описывает неориентированный граф.
    Реализовал только данный вид, так как в лабораторной такое требуется.
    """

    def add_edge(self, u: T, v: T) -> None:
        """
        Добавить дугу графа.
        Здесь нет направления, поэтому буквально делаем добавление туда - обратно.
        :param u: Первая вершина графа.
        :param v: Вторая вершина графа.
        :returns: Ничего не возвращает.
        """
        self._graph[u].append(v)
        self._graph[v].append(u)

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
                matrix[index2][index1] = 1

        result = ' ' + ' '.join(chr(x + 65) for x in range(n)) + '\n'
        for index, row in enumerate(matrix):
            result += chr(index + 65) + ' ' + ' '.join(map(str, row)) + '\n'

        return result.strip()
