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

Ввод из примера лежит в main, через консоль можете сделать сами
"""
import os
from collections import defaultdict, deque
from typing import Final, Self, AnyStr, Set, MutableMapping, List
from dataclasses import dataclass

from automata.fa.dfa import DFA
from automata.fa.nfa import NFA

from python_language.formal_languages.fifth_sixth_laboratory.grammar_class import Grammar
from python_language.formal_languages.fifth_sixth_laboratory.non_det_final_automat_class import (
    NonDeterministicFiniteAutomaton)

PATH_TO_DIAGRAM: Final = os.path.join(os.path.curdir, "test_dfa.png")


@dataclass
class DeterministicFiniteAutomaton:
    start_state: AnyStr
    set_of_input_alphabet_characters: Set[AnyStr]
    set_of_states: Set[AnyStr]
    transition_function: MutableMapping[AnyStr, MutableMapping[AnyStr, Set[AnyStr]]]
    final_states: Set[AnyStr]

    def __post_init__(self) -> None:
        """
        Действия, которые должны быть запущены после __init__
        """
        self.__construct_dfa()

    @classmethod
    def from_nfa(cls, nfa: NonDeterministicFiniteAutomaton) -> Self:
        """
        Классовый метод, который возвращает наш класс
        """
        return cls(
            start_state=nfa.start_state,
            set_of_input_alphabet_characters=nfa.set_of_input_alphabet_characters,
            set_of_states=nfa.set_of_states,
            transition_function=nfa.transition_function,
            final_states=nfa.final_states
        )

    def __construct_dfa(self) -> None:
        """
        Метод, с помощью которого начинается запуск построения ДКА
        """
        dfa_transitions = defaultdict(dict)
        unmarked_states = deque([self.__epsilon_closure({self.start_state})])
        marked_states = []

        while unmarked_states:
            current_state_set = unmarked_states.popleft()
            marked_states.append(current_state_set)

            self.__add_final_state(current_state_set)
            self.__fill_dfa_transition(current_state_set, marked_states, unmarked_states, dfa_transitions)

        self.transition_function = dfa_transitions
        self.set_of_states = {self._states_to_string(state) for state in marked_states if state}
        self.final_states = {state for state in self.set_of_states if state in self.final_states}
        self.start_state = next(iter([state for state in self.transition_function if self.start_state in state]))

    def __fill_dfa_transition(self,
                              current_state_set: Set[AnyStr],
                              marked_states: List[Set[AnyStr]],
                              unmarked_states: deque[Set[AnyStr]],
                              dfa_transitions: MutableMapping[AnyStr, MutableMapping[AnyStr, Set[AnyStr]]]
                              ) -> MutableMapping[AnyStr, MutableMapping[AnyStr, Set[AnyStr]]]:
        """
        Метод, который заполняет таблицу переходов для ДКА
        Args:
            current_state_set: текущее состояние
            marked_states: проверенные вершины
            unmarked_states: непроверенные вершины
            dfa_transitions: таблица переходов
        """
        for symbol in self.set_of_input_alphabet_characters:
            next_state_set = self.__epsilon_closure(self.__transition(current_state_set, symbol))

            if next_state_set not in marked_states:
                unmarked_states.append(next_state_set)

            if current_state_set:
                dfa_transitions[self._states_to_string(current_state_set)].update(
                    {symbol: {self._states_to_string(next_state_set)} if self._states_to_string(
                        next_state_set) else {}})

        return dfa_transitions

    def __add_final_state(self, current_state_set: Set[AnyStr]) -> None:
        """
        Если хотя бы одно состояние в текущем множестве является финальным,
        то текущее множество состояний ДКА также становится финальным
        """
        if any(state in self.final_states for state in current_state_set):
            self.final_states.add(self._states_to_string(current_state_set))

    def __transition(self, state_set: Set[AnyStr], symbol: AnyStr) -> Set[AnyStr] | Set[Set[AnyStr]]:
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

    def __epsilon_closure(self, state_set: Set[AnyStr]) -> Set[AnyStr]:
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

    def get_library_dfa(self) -> DFA:
        """
        Получение исходного ДКА из библиотеки для удобного отображения таблицы
        """
        return DFA.from_nfa(NFA(
            states=self.set_of_states,
            input_symbols=self.set_of_input_alphabet_characters,
            transitions=self.transition_function,
            initial_state=self.start_state,
            final_states=self.final_states,
        ), retain_names=True)

    def show_diagram(self) -> None:
        """
        Метод, который создает граф на основе автомата
        """
        self.get_library_dfa().show_diagram(path=PATH_TO_DIAGRAM)

    @staticmethod
    def _states_to_string(state_set: Set[AnyStr]) -> AnyStr:
        """
        Вспомогательный метод для перевода множества состояний в строку для библиотеки
        """
        return ''.join(sorted(state_set))


def main() -> None:
    grammar = Grammar({"a", "b"}, {"S", "A", "B"}, {"S": ["aB", "aA"], "B": ["bB", "a"], "A": ["aA", "b"]}, "S")
    nfa = NonDeterministicFiniteAutomaton(grammar)
    nfa.show_diagram()
    d = DeterministicFiniteAutomaton.from_nfa(nfa)
    d.show_diagram()
    print(d)


if __name__ == "__main__":
    main()
