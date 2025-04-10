# Реализовать cтек с помощью очереди

from collections import deque
from typing import Generic, TypeVar

T = TypeVar("T")


class Stack(Generic[T]):
    def __init__(self) -> None:
        self.queue: deque[T] = deque()

    def push(self, item: T) -> None:
        # Добавляем элемент в очередь
        self.queue.append(item)

    def pop(self) -> T:
        # Удаляем и возвращаем верхний элемент стека
        if self.is_empty():
            raise IndexError("pop from an empty stack")

        self.queue.rotate(-1)

        return self.queue.popleft()  # Возвращаем последний элемент

    def top(self) -> T:
        # Возвращаем верхний элемент стека без удаления
        if self.is_empty():
            raise IndexError("top from an empty stack")

        # Перемещаем все элементы, чтобы получить верхний элемент
        for _ in range(len(self.queue) - 1):
            self.queue.append(self.queue.popleft())

        top_item = self.queue.popleft()  # Сохраняем верхний элемент
        self.queue.append(top_item)  # Возвращаем его обратно в очередь
        return top_item

    def is_empty(self) -> bool:
        # Проверяем, пуст ли стек
        return len(self.queue) == 0

    def size(self) -> int:
        # Возвращаем размер стека
        return len(self.queue)


# Пример использования
stack = Stack()
stack.push(1)
stack.push(2)
stack.push(3)

print(stack.top())  # Вывод: 3
print(stack.pop())  # Вывод: 3
print(stack.size())  # Вывод: 2
print(stack.is_empty())  # Вывод: False
