"""
Удаление цепных правил из грамматики

Оригинальный код, который я переделывал взят отсюда:
Я сам ничего особо не понимаю, только улучшаю состояние кода, так как автор печально написал

https://github.com/LysenkoAlexey/delete_chain_rules/blob/main/Delete_chain_rules_version3/Delete_chain_rules_version3/Delete_chain_rules_version3.py

----

S -> AB
A -> B
A -> ab
B -> a
B -> C
C -> b
exit

---
Q -> 01A
Q -> 01B
Q -> A
A -> OB1
A -> B
A -> 1
A -> E
B -> BA0
B -> B1
B -> C
B -> E
exit
"""
from typing import Any, Generator

from formal_languages.third_laboratory import remove_unreachable_symbols
from formal_languages.useful_functions import get_rules_from_console


def delete_chains(rules: dict[str, list[str]]) -> dict[str, list[str]]:
    """
    https://neerc.ifmo.ru/wiki/index.php?title=%D0%A3%D0%B4%D0%B0%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5_%D1%86%D0%B5%D0%BF%D0%BD%D1%8B%D1%85_%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB_%D0%B8%D0%B7_%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B8

    Удаляет цепные правила из грамматики.

    Args:
        rules (dict): Словарь грамматических правил.

    Returns:
        dict: Грамматика без цепных правил.
    """

    # Получаем список нетерминальных символов
    not_terminals = set(rules.keys())

    # Создаем пары символов
    pairs = [(char_not_terminal, char_not_terminal) for char_not_terminal in not_terminals]

    # Расширяем пары символов для учета новых возможных пар
    for char in not_terminals:
        pairs.extend(_expand_pairs(pairs, rules, not_terminals, char))

    return _configure_new_rules(rules, pairs)


def _expand_pairs(
        pairs: list[tuple[str, str]],
        rules: dict[str, list[str]],
        not_terminals: set[str],
        char: str) -> Generator[tuple[str, str], Any, None]:
    """
    Расширяет список пар символов для учета новых возможных пар.

    Args:
        pairs (list): Список пар символов.
        rules (dict): Словарь грамматических правил.
        not_terminals (set): Множество нетерминальных символов.
        char (str): Текущий символ.
    """
    for left, right in pairs:
        if right == char:
            yield from ((left, elem) for elem in rules[char] if elem in not_terminals and elem != char)


def _configure_new_rules(rules: dict[str, list[str]], pairs: list[tuple[str, str]]) -> dict[str, list[str]]:
    """
    Здесь происходит конфигурация данных правил в результате алгоритма
    """
    new_rules = {char: [elem for elem in rules.get(char) if elem not in rules.keys()] for char in rules}

    for left, right in pairs:
        if left != right:
            new_rules[left].extend(new_rules[right])

    return new_rules


def main() -> None:
    grammar = get_rules_from_console("don't_remove")
    new_grammar = remove_unreachable_symbols(delete_chains(grammar))
    print("Новая грамматика без цепных правил:")
    print("\n".join(f"{key} -> {'|'.join(value)}".rstrip("|") for key, value in new_grammar.items()))


if __name__ == '__main__':
    main()
