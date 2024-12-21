from abc import ABC, abstractmethod
from collections import defaultdict
from typing import TypeVar, Generic, List, Dict, Iterator

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

    def get_neighbors(self, node: T) -> List[T]:
        """
        Метод для получения соседних вершин.
        :param node: Вершина, у которой мы хотим найти соседей.
        :returns: Список соседних вершин
        """
        return self._graph[node]

    def __iter__(self) -> Iterator[T]:
        """
        Метод для итерации по вершинам графа.
        В данном контексте он нужен для in, чтобы я при вводе проверил наличие вершины в графе.
        :returns: Итератор по вершинам графа.
        """
        return iter(self._graph.keys())

    def __len__(self) -> int:
        return len(self._graph)

    @abstractmethod
    def __str__(self) -> str:
        """
        Метод для печати матрицы смежности, зная граф.
        """
        ...


class BaseUnWeightedGraph(BaseGraph[T], ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def add_edge(self, u: T, v: T) -> None:
        """
        Добавить дугу графа.
        :param u: Первая вершина графа.
        :param v: Вторая вершина графа.
        :returns: Ничего не возвращает.
        """
        ...


class BaseWeightedGraph(BaseGraph[T], ABC):
    def __init__(self) -> None:
        super().__init__()
        self._weights: Dict[T, Dict[T, float]] = defaultdict(dict)

    @abstractmethod
    def add_edge(self, u: T, v: T, weight: float) -> None:
        """
        Добавить дугу графа.
        :param u: Первая вершина графа.
        :param v: Вторая вершина графа.
        :param weight: Вес направления от 1 вершины к другой.
        :returns: Ничего не возвращает.
        """
        ...

    def get_weight(self, u: T, v: T) -> float:
        return self._weights[u].get(v, float('inf'))
