"""
Обязательно для просмотра, чтобы понимать материал:
 1. https://youtu.be/XvDdCQxCYJ0?si=jTHna1pSAHafhEVJ
 2. https://www.youtube.com/watch?v=fM5UiCAFyIU
"""
import re
from typing import Pattern, AnyStr
from collections import defaultdict


def is_left_linear(grammar: dict[str, list[str]]) -> bool:
    """
    Лево линейная регулярная грамматика
    A ⇢ Bx
    A ⇢ x
    where A,B ∈ V and x ∈ T*
    ---

    >>> is_left_linear({"S": ["Ab"], "A": ["Ab", "Za"], "Z": ["Za", "$"]})
    True

    """
    pattern = re.compile(r'^[A-Z] -> [A-Za-z]+[A-Z]?$')
    return _is_linear(grammar=grammar, pattern=pattern)


def is_right_linear(grammar: dict[str, list[str]]) -> bool:
    """
    Правая линейная регулярная грамматика
    A ⇢ xB
    A ⇢ x
    where A, B ∈ V and x ∈ T*
    ---

    >>> is_right_linear({"S": ["aS", "aA"], "A": ["bA", "bZ"], "Z": ["$"]})
    True

    """
    pattern = re.compile(r'^[A-Z] -> [a-z][A-Za-z]*')
    return _is_linear(grammar=grammar, pattern=pattern)


def is_context_sensitive(grammar: dict[str, list[str]]) -> bool:
    """

    """
    pattern = re.compile(r'^[A-Z]')


def is_context_free(grammar: dict[str, list[str]]) -> bool:
    """

    """
    ...


def _is_linear(grammar: dict[str, list[str]], pattern: Pattern[AnyStr]) -> bool:
    """
    В данную функцию передают саму грамматику, которую пользователь ввел с консоли и паттерн для проверки.
    """
    for non_terminal, rules in grammar.items():
        return all(pattern.match(f"{non_terminal} -> {rule}") for rule in rules)


def main():
    dictionary = defaultdict(list)
    print("Сейчас вы будете вводить грамматики. Пример ввода: S -> aSb")

    while (args := input("Введите вашу грамматику. Например, ")) != "exit":
        key, value = map(lambda x: x.rstrip("|E"), args.split())
        dictionary[key].append(value)

    if is_left_linear(dictionary):
        return "Тип 3: регулярная лево линейная грамматика"

    if is_right_linear(dictionary):
        return "Тип 3: регулярная право линейная грамматика"

    if is_context_free(dictionary):
        return "Тип 2: контекстно-свободная грамматика"

    if is_context_sensitive(dictionary):
        return "Тип 1: контекстно-зависимая грамматика"

    return "Грамматика типа 0"


if __name__ == "__main__":
    print(main())
