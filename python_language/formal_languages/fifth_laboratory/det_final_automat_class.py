"""
Шаг 1. Пометить первый столбец таблицы переходов M′ ДКА начальным состоянием (множеством начальных состояний) НКА M.

Шаг 2. Заполняем очередной столбец таблицы переходов M′, помеченный символами D, для этого определяем те состояния M,
которые могут быть достигнуты из каждого символа строки D при каждом входном символе x.
Поместить каждое найденное множество R (в том числе ∅) в соответствующие позиции столбца D таблицы M′, т.е.:
F′(D, x) ={s | s∈F(t, x) для некоторого t∈D}.

Шаг 3. Для каждого нового множества R (кроме ∅), полученного в
столбце D таблицы переходов M ′, добавить новый столбец в таблицу,
помеченный R.

Шаг 4. Если в таблице переходов КА M′ есть столбец с незаполненными
позициями, то перейти к шагу 2.

Шаг 5. Во множество Z′ ДКА M′ включить каждое множество,
помечающее столбец таблицы переходов M′ и содержащее q ∈ Z НКА M.

Шаг 6. Составить таблицу новых обозначений множеств состояний и
определить ДКА M′ в этих обозначениях.
"""
import os
from collections import defaultdict
from typing import Any, Final

from automata.fa.dfa import DFA
from automata.fa.nfa import NFA

from python_language.formal_languages.fifth_laboratory.grammar_class import Grammar
from python_language.formal_languages.fifth_laboratory.non_det_final_automat_class import (
    NonDeterministicFiniteAutomaton)

PATH_TO_DIAGRAM: Final = os.path.join(os.path.curdir, "test_dfa.png")


class DeterministicFiniteAutomaton:
    def __init__(self, non_deterministic_automaton: NonDeterministicFiniteAutomaton) -> None:
        """
        M' = (Q', T, F', H, Z')
        - Q' - множество состояний (set_of_states)
        - T - множество символов входного алфавита (set_of_states)
        - F' - функции перехода (transition_function)
        - H - начальный символ автомата (start_state)
        - Z` - множество заключительных состояний (final_states)
        """
        self.start_state: str = non_deterministic_automaton.start_state
        self.set_of_input_alphabet_characters: set[str] = non_deterministic_automaton.set_of_input_alphabet_characters
        self.set_of_states = non_deterministic_automaton.set_of_states
        self.transition_function = non_deterministic_automaton.transition_function
        self.final_states = non_deterministic_automaton.final_states

    @property
    def set_of_states(self) -> set[str]:
        """
        Свойство геттер, которое возвращает множество состояний
        """
        return self.__set_of_states

    @set_of_states.setter
    def set_of_states(self, set_of_states_from_nfa: set[str]) -> None:
        self.__set_of_states = set_of_states_from_nfa

    @property
    def transition_function(self) -> dict[str, defaultdict[Any, set]]:
        """
        Свойство - геттер, которую возвращает функцию переходов
        """
        return self.__transition_function

    @transition_function.setter
    def transition_function(self, transition_function_from_nfa: dict[str, defaultdict[Any, set]]) -> None:
        self.__transition_function = transition_function_from_nfa

    @property
    def final_states(self) -> set[str]:
        """
        Свойство - геттер, которое возвращает множество заключительных состояний
        """
        return self.__final_states

    @final_states.setter
    def final_states(self, final_states_from_nfa: set[str]) -> None:
        self.__final_states = final_states_from_nfa

    def __str__(self) -> str:
        """
        Магический метод, который нужен для перевода в строку. В моем случае использование для print
        """
        return (f"M` = ({self.set_of_states},"
                f" {self.set_of_input_alphabet_characters},"
                f" {self.transition_function},"
                f" {self.start_state},"
                f" {self.final_states})")

    def show_diagram(self) -> None:
        """
        Метод, который создает граф на основе автомата
        """
        DFA(
            states=self.set_of_states,
            input_symbols=self.set_of_input_alphabet_characters,
            transitions=self.transition_function,
            initial_state=self.start_state,
            final_states=self.final_states,
        ).show_diagram(path=PATH_TO_DIAGRAM)

    def epsilon_closure(self, state: str):
        # Инициализируем эпсилон-замыкание текущим состоянием
        epsilon_closure_set = {state}

        # Создаем очередь для обработки состояний
        queue = [state]

        # Пока очередь не пуста
        while queue:
            current_state = queue.pop(0)

            # Находим все состояния, в которые можно перейти по эпсилон-переходу из текущего состояния
            epsilon_transitions = self.transition_function.get(current_state, {}).get('', set())

            # Добавляем новые состояния в эпсилон-замыкание
            epsilon_closure_set.update(epsilon_transitions)

            # Добавляем новые состояния в очередь для обработки
            queue.extend(epsilon_transitions - epsilon_closure_set)

        return epsilon_closure_set


if __name__ == "__main__":
    grammar = Grammar({"a", "b"}, {"S", "A", "B"}, {"S": ["aB", "aA"], "B": ["bB", "a"], "A": ["aA", "b"]}, "S")
    nfa = NonDeterministicFiniteAutomaton(grammar)
    print(nfa)
    dfa = DeterministicFiniteAutomaton(nfa)
    print(dfa.epsilon_closure("A"))
