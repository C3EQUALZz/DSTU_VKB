"""
Здесь происходит точка запуска между классами, значения взяты из примера в методичке
"""

import os

from automata.fa.dfa import DFA
from automata.fa.nfa import NFA

from formal_languages.seventh_eighth_laboratory.minimize_dfa_class import \
    DFAMinimizer
from formal_languages.seventh_eighth_laboratory.remove_unreachable_states_dfa_class import \
    RemovedUselessSymbolsDFA


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

    states = {"S", "A", "B", "C", "N"}
    alphabet = {"a", "b", "c", "/"}
    start = "S"
    final_states = {"N"}
    transitions = {
        "S": {"a": {"A"}, "b": {"B"}},
        "A": {"a": {"A"}, "c": {"C"}},
        "B": {"b": {"B"}, "c": {"C"}},
        "C": {"c": {"C"}, "/": {"N"}},
    }

    # states = {"q0", "q1", "q2", "q3", "q4", "q5", "q6"}
    # alphabet = {"a", "b"}
    # start = "q0"
    # transitions = {
    #     "q0": {"a": {"q1"}, "b": {"q4"}},
    #     "q1": {"a": {"q2"}, "b": {"q1"}},
    #     "q2": {"a": {"q3"}, "b": {"q6"}},
    #     "q3": {"a": {"q3"}, "b": {"q3"}},
    #     "q4": {"a": {"q5"}, "b": {"q1"}},
    #     "q5": {"a": {"q6"}, "b": {"q3"}},
    #     "q6": {"a": {"q6"}, "b": {"q3"}}
    # }
    #
    # final_states = {"q3", "q6"}

    # states = {"q0", "q1", "q2", "q3", "q4", "q5"}
    # alphabet = {"0", "1"}
    # start = "q0"
    # final_states = {"q3", "q4", "q5"}
    # transitions = {
    #     "q0": {"0": {"q1"}, "1": {"q2"}},
    #     "q1": {"0": {"q3"}, "1": {"q2"}},
    #     "q2": {"0": {"q4"}, "1": {"q1"}},
    #     "q3": {"0": {"q5"}, "1": {"q4"}},
    #     "q4": {"0": {"q4"}, "1": {"q2"}},
    #     "q5": {"0": {"q5"}, "1": {"q4"}}
    # }

    # d = RemovedUselessSymbolsDFA(states, alphabet, start, transitions, final_states)
    # d.show_diagram()
    # n = DFAMinimizer.from_removed_symbols_dfa(d)
    # print(n)

    DFA.from_nfa(
        NFA(
            states=states,
            input_symbols=alphabet,
            initial_state=start,
            transitions=transitions,
            final_states=final_states,
        ),
        retain_names=True,
        minify=False,
    ).show_diagram(path=os.path.join(os.path.curdir, "test_dfa_min.png"))

    # DFA.from_nfa(NFA(
    #     states=states,
    #     input_symbols=alphabet,
    #     final_states=final_states,
    #     transitions=transitions,
    #     initial_state=start
    # ), retain_names=True).show_diagram(path=os.path.join(os.path.curdir, "test_dfa.png"))

    # DFA(
    #     states=states,
    #     input_symbols=alphabet,
    #     final_states=final_states,
    #     transitions=transitions,
    #     initial_state=start,
    # ).minify(retain_names=True).show_diagram(os.path.join(os.path.curdir, "test_dfa_min.png"))


if __name__ == "__main__":
    main()
