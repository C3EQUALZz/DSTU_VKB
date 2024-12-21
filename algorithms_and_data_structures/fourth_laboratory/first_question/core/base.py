from abc import ABC, abstractmethod
from collections import defaultdict
from typing import TypeVar, Generic, List, Dict

T = TypeVar('T')


class BaseGraph(ABC, Generic[T]):
    """
    Базовый граф, от которого Вы должны наследоваться.
    Частные случаи графов, которые реализовать должны:
    - Неориентированный граф
    - Ориентированный граф
    """

    def __init__(self) -> None:
        self._graph: Dict[T, List[T]] = defaultdict(list)

    @abstractmethod
    def add_edge(self, u: T, v: T) -> None:
        """
        Добавить дугу графа.
        :param u: Первая вершина графа.
        :param v: Вторая вершина графа.
        :returns: Ничего не возвращает.
        """
        ...

    def get_neighbors(self, node: T) -> List[T]:
        """
        Метод для получения соседних вершин.
        :param node: Вершина, у которой мы хотим найти соседей.
        :returns: Список соседних вершин
        """
        return self._graph[node]

    def __str__(self) -> str:
        return '\n'.join(f"{key}: {value}" for key, value in self._graph.items())
