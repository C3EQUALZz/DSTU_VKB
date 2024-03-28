"""
Удаление ненужных вершин в ДКА
"""
import os
from copy import deepcopy
from dataclasses import dataclass
from typing import MutableMapping, Self, AnyStr, Set, Final

from automata.fa.nfa import NFA

from ..fifth_sixth_laboratory.det_final_automat_class import DeterministicFiniteAutomaton
from .graph_class import Graph

PATH_TO_DIAGRAM: Final = os.path.join(os.path.curdir, "test_dfa_removed.png")


@dataclass
class RemovedUselessSymbolsDFA:
    set_of_states: Set[AnyStr]
    set_of_input_alphabet_characters: Set[AnyStr]
    start_state: AnyStr
    transition_function: MutableMapping[AnyStr, MutableMapping[AnyStr, Set[AnyStr]]]
    final_states: Set[AnyStr]

    def __post_init__(self) -> None:
        self.__eliminate_unreachable_states()

    @classmethod
    def from_dfa(cls, dfa: DeterministicFiniteAutomaton) -> Self:
        return cls(
            set_of_states=dfa.set_of_states,
            set_of_input_alphabet_characters=dfa.set_of_input_alphabet_characters,
            start_state=dfa.start_state,
            transition_function=dfa.transition_function,
            final_states=dfa.final_states
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
