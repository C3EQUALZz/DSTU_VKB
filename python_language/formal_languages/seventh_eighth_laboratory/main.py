"""
Здесь происходит точка запуска между классами, значения взяты из примера в методичке
"""

from python_language.formal_languages.seventh_eighth_laboratory.remove_unreachable_states_dfa_class import (
    RemovedUselessSymbolsDFA)
from python_language.formal_languages.seventh_eighth_laboratory.minimize_dfa_class import DFAMinimizer


def main() -> None:
    states = {"A", "B", "C", "D", "E", "F", "G"}
    alphabet = {"a", "b"}
    start = "A"
    final_states = {"D", "E"}
    transitions = {
        "A": {"a": {"B"}, "b": {"C"}},
        "B": {"b": {"D"}},
        "C": {"b": {"E"}},
        "D": {"a": {"C"}, "b": {"E"}},
        "E": {"a": {"B"}, "b": {"D"}},
        "F": {"a": {"D"}, "b": {"G"}},
        "G": {"a": {"F"}, "b": {"E"}}
    }

    # M`` = ({'B', 'D', 'C', 'A', 'E'}, {'b', 'a'},
    # {'A': {'a': {'B'}, 'b': {'C'}},
    # 'B': {'b': {'D'}},
    # 'C': {'b': {'E'}},
    # 'D': {'a': {'C'}, 'b': {'E'}},
    # 'E': {'a': {'B'}, 'b': {'D'}}},
    # A, {'D', 'E'})
    d = RemovedUselessSymbolsDFA(states, alphabet, start, transitions, final_states)
    n = DFAMinimizer.from_removed_symbols_dfa(d)
    print(n)


if __name__ == "__main__":
    main()
