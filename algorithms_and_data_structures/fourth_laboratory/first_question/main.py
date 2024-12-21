import sys
from itertools import combinations
from typing import List

from algorithms_and_data_structures.fourth_laboratory.first_question.bfs import bfs
from algorithms_and_data_structures.fourth_laboratory.first_question.core.nonoriented import NonOrientedGraph
from algorithms_and_data_structures.fourth_laboratory.first_question.dfs import dfs


def create_graph_from_user_input() -> NonOrientedGraph:
    n: int = int(input('Введите количество вершин: '))

    graph: NonOrientedGraph[str] = NonOrientedGraph()

    # Создаем матрицу смежности
    matrix: List[List[int]] = [[0 for _ in range(n)] for _ in range(n)]

    # Генерируем все возможные комбинации вершин
    edges = list(combinations(range(1, n + 1), 2))

    # Запрашиваем у пользователя наличие связи между вершинами
    for vertex1, vertex2 in edges:
        s = f'Есть ли связь между вершинами {chr(64 + vertex1)} и {chr(64 + vertex2)}? (да/нет) '
        response = input(s).strip().lower()
        if response in ('да', 'yes'):
            graph.add_edge(chr(vertex1 + 64), chr(64 + vertex2))
            matrix[vertex1 - 1][vertex2 - 1] = 1
            matrix[vertex2 - 1][vertex1 - 1] = 1

    # Выводим матрицу смежности
    print(' ', *[chr(x + 64) for x in range(1, n + 1)])
    for index, row in enumerate(matrix, start=1):
        print(chr(index + 64), *row)

    return graph


def main() -> None:
    while True:
        questions = {
            "1": dfs,
            "2": bfs,
        }

        user_input = input("Что вы хотите сделать? Поиск в ширину (1) или поиск в глубину (2)? ")

        if user_input not in questions:
            continue

        graph = create_graph_from_user_input()

        start_vertex = input("Введите начальную вершину: ")

        if start_vertex not in graph:
            print(f"{start_vertex} нет в графе. Запускаю заново полностью алгоритм. ", file=sys.stderr)
            continue

        end_vertex = input("Введите конечную вершину: ")

        if end_vertex not in graph:
            print(f"{end_vertex} нет в графе. Запускаю заново полностью алгоритм. ", file=sys.stderr)
            continue

        print(questions[user_input](graph, start_vertex, end_vertex))


if __name__ == '__main__':
    main()
