import pytest
from python_language.formal_languages.seventh_eighth_laboratory.remove_unreachable_states_dfa_class import (
    RemovedUselessSymbolsDFA)
from python_language.formal_languages.seventh_eighth_laboratory.minimize_dfa_class import DFAMinimizer


def test_twelfth_variant():
    """
    Вариант Паши
    """
    states = {"q0", "q1", "q2", "q3", "q4", "q5", "q6"}
    alphabet = {"a", "b"}
    start = "q0"
    final_states = {"q3", "q6"}
    transitions = {
        "q0": {"a": {"q1"}, "b": {"q4"}},
        "q1": {"a": {"q2"}, "b": {"q1"}},
        "q2": {"a": {"q3"}, "b": {"q6"}},
        "q3": {"a": {"q3"}, "b": {"q3"}},
        "q4": {"a": {"q5"}, "b": {"q1"}},
        "q5": {"a": {"q6"}, "b": {"q3"}},
        "q6": {"a": {"q6"}, "b": {"q3"}},
    }

    d = RemovedUselessSymbolsDFA(states, alphabet, start, transitions, final_states)
    n = DFAMinimizer.from_removed_symbols_dfa(d)

    assert n.set_of_states == {'q0', 'q1q4', 'q2q5', 'q3q6'}
    assert n.set_of_input_alphabet_characters == {'a', 'b'}
    assert n.transition_function == {
        'q0': {'a': {'q1q4'}, 'b': {'q1q4'}},
        'q1q4': {'a': {'q2q5'}, 'b': {'q1q4'}},
        'q2q5': {'a': {'q3q6'}, 'b': {'q3q6'}},
        'q3q6': {'a': {'q3q6'}, 'b': {'q3q6'}},
    }
    assert n.final_states == {"q3q6"}


def test_fourth_variant():
    """
    Вариант Снежаны
    """

    states = {"q0", "q1", "q2", "q3", "q4", "q5", "q6"}
    alphabet = {"0", "1"}
    start = "q0"
    final_states = {"q3", "q5", "q6"}
    transitions = {
        "q0": {"0": {"q1"}, "1": {"q1"}},
        "q1": {"0": {"q4"}, "1": {"q2"}},
        "q2": {"0": {"q5"}, "1": {"q3"}},
        "q3": {"0": {"q3"}, "1": {"q5"}},
        "q4": {"0": {"q4"}, "1": {"q2"}},
        "q5": {"0": {"q3"}, "1": {"q5"}},
        "q6": {"0": {"q3"}, "1": {"q5"}},
    }

    d = RemovedUselessSymbolsDFA(states, alphabet, start, transitions, final_states)
    n = DFAMinimizer.from_removed_symbols_dfa(d)

    assert n.set_of_states == {'q0', 'q2', 'q3q5', 'q1q4'}
    assert n.set_of_input_alphabet_characters == {"0", "1"}
    assert n.transition_function == {
        'q0': {'1': {'q1q4'}, '0': {'q1q4'}},
        'q2': {'1': {'q3q5'}, '0': {'q3q5'}},
        'q3q5': {'1': {'q3q5'}, '0': {'q3q5'}},
        'q1q4': {'1': {'q2'}, '0': {'q1q4'}}
    }
    assert n.start_state == "q0"
    assert n.final_states == {'q3q5'}


def test_fourteenth_variant():
    """
    14 вариант
    """

    states = {"q0", "q1", "q2", "q3", "q4", "q5", "q6"}
    alphabet = {"a", "b"}
    start = "q0"
    final_states = {"q3", "q5", "q6"}
    transitions = {
        "q0": {"a": {"q1"}, "b": {"q4"}},
        "q1": {"a": {"q4"}, "b": {"q2"}},
        "q2": {"a": {"q5"}, "b": {"q3"}},
        "q3": {"a": {"q3"}, "b": {"q5"}},
        "q4": {"a": {"q4"}, "b": {"q2"}},
        "q5": {"a": {"q3"}, "b": {"q5"}},
        "q6": {"a": {"q3"}, "b": {"q5"}},
    }

    d = RemovedUselessSymbolsDFA(states, alphabet, start, transitions, final_states)
    n = DFAMinimizer.from_removed_symbols_dfa(d)

    assert n.set_of_states == {'q1q4', 'q0', 'q3q5', 'q2'}
    assert n.set_of_input_alphabet_characters == {"a", "b"}
    assert n.transition_function == {
        'q1q4': {'a': {'q1q4'}, 'b': {'q2'}},
        'q0': {'a': {'q1q4'}, 'b': {'q1q4'}},
        'q3q5': {'a': {'q3q5'}, 'b': {'q3q5'}},
        'q2': {'a': {'q3q5'}, 'b': {'q3q5'}}
    }
    assert n.start_state == "q0"
    assert n.final_states == {'q3q5'}


if __name__ == "__main__":
    pytest.main()
