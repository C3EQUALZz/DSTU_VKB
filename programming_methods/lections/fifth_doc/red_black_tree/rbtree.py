from dataclasses import dataclass
from enum import Enum
from typing import Generic, List, Optional, Self, TypeVar

T = TypeVar("T")


class NodeColor(Enum):
    RED = "RED"
    BLACK = "BLACK"


@dataclass
class RBNode(Generic[T]):
    key: Optional[T] = None
    color: NodeColor = NodeColor.RED
    left: Optional[Self] = None
    right: Optional[Self] = None
    parent: Optional[Self] = None


class RBTree(Generic[T]):
    def __init__(self) -> None:
        self.sentinel: RBNode[T] = RBNode(key=None, color=NodeColor.BLACK)
        self.root: RBNode[T] = self.sentinel

    def insert(self, key: T) -> None:
        new_node: RBNode[T] = RBNode(key=key, left=self.sentinel, right=self.sentinel)
        parent = None
        current = self.root

        while current != self.sentinel:
            parent = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                return  # Duplicate keys not allowed

        new_node.parent = parent
        if parent is None:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self._fix_insertion(new_node)

    def _left_rotate(self, node: RBNode[T]) -> None:
        right_child = node.right
        node.right = right_child.left

        if right_child.left != self.sentinel:
            right_child.left.parent = node

        right_child.parent = node.parent

        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child

        right_child.left = node
        node.parent = right_child

    def _right_rotate(self, node: RBNode[T]) -> None:
        left_child = node.left
        node.left = left_child.right

        if left_child.right != self.sentinel:
            left_child.right.parent = node

        left_child.parent = node.parent

        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child

        left_child.right = node
        node.parent = left_child

    def _fix_insertion(self, node: RBNode[T]) -> None:
        while node.parent and node.parent.color == NodeColor.RED:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color == NodeColor.RED:
                    node.parent.color = NodeColor.BLACK
                    uncle.color = NodeColor.BLACK
                    node.parent.parent.color = NodeColor.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    node.parent.color = NodeColor.BLACK
                    node.parent.parent.color = NodeColor.RED
                    self._right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.color == NodeColor.RED:
                    node.parent.color = NodeColor.BLACK
                    uncle.color = NodeColor.BLACK
                    node.parent.parent.color = NodeColor.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.color = NodeColor.BLACK
                    node.parent.parent.color = NodeColor.RED
                    self._left_rotate(node.parent.parent)

        self.root.color = NodeColor.BLACK

    def delete(self, key: T) -> None:
        if (node_to_delete := self.search(key)) is None:
            return

        original_color = node_to_delete.color
        if node_to_delete.left == self.sentinel:
            x = node_to_delete.right
            self._replace_node(node_to_delete, node_to_delete.right)
        elif node_to_delete.right == self.sentinel:
            x = node_to_delete.left
            self._replace_node(node_to_delete, node_to_delete.left)
        else:
            successor = self._find_min(node_to_delete.right)
            original_color = successor.color
            x = successor.right
            if successor.parent == node_to_delete:
                x.parent = successor
            else:
                self._replace_node(successor, successor.right)
                successor.right = node_to_delete.right
                successor.right.parent = successor

            self._replace_node(node_to_delete, successor)
            successor.left = node_to_delete.left
            successor.left.parent = successor
            successor.color = node_to_delete.color

        if original_color == NodeColor.BLACK:
            self._fix_deletion(x)

    def _replace_node(self, old_node: RBNode[T], new_node: RBNode[T]) -> None:
        if old_node.parent is None:
            self.root = new_node
        elif old_node == old_node.parent.left:
            old_node.parent.left = new_node
        else:
            old_node.parent.right = new_node
        new_node.parent = old_node.parent

    def _fix_deletion(self, node: RBNode[T]) -> None:
        while node != self.root and node.color == NodeColor.BLACK:
            if node == node.parent.left:
                sibling = node.parent.right
                if sibling.color == NodeColor.RED:
                    sibling.color = NodeColor.BLACK
                    node.parent.color = NodeColor.RED
                    self._left_rotate(node.parent)
                    sibling = node.parent.right

                if (
                    sibling.left.color == NodeColor.BLACK
                    and sibling.right.color == NodeColor.BLACK
                ):
                    sibling.color = NodeColor.RED
                    node = node.parent
                else:
                    if sibling.right.color == NodeColor.BLACK:
                        sibling.left.color = NodeColor.BLACK
                        sibling.color = NodeColor.RED
                        self._right_rotate(sibling)
                        sibling = node.parent.right

                    sibling.color = node.parent.color
                    node.parent.color = NodeColor.BLACK
                    sibling.right.color = NodeColor.BLACK
                    self._left_rotate(node.parent)
                    node = self.root
            else:
                sibling = node.parent.left
                if sibling.color == NodeColor.RED:
                    sibling.color = NodeColor.BLACK
                    node.parent.color = NodeColor.RED
                    self._right_rotate(node.parent)
                    sibling = node.parent.left

                if (
                    sibling.left.color == NodeColor.BLACK
                    and sibling.right.color == NodeColor.BLACK
                ):
                    sibling.color = NodeColor.RED
                    node = node.parent
                else:
                    if sibling.left.color == NodeColor.BLACK:
                        sibling.right.color = NodeColor.BLACK
                        sibling.color = NodeColor.RED
                        self._left_rotate(sibling)
                        sibling = node.parent.left

                    sibling.color = node.parent.color
                    node.parent.color = NodeColor.BLACK
                    sibling.left.color = NodeColor.BLACK
                    self._right_rotate(node.parent)
                    node = self.root

        node.color = NodeColor.BLACK

    def search(self, key: T) -> Optional[RBNode[T]]:
        current = self.root
        while current != self.sentinel and current.key != key:
            current = current.left if key < current.key else current.right
        return current if current != self.sentinel else None

    def _find_min(self, node: RBNode[T]) -> RBNode[T]:
        while node.left != self.sentinel:
            node = node.left
        return node

    def preorder_traversal(self, node: RBNode[T]) -> List[str]:
        if node == self.sentinel:
            return []
        return [
            f"{node.key}({node.color.value})",
            *self.preorder_traversal(node.left),
            *self.preorder_traversal(node.right),
        ]

    def inorder_traversal(self, node: RBNode[T]) -> List[str]:
        if node == self.sentinel:
            return []
        return [
            *self.inorder_traversal(node.left),
            f"{node.key}({node.color.value})",
            *self.inorder_traversal(node.right),
        ]

    def postorder_traversal(self, node: RBNode[T]) -> List[str]:
        if node == self.sentinel:
            return []
        return [
            *self.postorder_traversal(node.left),
            *self.postorder_traversal(node.right),
            f"{node.key}({node.color.value})",
        ]
