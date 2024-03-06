"""
Обязательно для просмотра, чтобы понимать материал:
 1. https://youtu.be/XvDdCQxCYJ0?si=jTHna1pSAHafhEVJ
 2. https://www.youtube.com/watch?v=fM5UiCAFyIU
"""
import re
from typing import Pattern, AnyStr
from python_language.formal_languages.useful_functions import get_rules_from_console


def is_left_linear(grammar: dict[str, list[str]]) -> bool:
    """
    Лево линейная регулярная грамматика
    A ⇢ Bx
    A ⇢ x
    where A, B ∈ V and x ∈ T*
    ---
    Пример:

    S -> Ab
    A -> Ab
    A -> Za
    Z -> Za
    Z -> $
    """
    pattern = re.compile(r'^[A-Z] -> (?:[A-Z]+[^A-Z]|\W+)$')
    return _checker(grammar=grammar, pattern=pattern)


def is_right_linear(grammar: dict[str, list[str]]) -> bool:
    """
    Правая линейная регулярная грамматика
    A ⇢ xB
    A ⇢ x
    where A, B ∈ V and x ∈ T*
    ---
    Пример:

    S -> aS
    S -> aA
    A -> bA
    A -> bZ
    Z -> $
    """
    pattern = re.compile(r'^[A-Z] -> (?:[^A-Z]*[A-Z]|\W+)')
    return _checker(grammar=grammar, pattern=pattern)


def is_context_sensitive(grammar: dict[str, list[str]]) -> bool:
    """
    Контекстно-зависимая грамматика (КЗ-грамматика, контекстная грамматика) — частный случай формальной
    грамматики (тип 1 по иерархии Хомского), у которой левые и правые части всех продукций могут быть
    окружены терминальными и нетерминальными символами.
    ---
    Пример:

    S -> aAS
    AS -> AAS
    AAA -> ABA
    A -> b
    bBA -> bcdA
    bS -> ba
    """
    for key, value in grammar.items():
        if len(key) <= len(value):
            return True
    return False


def is_context_free(grammar: dict[str, list[str]]) -> bool:
    """
    Проверяет, что является контекстно-свободной грамматикой.
    ---
    Пример:

    S -> aSa
    S -> bSb
    S -> aa
    I -> bb
    """
    pattern = re.compile(r'^[A-Z] -> (?:[A-Za-z]+|\W)')
    return _checker(grammar=grammar, pattern=pattern)


def _checker(grammar: dict[str, list[str]], pattern: Pattern[AnyStr]) -> bool:
    """
    В данную функцию передают саму грамматику, которую пользователь ввел с консоли и паттерн для проверки.
    """
    for first_half, second_half in grammar.items():
        if not all(pattern.fullmatch(f"{first_half} -> {second_half_el}") for second_half_el in second_half):
            return False
    return True


def main():
    dictionary = get_rules_from_console()

    if is_left_linear(dictionary):
        return "Тип 3: регулярная лево линейная грамматика"

    if is_right_linear(dictionary):
        return "Тип 3: регулярная право линейная грамматика"

    if is_context_free(dictionary):
        return "Тип 2: контекстно-свободная грамматика"

    if is_context_sensitive(dictionary):
        return "Тип 1: контекстно-зависимая грамматика"

    # xAbCD -> xHD
    return "Грамматика типа 0"


if __name__ == "__main__":
    print(main())
