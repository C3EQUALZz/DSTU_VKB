"""
Задача №1377. Остовное дерево

Требуется найти в связном графе остовное дерево минимально веса.

Входные данные

Первая строка входного файла содержит два натуральных числа n и m - количество вершин и ребер графа соответственно
(1≤n≤20000, 0≤m≤100000).
Следующие m строк содержат описание ребер по одному на строке. Ребро номер i описывается тремя натуральными числами bi,
ei и wi - номера концов ребра и его вес соответственно (1≤bi,ei≤n, 0≤wi≤100000).

Граф является связным.

Выходные данные

Выведите единственное целое число - вес минимального остовного дерева.
"""

from array import array
from collections import namedtuple
from typing import Generic, List, Sequence, TypeVar

Edge = namedtuple("Edge", ["weight", "vertex1", "vertex2"])

T = TypeVar("T")


class DisjointSetUnion(Generic[T]):
    def __init__(self, size: int):
        """
        Класс для реализации структуры данных "Система непересекающихся множеств" (DSU).
        Он позволяет эффективно объединять компоненты графа и находить представителя компоненты для каждой вершины.
        :param size: Количество вершин в графе.
        """
        self.parent = array("i", range(size))
        self.rank = array("i", [0] * size)

    def find(self, node: T) -> int:
        """
        Находит представителя компоненты, в которой находится вершина node.
        Сжатием путей уменьшаем глубину дерева, чтобы ускорить поиск в дальнейшем.

        :param node: Номер вершины, для которой ищем представителя.
        :return: Представитель компоненты для вершины.
        """
        if node != self.parent[node]:
            # Сжатие пути (оптимизация поиска)
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, node1: T, node2: T) -> None:
        """
        Объединяет две компоненты, в которых находятся вершины node1 и node2.
        Используем стратегию объединения по рангу для оптимизации.

        :param node1: Первая вершина, которую нужно объединить.
        :param node2: Вторая вершина, которую нужно объединить.
        """
        root1 = self.find(node1)
        root2 = self.find(node2)

        if root1 != root2:
            # Union by rank
            if self.rank[root1] < self.rank[root2]:
                root1, root2 = root2, root1
            self.parent[root2] = root1
            if self.rank[root1] == self.rank[root2]:
                self.rank[root1] += 1


def kruskal(num_vertices: int, edges: Sequence[Edge]) -> int:
    """
    Алгоритм Краскала для нахождения минимального остовного дерева в графе.
    Сначала сортируем все ребра по весу, а затем поочередно добавляем их в дерево,
    если они не образуют цикл. Для этого используется структура DSU (Disjoint Set Union).

    :param num_vertices: Количество вершин в графе.
    :param edges: Список всех рёбер графа.
    :return: Вес минимального остовного дерева.
    """
    dsu: DisjointSetUnion[int] = DisjointSetUnion(num_vertices)
    minimum_spanning_tree_weight: int = 0

    # Сортируем рёбра по весу в порядке возрастания
    for edge in sorted(edges, key=lambda e: e.weight):
        # Если вершины ещё не соединены, то объединяем их и добавляем вес ребра в итоговый результат
        if dsu.find(edge.vertex1) != dsu.find(edge.vertex2):
            dsu.union(edge.vertex1, edge.vertex2)
            minimum_spanning_tree_weight += edge.weight

    return minimum_spanning_tree_weight


def main() -> None:
    num_vertices, num_edges = map(int, input().split())
    edges: List[Edge] = []

    for _ in range(num_edges):
        vertex1, vertex2, weight = map(int, input().split())
        edges.append(Edge(weight, vertex1 - 1, vertex2 - 1))

    print(kruskal(num_vertices, edges))


if __name__ == "__main__":
    main()
