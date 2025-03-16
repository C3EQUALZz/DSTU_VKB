from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional
from dataclasses import dataclass

T = TypeVar('T')


@dataclass
class _BaseNode(Generic[T]):
    """
    Узел дерева.
    """
    value: T
    left: Optional['_BaseNode[T]'] = None
    right: Optional['_BaseNode[T]'] = None

    def __str__(self) -> str:
        return str({self.value})


class BaseTree(ABC, Generic[T]):
    """
    Абстрактный базовый класс дерева.
    """

    def __init__(self):
        self.root: Optional[_BaseNode[T]] = None

    @abstractmethod
    def insert(self, value: T) -> None:
        """
        Метод вставки элемента в дерево.
        """
        ...

    @property
    def height(self) -> int:
        """
        Свойство, возвращающее высоту дерева.
        """
        return self._calculate_height(self.root)

    def _calculate_height(self, node: Optional[_BaseNode[T]]) -> int:
        """
        Рекурсивный метод подсчета высоты дерева от заданного узла.
        """
        if node is None:
            return 0

        return 1 + max(self._calculate_height(node.left), self._calculate_height(node.right))

    def is_empty(self) -> bool:
        """
        Проверка, пустое ли дерево.
        """
        return self.root is None

    def __str__(self) -> str:
        """
        Строковое представление дерева в виде псевдографики
        """
        if self.root is None:
            return "∅"

        matrix: list[list[str]] = self.__build_tree_matrix()
        self.__trim_empty_columns(matrix)
        return "\n".join("".join(row) for row in matrix)

    def __build_tree_matrix(self) -> list[list[str]]:
        """
        Строит матрицу символов для графического отображения структуры дерева
        """
        tree_height = self.height
        matrix_width = (2 ** tree_height) * 2
        matrix_height = tree_height * 2

        # Инициализируем матрицу пробелами
        matrix: list[list[str]] = [[' '] * matrix_width for _ in range(matrix_height)]
        root_column = 2 ** tree_height  # Стартовая позиция корня

        # Очередь для хранения узлов и их позиций на каждом уровне
        levels: list[list[tuple[_BaseNode[T], int]]] = [[(self.root, root_column)]]

        for level in range(tree_height):
            current_level = levels[level]
            next_level: list[tuple[_BaseNode[T], int]] = []

            for node, column in current_level:
                # Записываем значение узла в матрицу
                matrix[level * 2][column] = str(node.value)

                # Обрабатываем соединения с потомками
                if node.left or node.right:
                    self._add_children_connections(matrix, level, column, node, tree_height, next_level)

            levels.append(next_level)

        return matrix

    def _add_children_connections(
            self,
            matrix: list[list[str]],
            level: int,
            parent_col: int,
            node: _BaseNode[T],
            tree_height: int,
            next_level: list[tuple[_BaseNode[T], int]]
    ) -> None:
        """
        Добавляет символы соединений для левого и правого потомков
        """
        connector_row = matrix[level * 2 + 1]
        horizontal_shift = 2 ** (tree_height - level - 1)

        # Левый потомок
        if node.left:
            left_child_col = parent_col - horizontal_shift
            next_level.append((node.left, left_child_col))
            connector_row[left_child_col] = "┌"
            connector_row[parent_col] = "┴" if node.right else "┘"
            self._fill_horizontal_line(connector_row, left_child_col + 1, parent_col - 1)

        # Правый потомок
        if node.right:
            right_child_col = parent_col + horizontal_shift
            next_level.append((node.right, right_child_col))
            connector_row[right_child_col] = "┐"
            connector_row[parent_col] = "┴" if node.left else "└"
            self._fill_horizontal_line(connector_row, parent_col + 1, right_child_col - 1)

    @staticmethod
    def _fill_horizontal_line(row: list[str], start: int, end: int) -> None:
        """Заполняет горизонтальную линию между двумя точками"""
        for i in range(start, end + 1):
            row[i] = "─"

    @staticmethod
    def __trim_empty_columns(matrix: list[list[str]]) -> None:
        """
        Удаляет пустые колонки в матрице для компактного отображения
        """
        if not matrix:
            return

        # Ищем полностью пустые колонки
        empty_columns: list[int] = []
        for col_idx in range(len(matrix[0])):
            if all(row[col_idx] == ' ' for row in matrix):
                empty_columns.append(col_idx)

        # Удаляем найденные пустые колонки
        for row in matrix:
            for idx in reversed(empty_columns):
                del row[idx]
