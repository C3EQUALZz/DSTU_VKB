# Реализовать очередь с помощью стека


from typing import TypeVar, Generic

T = TypeVar("T")

class Queue(Generic[T]):

    def __init__(self) -> None:
        self.current: T = []
        self.tmp: T = []

    def push(self, value: T) -> None:
        self.current.append(value)

    def pop(self) -> T:
        if len(self.tmp) == 0:

            while len(self.current) != 0:
                self.tmp.append(self.current.pop())

            return self.tmp.pop()

        return self.tmp.pop()

    def top(self) -> T:
        if len(self.tmp) == 0:
            while len(self.current) != 0:
                self.tmp.append(self.current.pop())
            return self.tmp[len(self.tmp) - 1]

        return self.tmp[len(self.tmp) - 1]

    def is_empty(self) -> bool:
        return bool((len(self.tmp) == 0) and (len(self.current) == 0))


a = Queue()

print(a.is_empty())