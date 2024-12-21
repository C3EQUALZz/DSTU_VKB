from typing import List, Optional, Set, TypeVar

from algorithms_and_data_structures.fourth_laboratory.core.base import BaseUnWeightedGraph

T = TypeVar("T")

def dfs(
        graph: BaseUnWeightedGraph[T],
        start: T,
        target: T,
        path: Optional[List[T]] = None,
        visited: Optional[Set[T]] = None
) -> Optional[List[T]]:
    """
    Выполняет поиск в глубину (DFS) в графе.

    :param graph: Граф, в котором выполняется поиск.
    :param start: Начальная вершина.
    :param target: Целевая вершина.
    :param path: Текущий путь (по умолчанию None).
    :param visited: Множество посещённых вершин (по умолчанию None).
    :returns: Список вершин, представляющий найденный путь, или None, если путь не найден.
    """

    if path is None:
        path = []
    if visited is None:
        visited = set()

    path.append(start)
    visited.add(start)

    if start == target:
        return path

    for neighbour in graph.get_neighbors(start):
        if neighbour not in visited:
            result = dfs(graph, neighbour, target, path, visited)
            if result is not None:
                return result

    path.pop()
