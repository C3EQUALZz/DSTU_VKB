"""
Задание 1. поиск в ширину/поиск в глубину.

Данные вводить с клавиатуры следующим образом:
Сначала вводите кол-во вершин, далее программа запрашивает по каждому ребру, пример:
“есть связь между вершиной 1 и 4?” и вводите “да/нет”. После чего выводится на экран матрица смежности.

Далее по вариантам реализовать поиск в ширину (1 вариант) или поиск в глубину (2 вариант) варианты также по списку.
Не забудьте добавить возможность введения с клавиатуры с какой вершины начинается поиск.
Далее вывести все возможные пути прохода с расстоянием (количество ребер).
"""

import sys
from itertools import combinations

from algorithms_and_data_structures.fourth_laboratory.core.unweighted import \
    NonOrientedGraph
from algorithms_and_data_structures.fourth_laboratory.first_question.bfs import \
    bfs
from algorithms_and_data_structures.fourth_laboratory.first_question.dfs import \
    dfs


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
