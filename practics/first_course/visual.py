"""
Отдельная сущность. Благодаря это функции из матрицы смежности можно получить граф.
"""
__all__ = ["graph"]

import math
from itertools import product

import matplotlib.pyplot as plt
import networkx as nx


def graph(matrix):
    g = nx.Graph()  # создаём объект графа
    length = len(matrix)
    nodes = [chr(x + 65) for x in range(length)]  # определяем список узлов (ID узлов)
    edges = [(chr(raw + 65), chr(column + 65)) for raw, column in product(range(length), repeat=2) if
             matrix[raw][column] not in (math.inf, 0)]
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)

    nx.draw(g, with_labels=True, font_weight='bold')
    plt.show()

