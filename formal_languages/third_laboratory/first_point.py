"""
Удаление бесполезных символов

Мой вариант:
R T U W V
--------
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


Пример ввода:
S R T
----
S -> R
S -> T
R -> pX
R -> paR
R -> paT
T -> Tg
T -> g
X -> aXb
Y -> aYa
Y -> y|E
exit
"""
from formal_languages.useful_functions import get_rules_from_console


def remove_useless_symbol(grammar_inner: dict[str, list[str]],
                          set_of_terminals: set[str]) -> dict[str, list[str]]:
    """
    Данная функция удаляет бесполезные символы, проверяя, что элемент грамматики входит во множество терминалов
    """
    return {terminal: _parse_rules(grammar_inner[terminal], set_of_terminals)
            for terminal in grammar_inner if terminal in set_of_terminals}


def _parse_rules(rules: list[str], set_of_terminals: set[str]) -> list[str]:
    """
    Удаляем правила, которые не находятся в множестве терминалов.
    """
    for rule in rules:
        if all(word not in set_of_terminals and word.isupper() for word in rule):
            rules.remove(rule)
    return rules


def main() -> None:
    set_of_terminals = set(input('Множество не терминалов: ').split())
    new_grammar = remove_useless_symbol(get_rules_from_console(), set_of_terminals)
    print("Новая грамматика без бесполезных символов:")
    print("\n".join(f"{key} -> {'|'.join(value)}" for key, value in new_grammar.items()))


if __name__ == "__main__":
    main()
