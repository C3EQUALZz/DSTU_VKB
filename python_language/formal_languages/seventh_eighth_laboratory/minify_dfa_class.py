"""
Минимизация ДКА
"""
import os
from copy import deepcopy
from typing import Final
from python_language.formal_languages.seventh_eighth_laboratory.graph_class import Graph

from automata.fa.dfa import DFA

PATH_TO_DIAGRAM: Final = os.path.join(os.path.curdir, "test_dfa_min.png")


class MinifiedDFA:
    # def __init__(self, dfa: DeterministicFiniteAutomaton) -> None:
    #     self.start_state: str = dfa.start_state
    #     self.set_of_input_alphabet_characters: set[str] = copy(dfa.set_of_input_alphabet_characters)
    #     self.set_of_states = copy(dfa.set_of_states)
    #     self.transition_function = deepcopy(dfa.transition_function)
    #     self.final_states = copy(dfa.final_states)

    def __init__(self, states, alphabet, start, transitions, final_states):
        self.__start_state = start
        self.__set_of_input_alphabet_characters = alphabet
        self.__transition_function = transitions
        self.__set_of_states = states
        self.__final_states = final_states
        self.__eliminate_unreachable_states()

    def __eliminate_unreachable_states(self) -> None:
        """
        Удаление недостижимых вершин
        """
        self.__set_of_states = Graph(transitions=self.__transition_function).bfs()
        self._correct_transition_function(transition_function=self.__transition_function)
        self._correct_final_states(final_state=self.__final_states)

    def _correct_transition_function(self, transition_function) -> None:
        """
        Удаление правил перехода, где используются недостижимые вершины
        """
        self.__transition_function = {key: value for key, value in deepcopy(transition_function).items() if
                                      key in self.__set_of_states}

    def _correct_final_states(self, final_state) -> None:
        """
        Удаление финальных состояний, если там были недостижимые вершины
        """
        self.__final_states = {state for state in final_state if state in self.__set_of_states}

    def __str__(self) -> str:
        """
        Магический метод, который нужен для перевода в строку. В моем случае использование для print
        """
        return (f"M`` = ({self.__set_of_states},"
                f" {self.__set_of_input_alphabet_characters},"
                f" {self.__transition_function},"
                f" {self.__start_state},"
                f" {self.__final_states})")

    def show_diagram(self) -> None:
        """
        Метод, который создает граф на основе автомата
        """
        DFA(
            states=self.__set_of_states,
            input_symbols=self.__set_of_input_alphabet_characters,
            transitions=self.__transition_function,
            initial_state=self.__start_state,
            final_states=self.__final_states,
        ).show_diagram(path=PATH_TO_DIAGRAM)


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

    d = MinifiedDFA(states, alphabet, start, transitions, final_states)
    print(d)


if __name__ == "__main__":
    main()
