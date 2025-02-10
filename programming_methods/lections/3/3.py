# Генерация двоичных чисел от 1 до N с помощью очереди

from collections import deque


def generate_binary_numbers(n):
    # Создаем очередь и добавляем первое двоичное число
    queue = deque()
    queue.append("1")

    binary_numbers = []

    for _ in range(n):
        # Извлекаем элемент из очереди
        current = queue.popleft()
        binary_numbers.append(current)

        # Генерируем следующие двоичные числа
        queue.append(current + "0")
        queue.append(current + "1")

    return binary_numbers


def main() -> None:
    # Пример использования
    n = 10
    binary_numbers = generate_binary_numbers(n)
    print(binary_numbers)

if __name__ == "__main__":
    main()
