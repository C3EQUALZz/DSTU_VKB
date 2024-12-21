from typing import TypeVar

from algorithms_and_data_structures.fourth_laboratory.first_question.core.base import BaseGraph

T = TypeVar('T')


class NonOrientedGraph(BaseGraph[T]):
    def add_edge(self, u: T, v: T) -> None:
        self._graph[u].append(v)
        self._graph[v].append(u)
