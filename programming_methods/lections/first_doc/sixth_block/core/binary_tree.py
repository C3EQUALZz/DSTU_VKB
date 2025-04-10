from collections import deque

from programming_methods.lections.first_doc.sixth_block.core.base import (
    BaseTree, T, _BaseNode)


class BinaryTree(BaseTree[T]):
    """
    Простое бинарное дерево.
    """

    def insert(self, value: T) -> None:
        """
        Просто вставляем значения по уровням (лево -> право)
        """
        new_node = _BaseNode(value)
        if self.root is None:
            self.root = new_node
        else:
            self._insert_level_order(self.root, new_node)

    @staticmethod
    def _insert_level_order(node: _BaseNode[T], new_node: _BaseNode[T]) -> None:
        queue = deque([node])
        while queue:
            current = queue.popleft()

            if current.left is None:
                current.left = new_node
                return
            else:
                queue.append(current.left)

            if current.right is None:
                current.right = new_node
                return
            else:
                queue.append(current.right)
