# Реализовать поиск по ширине и глубине

import sys
from itertools import combinations
from queue import Queue
from typing import Dict, List, Optional, Set, TypeVar

from programming_methods.lections.first_doc.fifth_block.core.base import \
    BaseUnWeightedGraph
from programming_methods.lections.first_doc.fifth_block.core.unweighted.nonoriented import \
    NonOrientedGraph

T = TypeVar("T")


def bfs(
    graph: BaseUnWeightedGraph[T], start_node: T, target_node: T
) -> Optional[List[T]]:
    """
    Выполняет поиск в ширину (BFS).
    :param graph: Граф, в котором выполняется поиск.
    :param start_node: Стартовая вершина в графе.
    :param target_node: Конечная вершина в графе.
    :returns:
    """
    # Set of visited nodes to prevent loops
    visited: Set[T] = set()
    queue: Queue[T] = Queue()

    # Add the start_node to the queue and visited list
    queue.put(start_node)
    visited.add(start_node)

    # start_node has no parents
    parent: Dict[T, T] = {start_node: None}

    # Perform BFS
    path_found = False
    while not queue.empty():
        current_node = queue.get()
        if current_node == target_node:
            path_found = True
            break

        for next_node in graph.get_neighbors(current_node):
            if next_node not in visited:
                queue.put(next_node)
                parent[next_node] = current_node
                visited.add(next_node)

    # Path reconstruction
    path: List[T] = []

    if not path_found:
        return None

    path.append(target_node)
    while parent[target_node] is not None:
        path.append(parent[target_node])
        target_node = parent[target_node]
    path.reverse()

    return path


def dfs(
    graph: BaseUnWeightedGraph[T],
    start: T,
    target: T,
    path: Optional[List[T]] = None,
    visited: Optional[Set[T]] = None,
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


def create_graph_from_user_input(n: int) -> NonOrientedGraph:
    """
    Функция для создания графа на основе ввода пользователя.
    Вынес в отдельную функцию, так как в таком случае main будет перегружен кодом.
    :param n: Количество вершин.
    :returns: Возвращает неориентированный граф.
    """
    graph: NonOrientedGraph[str] = NonOrientedGraph()

    edges = combinations(range(1, n + 1), 2)

    for vertex1, vertex2 in edges:
        s = f"Есть ли связь между вершинами {chr(64 + vertex1)} и {chr(64 + vertex2)}? (да/нет) "
        response = input(s).strip().lower()
        if response in ("да", "yes"):
            graph.add_edge(chr(vertex1 + 64), chr(64 + vertex2))

    return graph


def main() -> None:
    while True:
        questions = {
            "1": bfs,
            "2": dfs,
        }

        user_input = input(
            "Что вы хотите сделать? Поиск в ширину (1) или поиск в глубину (2)? "
        )

        if user_input not in questions:
            continue

        n: int = int(input("Введите количество вершин: "))

        graph = create_graph_from_user_input(n)
        print(graph)

        start_vertex = input("Введите начальную вершину: ")

        if start_vertex not in graph:
            print(
                f"{start_vertex} нет в графе. Запускаю заново полностью алгоритм. ",
                file=sys.stderr,
            )
            continue

        end_vertex = input("Введите конечную вершину: ")

        if end_vertex not in graph:
            print(
                f"{end_vertex} нет в графе. Запускаю заново полностью алгоритм. ",
                file=sys.stderr,
            )
            continue

        print(questions[user_input](graph, start_vertex, end_vertex))


if __name__ == "__main__":
    main()
