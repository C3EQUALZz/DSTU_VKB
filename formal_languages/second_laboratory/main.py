"""
Реализация от Романа Карпова

Пример ввода:
R -> T1T
R -> T1U
R -> W
R -> E
T -> U
T -> T01
T -> T10
T -> E
U -> +U
U -> +0
U -> +1
W -> W-W
W -> W+W
V -> *0
V -> /1
exit
----------
0 1 + - / *


E -> E+T
E -> T
T -> T*F
T -> F
F -> (E)
F -> a
--------
a + * ( )
"""

from typing import AnyStr, List, Mapping, Set

from formal_languages.first_laboratory import is_context_free
from formal_languages.useful_functions import get_rules_from_console


def check_grammar_exist(
    grammar: Mapping[AnyStr, List[AnyStr]],
    set_of_non_terminals: Set[AnyStr],
    key="exist",
) -> bool | set[str]:
    """
    Проверка КС грамматики с помощью алгоритма, который описан в методичке
    Args:
        grammar (Mapping[AnyStr, List[AnyStr]]) - правила перехода, которые ввел пользователь
        set_of_non_terminals (Set[AnyStr) - множество не терминалов
        key: ...
    """
    # Стартовый символ всегда в самом начале правил, поэтому так сделал
    # Стартовый символ всегда в самом начале правил, поэтому так сделал
    start_symbol = next(iter(grammar))

    flag = False

    for non_terminal in set_of_non_terminals:
        # Наше множество, в которое мы будем добавлять элементы
        set_with_non_terminals = set()
        temporary_non_terminal = non_terminal
        for symbol, rules in reversed(grammar.items()):
            if any(temporary_non_terminal in rule for rule in rules) or any(
                non_terminal in rule for rule in rules
            ):
                set_with_non_terminals.add(symbol)
            else:
                continue
            temporary_non_terminal = symbol

        if start_symbol in set_with_non_terminals:
            if key == "exist":
                flag = True
                break
            else:
                return set_with_non_terminals
    return flag


def main() -> AnyStr:
    dictionary = get_rules_from_console("don't_remove")
    set_of_terminals = set(
        input("Введите множество терминалов через пробел: ").strip().split()
    )
    set_of_non_terminals = set(
        input("Введите множество не терминалов через пробел: ").strip().split()
    )

    if is_context_free(
        set_of_terminals=set_of_terminals,
        set_of_non_terminals=set_of_non_terminals,
        grammar=dictionary,
    ):
        return (
            f"1)Введена КС - грамматика\n2)"
            f"{'Язык существует' if check_grammar_exist(dictionary, set_of_non_terminals) else 'Язык не существует'}"
        )
    return "Введенная грамматика не является КС-грамматикой "


if __name__ == "__main__":
    print(main())
