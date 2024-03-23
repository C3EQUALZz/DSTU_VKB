"""
Здесь описан класс графа, который мне нужен для поиска в ширину
"""
from collections import defaultdict, deque
from collections.abc import MutableMapping, MutableSet
from copy import deepcopy


class Graph:
    def __init__(self, transitions: MutableMapping[str, MutableMapping[str, MutableSet[str]]]) -> None:
        self.transitions = deepcopy(transitions)
        self._graph = defaultdict(set)
        self._convert_to_graph()

    def _convert_to_graph(self) -> None:
        """
        Из функций перехода конвертирует в граф (нам не нужно знать по какой букве переходит)
        Выглядит так:
            graph = {'A': set(['B', 'C']),
             'B': set(['A', 'D', 'E']),
             'C': set(['A', 'F']),
             'D': set(['B']),
             'E': set(['B', 'F']),
             'F': set(['C', 'E'])}
        """
        for key, dict_values in self.transitions.items():
            for _, value in dict_values.items():
                self._graph[key].update(value)

    def bfs(self) -> MutableSet[str]:
        """
        Здесь используется алгоритм обхода поиска в ширину
        Ссылка на источник:
        - https://www.easydoit.ru/python/kak-obojti-graf-v-shirinu-na-python-principy-sovety-i-primery-koda/
        """
        visited: set[str] = set()
        queue: deque[str] = deque([next(iter(self.transitions))])

        while queue:
            vertex = queue.popleft()

            if vertex not in visited:
                visited.add(vertex)
                queue.extend(self._graph[vertex] - visited)

        return visited
