"""
Задача №2781. Декартово дерево

Вам даны пары чисел (ai,bi), Вам необходимо построить декартово дерево, такое что i-ая вершина имеет ключи (ai,bi),
вершины с ключом ai образуют бинарное дерево поиска, а вершины с ключом bi образуют кучу на минимум.

Входные данные

В первой строке записано число N — количество пар.
Далее следует N (1≤N≤50000) пар (ai,bi). Для всех пар |ai|,|bi|≤30000. ai≠aj и bi≠bj для всех i≠j.

Выходные данные

Если декартово дерево с таким набором ключей построить возможно, выведите в первой строке YES, в противном случае выведите NO.
В случае ответа YES, выведите N строк, каждая из которых должна описывать вершину.
Описание вершины состоит из трёх чисел: номер предка, номер левого сына и номер правого сына.
Если у вершины отсутствует предок или какой-либо из сыновей, то выводите на его месте число 0.

Если подходящих деревьев несколько, выведите любое.
"""

from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple, cast


@dataclass
class Vertex:
    """
    Класс для представления вершины декартова дерева.

    Атрибуты:
        x (int): Ключ для бинарного дерева поиска.
        y (int): Приоритет для свойства кучи.
        label (int): Уникальная метка вершины.
        parent (Optional[Vertex]): Родительская вершина.
        left (Optional[Vertex]): Левая дочерняя вершина.
        right (Optional[Vertex]): Правая дочерняя вершина.
    """

    x: int
    y: int
    label: int
    parent: Optional["Vertex"] = None
    left: Optional["Vertex"] = None
    right: Optional["Vertex"] = None


class DecTree:
    def __init__(self, pairs: List[Tuple[int, int]]) -> None:
        """
        Класс для представления декартова дерева.
        :param pairs: Список пар (x, y), где x — ключ, а y — приоритет.
        """
        self.__vertices = [
            Vertex(x=a, y=b, label=i + 1) for i, (a, b) in enumerate(pairs)
        ]
        self.ordered = sorted(self.vertices, key=lambda v: v.x)
        self.root: Optional[Vertex] = None

        self._build_tree()

    @property
    def vertices(self) -> Sequence[Vertex]:
        """
        Возвращает список всех вершин дерева.
        :returns: Возвращает список всех вершин дерева.
        """
        return self.__vertices

    def is_empty(self) -> bool:
        """
        Проверяет, пусто ли дерево.
        :returns: True, если дерево пусто, иначе False.
        """
        return len(self.vertices) == 0

    def _build_tree(self) -> None:
        """
        Строит декартово дерево, удовлетворяющее свойствам бинарного дерева поиска и кучи на минимум.

        Алгоритм:
            1. Упорядочиваем вершины по ключу x (для бинарного дерева поиска).
            2. Начинаем с первой вершины как корня.
            3. Для каждой следующей вершины ищем место в дереве:
                - Если приоритет вершины y больше, поднимаем её вверх, переставляя связи.
                - Если приоритет y меньше, добавляем вершину в правого потомка текущей.
            4. Поддерживаем свойства бинарного дерева поиска (по ключу x) и кучи (по y).
        """
        self.root = self.ordered[0]
        last = self.root

        for vertex in self.ordered[1:]:
            # Найти корректное место для новой вершины в декартовом дереве
            while last and last.parent and vertex.y < last.y:
                last = last.parent

            if vertex.y >= last.y:
                vertex.left = last.right
                vertex.parent = last
                if last.right:
                    last.right.parent = vertex
                last.right = vertex
            else:
                vertex.left = last
                last.parent = vertex
                self.root = vertex

            last = vertex

    def __str__(self) -> str:
        """
        Возвращает строковое представление дерева для вывода.

        Формат:
            Для каждой вершины выводятся три числа:
                1. Метка родителя (0, если родителя нет).
                2. Метка левого сына (0, если сына нет).
                3. Метка правого сына (0, если сына нет).

        :returns: Строка с описанием всех вершин дерева.
        """
        result: List[Tuple[int, int, int]] = [
            (
                v.parent.label if v.parent else 0,
                v.left.label if v.left else 0,
                v.right.label if v.right else 0,
            )
            for v in self.vertices
        ]

        return "\n".join(" ".join(map(str, collection)) for collection in result)


def main() -> None:
    n: int = int(input())
    pairs: List[Tuple[int, int]] = cast(
        List[Tuple[int, int]], [tuple(map(int, input().split())) for _ in range(n)]
    )
    tree: DecTree = DecTree(pairs)

    if tree.is_empty():
        print("NO")
    else:
        print("YES", tree, sep="\n")


if __name__ == "__main__":
    main()
