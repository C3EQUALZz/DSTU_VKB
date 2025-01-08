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
from collections import namedtuple
from typing import List

Edge = namedtuple('Edge', ['weight', 'vertex1', 'vertex2'])


class DisjointSetUnion:
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, node: int) -> int:
        if node != self.parent[node]:
            self.parent[node] = self.find(self.parent[node])  # Path compression
        return self.parent[node]

    def union(self, node1: int, node2: int) -> None:
        root1 = self.find(node1)
        root2 = self.find(node2)

        if root1 != root2:
            # Union by rank
            if self.rank[root1] < self.rank[root2]:
                root1, root2 = root2, root1
            self.parent[root2] = root1
            if self.rank[root1] == self.rank[root2]:
                self.rank[root1] += 1


def kruskal(num_vertices: int, edges: List[Edge]) -> int:
    dsu = DisjointSetUnion(num_vertices)
    minimum_spanning_tree_weight = 0

    # Sort edges by weight
    for edge in sorted(edges, key=lambda e: e.weight):
        if dsu.find(edge.vertex1) != dsu.find(edge.vertex2):
            dsu.union(edge.vertex1, edge.vertex2)
            minimum_spanning_tree_weight += edge.weight

    return minimum_spanning_tree_weight


def main() -> None:
    num_vertices, num_edges = map(int, input().split())
    edges = []

    for _ in range(num_edges):
        vertex1, vertex2, weight = map(int, input().split())
        edges.append(Edge(weight, vertex1 - 1, vertex2 - 1))

    print(kruskal(num_vertices, edges))


if __name__ == "__main__":
    main()
