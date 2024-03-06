"""
Во многих лабораторных работах происходит запрос грамматики через консоль, поэтому вынес отдельную функцию, чтобы обрабатывать
"""
from collections import defaultdict


def get_rules_from_console():
    """
    Получение информации о правилах грамматики, возвращая в виде словаря
    """
    dictionary = defaultdict(list)
    print("Сейчас вы будете вводить грамматики. Пример ввода: S -> aSb\nКонец ввода - это 'exit' ")

    while (args := input()) != "exit":
        key, value = map(lambda x: x.strip().rstrip("|E"), args.split("->"))
        dictionary[key].append(value)

    return dictionary
