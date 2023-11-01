"""
Реализация алгоритма Флойда для взаимодействия через консоль с пользователем.

Разработан в учебных целях, здесь активно используется декораторы во избежание того, чтобы
пользователь не вводил некорректные данные. В случае неверного ввода будет вызвано исключение.

Из оптимизаций: использование параллельных вычислений.
Является только логикой, основное взаимодействие осуществляется в interact_with_user.py
"""
import threading

import interact_with_user as interact
from decorators import pprint_matrix

all_path = []


def update_path(i: int, top: int, matrix: list[list]) -> None:
    """
    Обновление кратчайшего пути между двумя вершинами i и j через промежуточную вершину top
    :param i: номер первой вершины
    :param top: номер промежуточной вершины при движении от i к j
    :param matrix: матрица смежности для графа
    """
    global all_path
    for j in range(len(matrix)):
        if matrix[i][j] > matrix[i][top] + matrix[top][j]:
            matrix[i][j] = matrix[i][top] + matrix[top][j]
            all_path[i][j] = top


@pprint_matrix
def floyd(n: int) -> tuple[list[list], list[list]]:
    """
    Функция, реализующая алгоритм Флойда
    :param n: количество вершин
    :return: матрицу смежности, где заполнены всевозможные пути,
    и матрицу, показывающей вершину, где проходит самый короткий путь через 2 других
    """
    global all_path
    matrix = interact.create_matrix(n)
    length = len(matrix)
    all_path = [[0] * length for _ in range(length)]
    for top in range(n):
        threads = []
        for i in range(n):
            thread = threading.Thread(target=update_path, args=(i, top, matrix))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
    for i in range(n):
        if matrix[i][i] < 0:
            raise ValueError("Отрицательный цикл обнаружен! Алгоритм Флойда работает некорректно!")
    return all_path, matrix


def get_path(shortest_vertex, end: int, start: int) -> tuple:
    """
    Функция, которая возвращает полный путь от конечной точки к начальной.
    :param shortest_vertex: Матрица путей, которая показывает вершину, соединяющую эти точки.
    :param end: Конечная точка.
    :param start: Начальная точка.
    """
    shortest_path_matrix, distance_matrix = shortest_vertex
    path, summary = [end], 0
    while end != start:

        if shortest_path_matrix[end][start] == 0:
            path.insert(0, start)
            summary += distance_matrix[end][start]
            break

        new_point = shortest_path_matrix[end][start]
        summary += distance_matrix[end][new_point]
        end = new_point
        path.insert(0, end)

    return [chr(65 + vertex) for vertex in path], summary