# Сортировка значений в стеке

from collections import deque
from typing import Protocol, TypeVar

T = TypeVar('T')


class StackProtocol(Protocol[T]):
    def pop(self) -> T:
        raise NotImplementedError

    def append(self, value: T) -> None:
        raise NotImplementedError


def sort_stack(s: StackProtocol[int]) -> deque[int]:
    temporary: deque[int] = deque()

    while s:
        x = s.pop()

        while temporary and temporary[-1] > x:
            s.append(temporary.pop())

        temporary.append(x)

    return temporary


print(sort_stack([1, 5, 4]))
