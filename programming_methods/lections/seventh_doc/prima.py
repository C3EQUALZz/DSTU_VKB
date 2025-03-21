from typing import TypeVar, Set, Tuple
import heapq
from programming_methods.lections.first_doc.fifth_block.core.weighted.nonoriented import NonOrientedGraph

T = TypeVar('T')


def prim_mst(graph: NonOrientedGraph[T]) -> NonOrientedGraph[T]:
    """
    Алгоритм Прима для поиска минимального остовного дерева.
    Возвращает новый граф, представляющий MST.
    """
    mst = NonOrientedGraph[T]()
    visited: Set[T] = set()

    # Проверка на пустой граф
    if not graph._graph:
        return mst

    # Стартовая вершина
    start_vertex = next(iter(graph))
    visited.add(start_vertex)

    # Очередь смежных рёбер вида (вес, вершина_откуда, вершина_куда)
    edges_heap: list[Tuple[float, T, T]] = []

    # Добавляем все рёбра, исходящие из стартовой вершины
    for neighbor in graph.get_neighbors(start_vertex):
        weight = graph.get_weight(start_vertex, neighbor)
        heapq.heappush(edges_heap, (weight, start_vertex, neighbor))

    while edges_heap and len(visited) < len(graph):
        weight, u, v = heapq.heappop(edges_heap)

        if v in visited:
            continue

        # Добавляем вершину (неявно) и ребро в MST
        mst.add_edge(u, v, weight)
        visited.add(v)

        # Добавляем рёбра из новой вершины
        for neighbor in graph.get_neighbors(v):
            if neighbor not in visited:
                edge_weight = graph.get_weight(v, neighbor)
                heapq.heappush(edges_heap, (edge_weight, v, neighbor))

    return mst


def main() -> None:
    # Создаём граф
    graph = NonOrientedGraph[str]()

    # Добавляем рёбра (граф неориентированный, так что достаточно одного add_edge на пару вершин)
    graph.add_edge('A', 'B', 4)
    graph.add_edge('A', 'H', 8)
    graph.add_edge('B', 'H', 11)
    graph.add_edge('B', 'C', 8)
    graph.add_edge('C', 'I', 2)
    graph.add_edge('C', 'F', 4)
    graph.add_edge('C', 'D', 7)
    graph.add_edge('D', 'F', 14)
    graph.add_edge('D', 'E', 9)
    graph.add_edge('E', 'F', 10)
    graph.add_edge('F', 'G', 2)
    graph.add_edge('G', 'I', 6)
    graph.add_edge('G', 'H', 1)
    graph.add_edge('H', 'I', 7)

    print("Исходный граф:")
    print(graph)

    # Строим минимальное остовное дерево
    mst = prim_mst(graph)

    print("\nМинимальное остовное дерево (MST):")
    print(mst)


if __name__ == '__main__':
    main()
