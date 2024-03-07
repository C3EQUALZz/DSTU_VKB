"""
Реализовать удаление цепных правил
"""
from python_language.formal_languages.useful_functions import get_rules_from_console


def remove_chain_rules(grammar: dict[str, list[str]]) -> dict[str, set[str]]:
    new_grammar = {}
    for non_terminal, productions in grammar.items():
        new_productions = set()
        chain_productions = set()
        for production in productions:
            if len(production) == 1 and production.isupper():
                chain_productions.add(production)
            else:
                new_productions.add(production)
        while chain_productions:
            chain_non_terminal = chain_productions.pop()
            if chain_non_terminal not in grammar:
                continue
            for chain_production in grammar[chain_non_terminal]:
                if len(chain_production) == 1 and chain_production.isupper():
                    chain_productions.add(chain_production)
                else:
                    new_productions.add(chain_production)
        new_grammar[non_terminal] = new_productions
    return new_grammar


def main():
    new_grammar = remove_chain_rules(get_rules_from_console("don't_remove"))
    print("Новая грамматика без цепных правил:")
    print("\n".join(f"{key} -> {'|'.join(value)}" for key, value in new_grammar.items()))


if __name__ == "__main__":
    main()
