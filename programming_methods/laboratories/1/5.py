"""
Задача №51. Правильная скобочная последовательность

Рассмотрим последовательность, состоящую из круглых, квадратных и фигурных скобок.
Программа должна определить, является ли данная скобочная последовательность правильной.

Пустая последовательность является правильной. Если A – правильная, то последовательности (A), [A], {A} – правильные.
Если A и B – правильные последовательности, то последовательность AB – правильная.
"""
from collections import deque


def is_balanced(sequence: str) -> str:
    """Проверяет, является ли последовательность скобок правильной."""
    stack = deque()
    matching_brackets = {')': '(', '}': '{', ']': '['}

    for char in sequence:
        if char in matching_brackets.values():  # Открывающая скобка
            stack.append(char)
        elif char in matching_brackets.keys():  # Закрывающая скобка
            if stack and stack[-1] == matching_brackets[char]:
                stack.pop()
            else:
                return 'no'

    return 'yes' if not stack else 'no'


def main() -> None:
    sequence = input()
    result = is_balanced(sequence)
    print(result)


if __name__ == "__main__":
    main()
