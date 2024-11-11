"""
Даны три целых числа. Определите, сколько среди них совпадающих.
Функция должна вернуть одно из чисел: 3 (если все совпадают), 2 (если два совпадает) или 0 (если все числа различны).
Тестовые данные:
- 1 2 3
- 3 3 3
- 15154352 1 15154352
"""

from typing import Iterable


def find_occurrences(numbers: Iterable[int]) -> int:
    return {1: 3, 2: 2, 3: 0}[len(set(numbers))]


def main() -> None:
    user_input = input("Введите 3 числа через пробел: ").strip().split()

    if all(x.isdigit() or (x[0] == "-" and x[1:].isdigit()) for x in user_input) and len(user_input) == 3:
        print(find_occurrences(map(int, user_input)))
    else:
        print("Неправильный ввод от пользователя")


if __name__ == '__main__':
    main()
