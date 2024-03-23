"""
Удаление ненужных вершин в ДКА
"""
import os
from copy import deepcopy
from typing import Final, MutableSet, MutableMapping, Self, AnyStr, Set

from automata.fa.nfa import NFA

from python_language.formal_languages.seventh_eighth_laboratory.graph_class import Graph
from python_language.formal_languages.fifth_sixth_laboratory.det_final_automat_class import DeterministicFiniteAutomaton

PATH_TO_DIAGRAM: Final = os.path.join(os.path.curdir, "test_dfa_min.png")


class RemovedUselessSymbolsDFA:
    def __init__(self,
                 states: MutableSet[AnyStr],
                 alphabet: MutableSet[AnyStr],
                 start: AnyStr,
                 transitions: MutableMapping[AnyStr, MutableMapping[AnyStr, Set[AnyStr]]],
                 final_states: MutableSet[AnyStr]):

        self.start_state = start
        self.set_of_input_alphabet_characters = alphabet
        self.transition_function = transitions
        self.set_of_states = states
        self.final_states = final_states
        self.__eliminate_unreachable_states()

    @classmethod
    def from_dfa(cls, dfa: DeterministicFiniteAutomaton) -> Self:
        return cls(
            states=dfa.set_of_states,
            alphabet=dfa.set_of_input_alphabet_characters,
            start=dfa.start_state,
            transitions=dfa.transition_function(),
            final_states=dfa.final_states()
        )

    def __eliminate_unreachable_states(self) -> None:
        """
        Удаление недостижимых вершин
        """
        self.set_of_states = Graph(transitions=self.transition_function).bfs()
        self._correct_transition_function(transition_function=self.transition_function)
        self._correct_final_states(final_state=self.final_states)

    def _correct_transition_function(self, transition_function) -> None:
        """
        Удаление правил перехода, где используются недостижимые вершины
        """
        self.transition_function = {key: value for key, value in deepcopy(transition_function).items() if
                                    key in self.set_of_states}

    def _correct_final_states(self, final_state) -> None:
        """
        Удаление финальных состояний, если там были недостижимые вершины
        """
        self.final_states = {state for state in final_state if state in self.set_of_states}

    def __str__(self) -> str:
        """
        Магический метод, который нужен для перевода в строку. В моем случае использование для print
        """
        return (f"M`` = ({self.set_of_states},"
                f" {self.set_of_input_alphabet_characters},"
                f" {self.transition_function},"
                f" {self.start_state},"
                f" {self.final_states})")

    def show_diagram(self) -> None:
        """
        Метод, который создает граф на основе автомата
        """
        NFA(
            states=self.set_of_states,
            input_symbols=self.set_of_input_alphabet_characters,
            transitions=self.transition_function,
            initial_state=self.start_state,
            final_states=self.final_states,
        ).show_diagram(path=PATH_TO_DIAGRAM)
