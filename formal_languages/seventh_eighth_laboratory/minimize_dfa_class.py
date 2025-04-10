"""
Минимизация самого ДКА, алгоритм 2
Полезные ресурсы:
- https://youtu.be/v4YIiRfnnDY?si=Iq5-yuFR7Nrke5QX
- https://youtu.be/0XaGAkY09Wc?si=Ltcw-JBfBYO82KMQ
"""

import os
import re
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from itertools import chain, product
from typing import AnyStr, Final, Mapping, Self, Set

from automata.fa.nfa import NFA
from remove_unreachable_states_dfa_class import RemovedUselessSymbolsDFA

PATH_TO_DIAGRAM: Final = os.path.join(os.path.curdir, "test_dfa_min.png")


@dataclass
class DFAMinimizer:
    set_of_states: Set[AnyStr]
    set_of_input_alphabet_characters: Set[AnyStr]
    start_state: AnyStr
    transition_function: Mapping[AnyStr, Mapping[AnyStr, Set[AnyStr]]]
    final_states: Set[AnyStr]

    def __post_init__(self):
        self.__minimize_dfa()

    @classmethod
    def from_removed_symbols_dfa(cls, dfa: RemovedUselessSymbolsDFA) -> Self:
        return cls(
            set_of_states=dfa.set_of_states,
            set_of_input_alphabet_characters=dfa.set_of_input_alphabet_characters,
            start_state=dfa.start_state,
            transition_function=dfa.transition_function,
            final_states=dfa.final_states,
        )

    def __minimize_dfa(self) -> None:
        """
        Здесь происходит логика минимизации ДКА
        """
        self.set_of_states = {"".join(sorted(s)) for s in self.__minimize_states()}
        self.final_states = {
            state
            for state in self.set_of_states
            if any(set(fin_state).issubset(state) for fin_state in self.final_states)
        }

        self.start_state = "".join(
            [state for state in self.set_of_states if self.start_state in state]
        )
        self.transition_function = self.__construct_transition_function()

    def __minimize_states(self) -> list[Set[AnyStr]]:
        """
        Здесь происходит запуск логики для минимизации вершин графа
        """
        eq_class = [
            sorted(self.final_states),
            sorted(self.set_of_states - self.final_states),
        ]

        while True:
            new_eq_class = self.__new_class_eq(deepcopy(eq_class))

            if eq_class == new_eq_class:
                break

            eq_class = new_eq_class

        return new_eq_class

    def __new_class_eq(self, eq_class: list[Set[AnyStr]]) -> list[Set[AnyStr]]:
        """
        Здесь формируется каждый раз новый класс эквивалентности (0, 1, 2 и т.п).
        Подробнее смотрите данное видео:
        - https://youtu.be/0XaGAkY09Wc?si=GpCJOqZkFvVLfGb5&t=920

        Args:
            eq_class (list[set[str]]) - прошлый класс эквивалентности
        Returns:
            list[set[AnyStr]] - новый класс эквивалентности
        """
        new_eq_class = []
        for group in eq_class:
            if len(group) == 1:
                new_eq_class.append(group)
            else:
                new_eq_class.extend(
                    filter(None, self.__create_new_group_based_on_the_old(group))
                )

        return new_eq_class

    def __create_new_group_based_on_the_old(
        self, group: set[AnyStr]
    ) -> tuple[set[AnyStr], set[AnyStr]]:
        """
        Здесь вот каждый раз создаются новые группы - наборы вершин
        Args:
            group - группа, которую мы хотим видоизменить
        Returns:
            Кортеж из новой и старой видоизмененной группы
            Пример: ({A, B, C} -> __create_new_group_based_on_the_old -> {A, B}, {C})
        """
        # TODO: ЗДЕСЬ ОШИБКА В ЛОГИКЕ, НУЖНО ИСПРАВИТЬ

        new_group = set()
        remaining_states = group.copy()

        for state in group:
            # Проверяем все ли переходы из этого состояния остаются в группе
            if all(
                self.transition_function.get(state, {})
                .get(symbol, set())
                .issubset(group)
                for symbol in self.set_of_input_alphabet_characters
            ):
                new_group.add(state)
                remaining_states.remove(state)

        return remaining_states, new_group

    def __construct_transition_function(
        self,
    ) -> Mapping[AnyStr, Mapping[AnyStr, Set[AnyStr]]]:
        """
        Перестроение таблицы переходов на основе наших вершин.
        На основе старой берутся вершины и объединяются в общую функцию перехода.
        """
        new_transition_function = defaultdict(dict)

        for state, symbol in product(
            self.set_of_states, self.set_of_input_alphabet_characters
        ):
            transitions = set(
                chain.from_iterable(
                    self.transition_function.get(old_state, {}).get(symbol, [])
                    for old_state in re.findall(r"[A-Za-z][0-9]*", state)
                )
            )

            new_transition_function[state][symbol] = {
                new_state_set
                for new_state_set in self.set_of_states
                if any(
                    set(new_state).issubset(new_state_set) for new_state in transitions
                )
            }

        return new_transition_function

    def __str__(self) -> str:
        """
        Магический метод, который нужен для перевода в строку. В моем случае использование для print
        """
        return (
            f"M`` = ({self.set_of_states},"
            f" {self.set_of_input_alphabet_characters},"
            f" {self.transition_function},"
            f" {self.start_state},"
            f" {self.final_states})"
        )

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
