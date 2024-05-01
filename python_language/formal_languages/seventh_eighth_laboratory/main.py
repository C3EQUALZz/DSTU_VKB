"""
Здесь происходит точка запуска между классами, значения взяты из примера в методичке
"""

from python_language.formal_languages.seventh_eighth_laboratory.remove_unreachable_states_dfa_class import (
    RemovedUselessSymbolsDFA)
from python_language.formal_languages.seventh_eighth_laboratory.minimize_dfa_class import DFAMinimizer


def main() -> None:

    states = {"q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7"}
    alphabet = {"a", "b"}
    start = "q0"
    final_states = {"q2", "q3", "q5", "q6", "q7"}
    transitions = {
        "q0": {"a": {"q1"}, "b": {"q4"}},
        "q1": {"a": {"q2"}, "b": {"q4"}},
        "q2": {"a": {"q3"}, "b": {"q5"}},
        "q3": {"a": {"q6"}, "b": {"q3"}},
        "q4": {"a": {"q5"}, "b": {"q1"}},
        "q5": {"a": {"q3"}, "b": {"q4"}},
        "q6": {"a": {"q3"}, "b": {"q6"}},
        "q7": {"a": {"q3"}, "b": {"q6"}},
    }
    d = RemovedUselessSymbolsDFA(states, alphabet, start, transitions, final_states)
    n = DFAMinimizer.from_removed_symbols_dfa(d)
    n.show_diagram()


if __name__ == "__main__":
    main()
