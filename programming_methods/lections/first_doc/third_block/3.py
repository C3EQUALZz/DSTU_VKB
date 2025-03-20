# Генерация двоичных чисел от 1 до N с помощью очереди

from collections import deque
from typing import Sequence


def generate_binary_numbers(n: int) -> Sequence[str]:
    # Создаем очередь и добавляем первое двоичное число
    queue: deque[str] = deque("1")

    binary_numbers: deque[str] = deque()

    for _ in range(n):
        # Извлекаем элемент из очереди
        current = queue.popleft()
        binary_numbers.append(current)

        # Генерируем следующие двоичные числа
        queue.extend((current + "0", current + "1"))

    return binary_numbers


def main() -> None:
    # Пример использования
    n = 10
    binary_numbers = generate_binary_numbers(n)
    print(binary_numbers)


if __name__ == "__main__":
    main()
