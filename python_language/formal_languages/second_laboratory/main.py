"""
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

from itertools import chain
from typing import Mapping, Set, List, AnyStr
from python_language.formal_languages.first_laboratory import is_context_free
from python_language.formal_languages.useful_functions import get_rules_from_console


def check_grammar_existence(grammar: Mapping[AnyStr, List[AnyStr]], set_of_non_terminals: Set[AnyStr]) -> bool:
    """
    Проверка КС грамматики с помощью алгоритма, который описан в методичке
    Args:
        grammar (Mapping[AnyStr, List[AnyStr]]) - правила перехода, которые ввел пользователь
        set_of_non_terminals (Set[AnyStr) - множество не терминалов
    """
    # Стартовый символ всегда в самом начале правил, поэтому так сделал
    start_symbol = next(iter(grammar))

    # Наше множество, в которое мы будем добавлять элементы
    set_with_non_terminals = {start_symbol}

    max_length = 0

    # Из примера я понял, что нужно рассматривать каждый отдельный символ S -> AB ---> A B, а не слитно
    for symbol in chain.from_iterable(rule for rules in grammar.values() for rule in rules):

        if symbol in set_with_non_terminals | set_of_non_terminals:
            set_with_non_terminals.add(symbol)

        if max_length == (length := len(set_with_non_terminals)):
            break
        else:
            max_length = length

    return start_symbol in set_with_non_terminals


def main() -> AnyStr:
    dictionary = get_rules_from_console("don't_remove")
    set_of_terminals = set(input("Введите множество терминалов через пробел: ").strip().split())
    set_of_non_terminals = set(input("Введите множество не терминалов через пробел: ").strip().split())

    if is_context_free(set_of_terminals=set_of_terminals,
                       set_of_non_terminals=set_of_non_terminals,
                       grammar=dictionary):

        return (f"1)Введена КС - грамматика\n2)"
                f"{('Язык не существует', 'Язык существует')
                    [check_grammar_existence(dictionary, set_of_non_terminals)]}")

    return "1)Введенная грамматика не является КС-грамматикой "


if __name__ == "__main__":
    print(main())
