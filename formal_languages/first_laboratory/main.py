"""
Обязательно для просмотра, чтобы понимать материал:
 1. https://youtu.be/XvDdCQxCYJ0?si=jTHna1pSAHafhEVJ
 2. https://www.youtube.com/watch?v=fM5UiCAFyIU
 Мой вариант:
 S -> 0A0
 S -> 0B0
 A -> 1B1
 A -> 11
 B -> 0S0
 B -> 00
"""

import re
from typing import AnyStr, List, Mapping, Pattern, Set

from formal_languages.useful_functions import get_rules_from_console


def is_left_linear(
    *,
    set_of_terminals: Set[AnyStr],
    set_of_non_terminals: Set[AnyStr],
    grammar: Mapping[AnyStr, List[AnyStr]],
) -> bool:
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
    non_terminals = "|".join(map(re.escape, set_of_non_terminals))
    terminals = "|".join(map(re.escape, set_of_terminals))
    pattern = re.compile(
        rf"^({non_terminals}) -> (({non_terminals})*({terminals})+|ε)$"
    )

    return _checker(grammar=grammar, pattern=pattern)


def is_right_linear(
    *,
    set_of_terminals: Set[AnyStr],
    set_of_non_terminals: Set[AnyStr],
    grammar: Mapping[AnyStr, List[AnyStr]],
) -> bool:
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
    non_terminals = "|".join(map(re.escape, set_of_non_terminals))
    terminals = "|".join(map(re.escape, set_of_terminals))
    pattern = re.compile(
        rf"^({non_terminals}) -> (({terminals})+({non_terminals})*|ε)$"
    )

    return _checker(grammar=grammar, pattern=pattern)


def is_context_sensitive(
    *,
    set_of_terminals: Set[AnyStr],
    set_of_non_terminals: Set[AnyStr],
    grammar: Mapping[AnyStr, List[AnyStr]],
) -> bool:
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
    non_terminals = "|".join(map(re.escape, set_of_non_terminals))
    terminals = "|".join(map(re.escape, set_of_terminals))
    union_of_symbols = non_terminals + "|" + terminals
    pattern = re.compile(
        rf"^(({union_of_symbols})*({non_terminals})({union_of_symbols})*) -> (({union_of_symbols})+|ε)$"
    )

    return all(
        len(key) <= len(value) for key, values in grammar.items() for value in values
    ) and _checker(grammar=grammar, pattern=pattern)


def is_context_free(
    *,
    set_of_terminals: Set[AnyStr],
    set_of_non_terminals: Set[AnyStr],
    grammar: Mapping[AnyStr, List[AnyStr]],
) -> bool:
    """
    Проверяет, что является контекстно-свободной грамматикой.
    ---
    Пример:

    S -> aSa
    S -> bSb
    S -> aa
    I -> bb
    """

    terminals = "|".join(map(re.escape, set_of_terminals))
    non_terminals = "|".join(map(re.escape, set_of_non_terminals))
    union_of_symbols = non_terminals + "|" + terminals

    pattern = re.compile(rf"^({non_terminals}) -> (({union_of_symbols})*|ε)$")

    return _checker(grammar=grammar, pattern=pattern)


def _checker(grammar: Mapping[str, list[str]], pattern: Pattern[AnyStr]) -> bool:
    """
    В данную функцию передают саму грамматику, которую пользователь ввел с консоли и паттерн для проверки.
    """
    for first_half, second_half in grammar.items():
        if not all(
            pattern.fullmatch(f"{first_half} -> {second_half_el}")
            for second_half_el in second_half
        ):
            return False
    return True


def main():
    dictionary = get_rules_from_console("don't_remove")
    set_of_terminals = set(
        input("Введите множество терминалов через пробел: ").strip().split()
    )
    set_of_non_terminals = set(
        input("Введите множество не терминалов через пробел: ").strip().split()
    )

    if is_left_linear(
        set_of_terminals=set_of_terminals,
        set_of_non_terminals=set_of_non_terminals,
        grammar=dictionary,
    ):
        return "Тип 3: регулярная лево линейная грамматика"

    if is_right_linear(
        set_of_terminals=set_of_terminals,
        set_of_non_terminals=set_of_non_terminals,
        grammar=dictionary,
    ):
        return "Тип 3: регулярная право линейная грамматика"

    if is_context_free(
        set_of_terminals=set_of_terminals,
        set_of_non_terminals=set_of_non_terminals,
        grammar=dictionary,
    ):
        return "Тип 2: контекстно-свободная грамматика"

    if is_context_sensitive(
        set_of_terminals=set_of_terminals,
        set_of_non_terminals=set_of_non_terminals,
        grammar=dictionary,
    ):
        return "Тип 1: контекстно-зависимая грамматика"

    # xAbCD -> xHD
    return "Грамматика типа 0"


if __name__ == "__main__":
    print(main())
