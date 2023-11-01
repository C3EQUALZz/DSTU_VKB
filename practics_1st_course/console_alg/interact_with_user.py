#!/usr/bin/env python3.11+
"""
Главный модуль, где происходит взаимодействие с пользователем.
Для данной программы нужен Python 3.11 и выше.
На данный момент не продумана работоспособность на Windows.
"""

__version__ = '0.1'
__author__ = 'Данил Ковалев ВКБ12 c3equalz'

from itertools import permutations, combinations
from math import inf
from string import ascii_letters
from time import sleep
from typing import Callable

from colorama import Fore

import algorithm_console as alg
from decorators import progress_bar, retry_on_value_error, pprint_matrix
from visual import graph

approval = ('да', 'y', 'yes', 'ofc')


@progress_bar
@retry_on_value_error
def questionary() -> tuple[tuple[list[list], list[list]], tuple]:
    """
    Функция, которая задает начальные данные для остальных функций
    """
    start_node = input(Fore.LIGHTWHITE_EX + '\nВведите начальную вершину по лексикограф. порядку (буква англ.) ')
    end_node = input('Введите конечную вершину по лексикограф порядку (буква англ.) ')
    start_node, end_node = sorted((start_node, end_node))

    find_start = input("Введите начало (c какой вершины поиск): ")
    find_end = input("Введите конец: ")
    params = (end_node, start_node, find_end, find_start)

    check: Callable[[str], bool] = lambda alpha: len(alpha) == (alpha in ascii_letters)
    if all(check(i) for i in params) and start_node != end_node:
        params = map(lambda x: ord(x.title()) - 65, params)
        info_for_graph = alg.floyd(next(params) - next(params) + 1)
        shortest_path = alg.get_path(info_for_graph, next(params), next(params))
        return info_for_graph, shortest_path
    raise ValueError()


@retry_on_value_error
@pprint_matrix
def create_matrix(n: int) -> list[list[int]]:
    """
    Функция создания матрицы смежности на основе входных данных с консоли
    :param n: количество вершин
    :return: матрицу для алгоритма Флойда
    """
    comment = "Введите какой граф вы изначально хотите (oriented, undirected)? По умолчанию undirected. "
    generate_iter = permutations if input(comment).lower() == 'oriented' else combinations
    matrix = [[inf if i != j else 0 for i in range(n)] for j in range(n)]
    for start, end in generate_iter(range(n), 2):
        query = input(f"Есть ли направленное ребро между {chr(65 + start)} и {chr(65 + end)}? ")
        if query.lower() in approval:
            matrix[start][end] = int(input('Введите вес '))
            matrix[end][start] = matrix[start][end] if generate_iter is combinations else matrix[end][start]
    graph(matrix)
    return matrix


def main() -> None:
    info_for_graph, shortest_path = questionary()
    print(f"Самый короткий путь - это {shortest_path[0]} c весом {shortest_path[1]}")
    sleep(3)
    graph(info_for_graph[1])


if __name__ == "__main__":
    main()