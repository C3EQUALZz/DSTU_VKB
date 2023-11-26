"""
Реализация односвязного списка без хвоста (Single Linked List without tail).
Здесь реализованы методы:
    - Поиск индекса элемента, зная только его значение (index);
    - Добавить в конец (append);
    - Обращения по индексу (__getitem__, __setitem__);
    - Вставка элемента по индексу (insert);
    - Удаление по индексу (remove);
    - Разворот односвязного списка (reverse);
"""

from typing import Any
from algorithms_and_data_structures.linked_list_python.node import Node
import sys

sys.tracebacklimit = 0


class LinkedList:

    @staticmethod
    def __index_error(func):
        def wrapper(self, *args, **kwargs):
            index, *_ = args
            if index < 0:
                raise IndexError("Negative index is not supported")
            if type(index) != int:
                raise ValueError("Index is only int")
            try:
                return func(self, *args, **kwargs)
            except AttributeError:
                raise IndexError("Index out of range") from None

        return wrapper

    def __init__(self):
        self.head = None

    def __str__(self):
        cur_node = self.head
        output = ""
        while cur_node is not None:
            output += str(cur_node.get_current()) + " -> "
            cur_node = cur_node.get_next()
        return output.rstrip(" -> ")

    def __len__(self):
        cur_node = self.head
        counter = 0
        while cur_node is not None:
            counter += 1
            cur_node = cur_node.get_next()
        return counter

    @__index_error
    def __getitem__(self, index: int) -> object:
        cur_node = self.head
        for _ in range(index):
            cur_node = cur_node.get_next()
        return cur_node.get_current()

    @__index_error
    def __setitem__(self, index: int, data: Any) -> None:
        cur_node = self.head
        for _ in range(index):
            cur_node = cur_node.get_next()
        cur_node.set_current(data)

    def append(self, data: Any) -> None:
        """
        Creates new node at the end of Linked List
        :param data: any object
        :return: None
        """
        if self.head is None:
            self.head = Node(data)
            return
        cur_node = self.head
        while cur_node.get_next() is not None:
            cur_node = cur_node.get_next()
        cur_node.set_next(Node(data))

    @__index_error
    def insert(self, index: int, data) -> None:
        """
        Creates a new node by the desired index of the linked list
        :param index: index in LinkedList, doesn't support negative numbers
        :param data: any object
        :return: None
        """
        new_node = Node(data)
        cur_node = self.head
        for i in range(index):
            if index == 0:
                new_node.set_next(self.head)
                self.head = new_node
                return
            if i + 1 == index:
                new_node.set_next(cur_node.get_next())
                cur_node.set_next(new_node)
                return
            cur_node = cur_node.get_next()

    def index(self, data) -> int:
        """
        Method that finds index of element
        :param data: any object
        :return: index of element
        """
        cur_node = self.head
        count = 0
        while cur_node is not None:
            if cur_node.get_current() == data:
                return count
            count += 1
            cur_node = cur_node.get_next()
        return -1

    @__index_error
    def remove(self, index: int) -> None:
        """
        delete element from LinkedList
        :param index: index of element
        :return: None
        """
        cur_node = self.head
        for i in range(index):
            if index == 0:
                self.head = cur_node.get_next()
                return
            if i + 1 == index:
                node_to_remove = cur_node.get_next()
                node_after_removed = node_to_remove.get_next()
                cur_node.set_next(node_after_removed)
                return
            cur_node = cur_node.get_next()

    def reverse(self):
        prev = next_node = None
        cur_node = self.head
        while cur_node is not None:
            next_node = cur_node.get_next()
            cur_node.set_next(prev)
            prev = cur_node
            cur_node = next_node
        self.head = prev