"""
Удаляет левую рекурсию из грамматики

Полезные источники:
- https://www.geeksforgeeks.org/removing-direct-and-indirect-left-recursion-in-a-grammar/
- https://www.gatevidyalay.com/left-recursion-left-recursion-elimination/?__cf_chl_rt_tk=uccLph7mi4FFPGgpf6Qqv1CojQylaiIfUsftfjKIz68-1710434049-0.0.1.1-1386
- https://boxofnotes.com/what-is-left-recursion-and-how-to-eliminate-left-recursion/
--------
S -> Sa
S -> Sb
S -> c
S -> d
exit
"""

from collections import defaultdict
from typing import Iterator

from python_language.formal_languages.useful_functions import get_rules_from_console


def _split_rules(rules: list[str], non_terminal: str) -> tuple[Iterator[str], Iterator[str]]:
    """
    Разделяет правила на alpha_rules и beta_rules.

    Args:
        rules: Список правил для не терминала
        non_terminal: Не терминал, для которого разделяются правила.

    Returns:
        Кортеж из двух итераторов: первый для правил, начинающихся с не терминала,
        второй для остальных правил.
    """
    alpha_rules = (rule[len(non_terminal):] for rule in rules if rule.startswith(non_terminal))

    beta_rules = (rule for rule in rules if not rule.startswith(non_terminal))

    return alpha_rules, beta_rules


def _generate_new_rules(non_terminal: str,
                        alpha_rules: Iterator[str],
                        beta_rules: Iterator[str]) -> tuple[Iterator[str], Iterator[str], str]:
    """
    Генерирует новые правила для не терминала и его нового варианта.

    Args:
        non_terminal: Исходный не терминал
        alpha_rules: Итератор правил, начинающихся с не терминала
        beta_rules: Итератор остальных правил.

    Returns:
        Кортеж из трех элементов: итератор новых правил для исходного не терминала,
        итератор новых правил для нового не терминала, и сам новый не терминал.
    """
    new_non_terminal = non_terminal + "'"

    new_rules_non_terminal = (rule + new_non_terminal for rule in beta_rules)

    new_rules_new_non_terminal = iter([rule + new_non_terminal for rule in alpha_rules] + ["E"])

    return new_rules_non_terminal, new_rules_new_non_terminal, new_non_terminal


def remove_left_recursion(rules: dict[str, list[str]]) -> dict[str, list[str]]:
    """
    Удаляет левую рекурсию из грамматики.

    Args:
        rules: Словарь с правилами грамматики.

    Returns:
        Словарь с обновленными правилами грамматики без левой рекурсии.
    """
    non_terminals = defaultdict(list, rules)

    for non_terminal in rules:

        if any(rule.startswith(non_terminal) for rule in rules[non_terminal]):
            alpha_rules, beta_rules = _split_rules(non_terminals[non_terminal], non_terminal)

            if not alpha_rules:
                continue

            new_rules_non_terminal, new_rules_new_non_terminal, new_non_terminal = _generate_new_rules(non_terminal,
                                                                                                       alpha_rules,
                                                                                                       beta_rules)

            non_terminals[non_terminal] = list(new_rules_non_terminal)
            non_terminals[new_non_terminal] = list(new_rules_new_non_terminal)

    return non_terminals


def main() -> None:
    grammar = get_rules_from_console("don't_remove")
    new_grammar = remove_left_recursion(grammar)
    print("Новая грамматика без левой рекурсии: ")
    print("\n".join(f"{key} -> {'|'.join(value).rstrip('|')}" for key, value in new_grammar.items() if value))


if __name__ == '__main__':
    main()
