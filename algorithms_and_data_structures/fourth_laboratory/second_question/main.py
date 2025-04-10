"""
Задание 2.  Алгоритм Дейкстры.
С клавиатуры, любым способом задайте граф (как в первом задании, сразу матрицами или списками),
не забудьте, что граф взвешенный, но считайте его неориентированным.

Дополнительно необходимо ввести две вершины (начало и конец пути).
И далее реализовать алгоритм Дейкстры, т.е найти кратчайший путь и вывести его.
"""

import sys
from itertools import combinations

from algorithms_and_data_structures.fourth_laboratory.core.weighted import \
    NonOrientedGraph
from algorithms_and_data_structures.fourth_laboratory.second_question.dijkstra import \
    dijkstra


def create_graph_from_user_input(n: int) -> NonOrientedGraph:
    graph: NonOrientedGraph[str] = NonOrientedGraph()

    edges = combinations(range(1, n + 1), 2)

    for vertex1, vertex2 in edges:
        s = f"Есть ли связь между вершинами {chr(64 + vertex1)} и {chr(64 + vertex2)}? (да/нет) "
        response = input(s).strip().lower()
        if response in ("да", "yes"):
            if (weight := input("Введите вес дуги (целое число): ")).isdigit():
                graph.add_edge(chr(vertex1 + 64), chr(64 + vertex2), int(weight))
            else:
                print(
                    "Вы ввели не целое число. Перезапускаю программу", file=sys.stderr
                )
                continue

    return graph


def main() -> None:
    while True:
        n: int = int(input("Введите количество вершин: "))

        graph: NonOrientedGraph[str] = create_graph_from_user_input(n)
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

        print(dijkstra(graph, start_vertex, end_vertex))


if __name__ == "__main__":
    main()
