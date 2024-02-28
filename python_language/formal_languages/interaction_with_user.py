"""
Вынес в общую функцию, чтобы делать ввод данных от пользователя
"""
from collections import defaultdict


def read_grammar_from_console():
    dictionary = defaultdict(list)
    print("Сейчас вы будете вводить грамматики. Пример ввода: S -> aSb\nКонец ввода - это 'exit' ")

    while (args := input()) != "exit":
        key, value = map(lambda x: x.strip().rstrip("|E"), args.split("->"))
        dictionary[key].append(value)
