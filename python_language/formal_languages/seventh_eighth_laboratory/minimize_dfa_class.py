"""
Минимизация самого ДКА, алгоритм 2
Полезные ресурсы:
- https://youtu.be/v4YIiRfnnDY?si=Iq5-yuFR7Nrke5QX
"""
import os
from typing import Self, Set, AnyStr, Mapping, Final

from python_language.formal_languages.seventh_eighth_laboratory.remove_unreachable_states_dfa_class import (
    RemovedUselessSymbolsDFA)

from automata.fa.nfa import NFA

PATH_TO_DIAGRAM: Final = os.path.join(os.path.curdir, "test_dfa_min.png")


class DFAMinimizer:
    def __init__(self,
                 states: Set[AnyStr],
                 alphabet: Set[AnyStr],
                 start: AnyStr,
                 transitions: Mapping[AnyStr, Mapping[AnyStr, Set[AnyStr]]],
                 final_states: Set[AnyStr]) -> None:
        self.start_state = start
        self.set_of_input_alphabet_characters: set[str] = alphabet
        self.set_of_states = states
        self.transition_function = transitions
        self.final_states = final_states
        self.__minimize()

    @classmethod
    def from_removed_symbols_dfa(cls, dfa: RemovedUselessSymbolsDFA) -> Self:
        return cls(
            states=dfa.set_of_states,
            alphabet=dfa.set_of_input_alphabet_characters,
            start=dfa.start_state,
            transitions=dfa.transition_function,
            final_states=dfa.final_states
        )

    def __minimize(self) -> None:
        ...

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
