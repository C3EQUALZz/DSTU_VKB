"""
Левая факторизация правил

Полезные ресурсы: https://stackoverflow.com/questions/21217410/left-factoring-using-python

---
A -> abc
A -> abd
A -> aef
B -> bcd
B -> bde
B -> bef
exit
"""
from python_language.formal_languages.useful_functions import get_rules_from_console
from collections import defaultdict


def left_factorize(grammar: dict[str, list[str]]) -> dict[str, list[str]]:
    """
    Эта функция выполняет левую факторизацию по данной грамматике
    Args:
        grammar: словарь, представляющий грамматику, где ключи - это нетерминальные символы,
         а значения - списки производственных правил.
    Returns:
        Left-factorized грамматику
    """
    new_grammar = defaultdict(list)

    for non_terminal, productions in grammar.items():
        # Найти общий префикс среди производств текущего не терминала
        if common_prefix := _find_common_prefix(productions):

            # Если существует общий префикс, создаем для него новый нетерминальный символ
            new_non_terminal = non_terminal + "`"

            # Обновляем грамматику, чтобы отразить лево-факторные правила
            new_grammar[non_terminal].append(common_prefix + new_non_terminal)
            new_grammar[new_non_terminal].extend([production[len(common_prefix):] for production in productions])

        else:
            new_grammar[non_terminal].append(productions)

    return new_grammar


def _find_common_prefix(productions: list[str]) -> str:
    """
    Находит общий префикс в списке производственных правил.

    Args:
        productions: Лист с продукциями.

    Returns:
        Общий префикс среди производственных правил.
    """
    if not productions:
        return ""

    common_prefix = []
    for chars in zip(*productions):
        # Проверяем, то что совпадают ли все символы в одной позиции
        if len(set(chars)) == 1:
            # Если все символы одинаковы, добавляем их к общему префиксу
            common_prefix.append(chars[0])
        else:
            break

    return ''.join(common_prefix)


def main() -> None:
    grammar = get_rules_from_console("don't_remove")
    new_grammar = left_factorize(grammar)
    print("Новая грамматика c факторизацией правил:")
    print("\n".join(f"{key} -> {'|'.join(value)}".rstrip("|") for key, value in new_grammar.items()))


if __name__ == "__main__":
    main()
