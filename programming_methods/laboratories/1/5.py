"""
Задача №51. Правильная скобочная последовательность

Рассмотрим последовательность, состоящую из круглых, квадратных и фигурных скобок.
Программа должна определить, является ли данная скобочная последовательность правильной.

Пустая последовательность является правильной. Если A – правильная, то последовательности (A), [A], {A} – правильные.
Если A и B – правильные последовательности, то последовательность AB – правильная.
"""
from collections import deque
from typing import Dict


def is_balanced(sequence: str) -> bool:
    """
    Проверяет, является ли последовательность скобок правильной.
    Опять-таки классическая задача на стек, но в Python нет готового стека, поэтому я буду пользоваться деком.
    В словаре хранятся всевозможные пары, которые являются корректными.

    Если у нас текущая скобочка является открывающей, то мы добавляем в стек, в ином случае проверяем,
    что в стеке последнее.

    :param sequence: Последовательность скобочек из условия задания.
    :returns: True, если последовательность удовлетворяет условию задачи, в ином случае False
    """
    stack: deque[str] = deque()
    matching_brackets: Dict[str, str] = {')': '(', '}': '{', ']': '['}

    for char in sequence:
        if char in matching_brackets.values():
            stack.append(char)
        elif char in matching_brackets:
            if not (stack and stack[-1] == matching_brackets[char]):
                return False
            stack.pop()

    return not bool(stack)


def main() -> None:
    sequence = input()
    print("yes" if is_balanced(sequence) else "no")


if __name__ == "__main__":
    main()
