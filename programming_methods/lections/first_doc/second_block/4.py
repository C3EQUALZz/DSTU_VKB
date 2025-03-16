# Реверс строки с помощью стека
from collections import deque


def reverse_string(string: str) -> str:
    stack = deque((char for char in string))
    return "".join(stack.pop() for _ in range(len(stack)))


if __name__ == "__main__":
    print(reverse_string("hello"))
