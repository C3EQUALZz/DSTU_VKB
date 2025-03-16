# Найти кратчайший путь между двумя вершинами

import sys
from itertools import combinations
from queue import PriorityQueue
from typing import TypeVar, List

from programming_methods.lections.first_doc.fifth_block.core.base import BaseWeightedGraph
from programming_methods.lections.first_doc.fifth_block.core.weighted.nonoriented import NonOrientedGraph

T = TypeVar("T")


def dijkstra(graph: BaseWeightedGraph[T], start_vertex: T, end_vertex: T) -> List[T]:
    distances = {v: float('inf') for v in graph}
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


def create_graph_from_user_input(n: int) -> NonOrientedGraph:
    graph: NonOrientedGraph[str] = NonOrientedGraph()

    edges = combinations(range(1, n + 1), 2)

    for vertex1, vertex2 in edges:
        s = f'Есть ли связь между вершинами {chr(64 + vertex1)} и {chr(64 + vertex2)}? (да/нет) '
        response = input(s).strip().lower()
        if response in ('да', 'yes'):
            if (weight := input("Введите вес дуги (целое число): ")).isdigit():
                graph.add_edge(chr(vertex1 + 64), chr(64 + vertex2), int(weight))
            else:
                print("Вы ввели не целое число. Перезапускаю программу", file=sys.stderr)
                continue

    return graph


def main() -> None:
    while True:
        n: int = int(input("Введите количество вершин: "))

        graph: NonOrientedGraph[str] = create_graph_from_user_input(n)
        print(graph)

        start_vertex = input("Введите начальную вершину: ")

        if start_vertex not in graph:
            print(f"{start_vertex} нет в графе. Запускаю заново полностью алгоритм. ", file=sys.stderr)
            continue

        end_vertex = input("Введите конечную вершину: ")

        if end_vertex not in graph:
            print(f"{end_vertex} нет в графе. Запускаю заново полностью алгоритм. ", file=sys.stderr)
            continue

        print(dijkstra(graph, start_vertex, end_vertex))


if __name__ == '__main__':
    main()
