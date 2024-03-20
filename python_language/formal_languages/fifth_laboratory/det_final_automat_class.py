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
from collections import defaultdict, deque
from typing import Any, Final

from automata.fa.dfa import DFA

from python_language.formal_languages.fifth_laboratory.grammar_class import Grammar
from python_language.formal_languages.fifth_laboratory.non_det_final_automat_class import (
    NonDeterministicFiniteAutomaton)

PATH_TO_DIAGRAM: Final = os.path.join(os.path.curdir, "test_dfa.png")


class DeterFA:
    def __init__(self, transitions: dict[str, dict[str, set[str]]], start_state, final_states, input_alphabet, states):
        self.start_state: str = start_state
        self.set_of_input_alphabet_characters: set[str] = input_alphabet
        self.set_of_states = states
        self.transition_function = transitions
        self.final_states = final_states

    def construct_dfa(self) -> None:
        dfa_transitions = defaultdict(dict)
        unmarked_states = [self._epsilon_closure({self.start_state})]
        marked_states = []

        while unmarked_states:
            current_state_set = unmarked_states.pop(0)
            marked_states.append(current_state_set)

            # Проверяем, содержит ли текущее состояние хотя бы одно финальное состояние
            if current_state_set.intersection(self.final_states):
                self.final_states.update(current_state_set)

            for symbol in self.set_of_input_alphabet_characters:
                next_state_set = self._epsilon_closure(self._transition(current_state_set, symbol))

                if next_state_set not in marked_states:
                    unmarked_states.append(next_state_set)

                dfa_transitions[self._states_to_string(current_state_set)].update(
                    {symbol: self._states_to_string(next_state_set)})

        self.transition_function = dfa_transitions
        self.set_of_states = {self._states_to_string(state) for state in marked_states}
        # Убираем из множества финальных состояний все, которые не являются финальными в ДКА
        self.final_states = {state for state in self.final_states if state in self.set_of_states}

    def _transition(self, state_set: set[str], symbol: str) -> set[str]:
        """
        Данный метод используется для получения множества состояний,
        в которые можно перейти из заданного множества состояний по заданному символу.

        В частности, он принимает на вход текущее множество состояний state_set и символ symbol, и возвращает множество
        состояний, в которые можно перейти из состояний state_set по символу symbol.
        """
        next_state_set = set()

        for state in state_set:
            if state in self.transition_function and symbol in self.transition_function[state]:
                next_state_set.update(self.transition_function[state][symbol])

        return next_state_set

    def _epsilon_closure(self, state_set: set[str]) -> set[str]:
        """
        Вычисление эпсилон перехода для элемента (вершины, к которым мы можем перейти по эпислон)
        """
        closure = set(state_set)
        stack = deque(state_set)

        while stack:
            state = stack.pop()
            epsilon_states = self.transition_function.get(state, {}).get('', set())

            closure.update(epsilon_states)
            stack.extend(epsilon_states - closure)

        return closure

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

    @staticmethod
    def _states_to_string(state_set: set[str]) -> str:
        """
        Вспомогательный метод для перевода множества состояний в строку для библиотеки
        """
        return ''.join(sorted(state_set))


def main() -> None:
    transitions = {
        "q0": {"a": {"q0"}, "b": {"q0", "q1"}},
        "q1": {"a": {}, "b": {"q2"}},
        "q2": {"a": {}, "b": {}},
    }

    start_state = "q0"
    final_states = {"q2"}
    input_alphabet = {"a", "b"}
    states = {"q0", "q1", "q2"}

    d = DeterFA(transitions, start_state, final_states, input_alphabet, states)
    d.construct_dfa()
    d.show_diagram()

    print(d)


if __name__ == "__main__":
    grammar = Grammar({"a", "b"}, {"S", "A", "B"}, {"S": ["aB", "aA"], "B": ["bB", "a"], "A": ["aA", "b"]}, "S")
    nfa = NonDeterministicFiniteAutomaton(grammar)
    print(nfa)
