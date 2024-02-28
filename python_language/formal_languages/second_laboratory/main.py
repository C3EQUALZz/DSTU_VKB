"""
Лабораторная работа №2 по формальным языкам
"""

from grammar_checker import recognize, GrammarType
from python_language.formal_languages.interaction_with_user import read_grammar_from_console


def check_existing_of_grammar(grammar: GrammarType) -> bool:
    ...


def main():
    grammar = read_grammar_from_console()

    if recognize(grammar) == GrammarType.CONTEXT_SENSITIVE:
        check_existing_of_grammar(grammar)


if __name__ == "__main__":
    main()
