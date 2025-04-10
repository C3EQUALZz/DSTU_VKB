from queue import PriorityQueue
from typing import List, TypeVar

from algorithms_and_data_structures.fourth_laboratory.core.base import \
    BaseWeightedGraph

T = TypeVar("T")


def dijkstra(graph: BaseWeightedGraph[T], start_vertex: T, end_vertex: T) -> List[T]:
    distances = {v: float("inf") for v in graph}
    distances[start_vertex] = 0

    # Словарь для отслеживания предшественников
    predecessors = {v: None for v in graph}

    pq = PriorityQueue()
    pq.put((0, start_vertex))

    while not pq.empty():
        (dist, current_vertex) = pq.get()

        # Если мы достигли конечной вершины, можем завершить
        if current_vertex == end_vertex:
            break

        for neighbor in graph.get_neighbors(current_vertex):
            distance = graph.get_weight(current_vertex, neighbor)
            new_cost = distances[current_vertex] + distance

            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                predecessors[neighbor] = current_vertex
                pq.put((new_cost, neighbor))

    # Восстановление пути
    path = []
    current = end_vertex
    while current is not None:
        path.append(current)
        current = predecessors[current]
    path.reverse()

    return path
