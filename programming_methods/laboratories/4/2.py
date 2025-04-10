"""
Задача №165. Банкет

На банкет были приглашены N Очень Важных Персон (ОВП).
Были поставлены 2 стола. Столы достаточно большие, чтобы все посетители банкета могли сесть за любой из них.
Проблема заключается в том, что некоторые ОВП не ладят друг с другом и не могут сидеть за одним столом.
Вас попросили определить, возможно ли всех ОВП рассадить за двумя столами.

Входные данные

В первой строке входных данных содержатся два числа: N и M (1 <= N, M <= 100),
где N – количество ОВП, а M – количество пар ОВП, которые не могут сидеть за одним столом.
В следующих M строках записано по 2 числа – пары ОВП, которые не могут сидеть за одним столом.

Выходные данные

Если способ рассадить ОВП существует, то выведите YES в первой строке и номера ОВП, которых необходимо посадить за
первый стол, во второй строке. В противном случае в первой и единственной строке выведите NO.
"""

from collections import deque
from typing import List, Tuple, cast


class Graph:
    def __init__(self, n: int) -> None:
        """Инициализируем граф с n вершинами."""
        self._n = n
        self._adj_list: List[List[int]] = [
            [] for _ in range(n)
        ]  # Список смежности для графа
        self._color: List[int] = []

    def add_edge(self, u: int, v: int) -> None:
        """Добавляем ребро между вершинами u и v."""
        self._adj_list[u - 1].append(v - 1)
        self._adj_list[v - 1].append(u - 1)

    def is_bipartite(self) -> bool:
        """
        Проверяет, является ли граф двудольным.

        Использует обход в ширину (BFS) для проверки, можно ли раскрасить граф в два цвета
        так, чтобы соседние вершины имели разные цвета

        :returns: True, если граф двудольный.
        """
        self._color = [-1] * self._n  # -1: не окрашена, 0: первая доля, 1: вторая доля

        def bfs(start_inner: int) -> bool:
            """
            Выполняет обход в ширину для проверки двудольности графа.

            :param start_inner: Начальная вершина для обхода.

            :returns: True, если граф двудольный относительно начальной вершины, иначе False.
            """
            queue: deque[int] = deque([start_inner])
            self._color[start_inner] = 0
            while queue:
                v = queue.popleft()
                for u in self._adj_list[v]:
                    if self._color[u] == -1:
                        self._color[u] = 1 - self._color[v]
                        queue.append(u)
                    elif self._color[u] == self._color[v]:
                        return False
            return True

        for start in range(self._n):
            if self._color[start] == -1 and not bfs(start):  # Если вершина не посещена
                return False
        return True

    @property
    def bipartite_partition(self) -> List[int]:
        """
        Возвращает список вершин первой доли графа, если он двудольный.

        :returns: Список вершин первой доли (индексы начинаются с 1), если граф двудольный, иначе пустой список.
        """
        if self.is_bipartite():
            return [i + 1 for i in range(self._n) if self._color[i] == 0]
        return []


def main() -> None:
    n, m = map(int, input().split())
    pairs = cast(
        List[Tuple[int, int]], [tuple(map(int, input().split())) for _ in range(m)]
    )

    # Создаем граф и добавляем ребра
    graph = Graph(n)
    for u, v in pairs:
        graph.add_edge(u, v)

    # Проверяем, возможно ли рассадить
    result = graph.bipartite_partition

    if result:
        print("YES")
        print(*result)
    else:
        print("NO")


if __name__ == "__main__":
    main()
