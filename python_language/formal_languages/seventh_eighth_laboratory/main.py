"""
Здесь происходит точка запуска между классами, значения взяты из примера в методичке
"""

from python_language.formal_languages.seventh_eighth_laboratory.remove_unreachable_states_dfa_class import (
    RemovedUselessSymbolsDFA)
from python_language.formal_languages.seventh_eighth_laboratory.minimize_dfa_class import DFAMinimizer


def main() -> None:
    # states = {"A", "B", "C", "D", "E", "F", "G"}
    # alphabet = {"a", "b"}
    # start = "A"
    # final_states = {"D", "E"}
    # transitions = {
    #     "A": {"a": {"B"}, "b": {"C"}},
    #     "B": {"b": {"D"}},
    #     "C": {"b": {"E"}},
    #     "D": {"a": {"C"}, "b": {"E"}},
    #     "E": {"a": {"B"}, "b": {"D"}},
    #     "F": {"a": {"D"}, "b": {"G"}},
    #     "G": {"a": {"F"}, "b": {"E"}}
    # }

    # M`` = ({'B', 'D', 'C', 'A', 'E'}, {'b', 'a'},
    # {'A': {'a': {'B'}, 'b': {'C'}},
    # 'B': {'b': {'D'}},
    # 'C': {'b': {'E'}},
    # 'D': {'a': {'C'}, 'b': {'E'}},
    # 'E': {'a': {'B'}, 'b': {'D'}}},
    # A, {'D', 'E'})

    # A, B, C, D, E

    # states = {"q0", "q1", "q2", "q3", "q4", "q5"}
    # alphabet = {"1", "0"}
    # start = "q0"
    # transitions = {
    #     "q0": {"0": {"q0"}, "1": {"q1"}},
    #     "q1": {"0": {"q2"}, "1": {"q1"}},
    #     "q2": {"0": {"q0"}, "1": {"q3"}},
    #     "q3": {"0": {"q4"}, "1": {"q3"}},
    #     "q4": {"0": {"q5"}, "1": {"q3"}},
    #     "q5": {"0": {"q5"}, "1": {"q3"}}
    # }
    # final_states = {"q3", "q4", "q5"}

    # states = {"A", "B", "C", "D", "E"}
    # alphabet = {"0", "1"}
    # start = "A"
    # final_states = {"E"}
    # transitions = {
    #     "A": {"0": {"B"}, "1": {"C"}},
    #     "B": {"0": {"B"}, "1": {"D"}},
    #     "C": {"0": {"B"}, "1": {"C"}},
    #     "D": {"0": {"B"}, "1": {"E"}},
    #     "E": {"0": {"B"}, "1": {"C"}}
    # }

    states = {"Y", "X", "Z", "I", "J", "K", "L", "N", "M"}
    alphabet = {"i", "j", "n", "m", "k", "/", "!"}
    start = "X"
    final_states = {"N"}
    transitions = {
        "Y": {"n": {"X"}, "m": {"I"}},
        "X": {"i": {"I"}, "j": {"K"}},
        "Z": {"n": {"X"}, "m": {"K"}},
        "I": {"j": {"J"}, "n": {"L"}},
        "J": {"m": {"X"}, "k": {"N"}},
        "K": {"j": {"J"}, "n": {"M"}},
        "L": {"/": {"L"}, "!": {"N"}},
        "N": {},
        "M": {"!": {"N"}, "/": {"M"}}
    }

    d = RemovedUselessSymbolsDFA(states, alphabet, start, transitions, final_states)
    d.show_diagram()
    n = DFAMinimizer.from_removed_symbols_dfa(d)
    n.show_diagram()


if __name__ == "__main__":
    main()
