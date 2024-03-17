"""
Шаг 2.
Начальный символ грамматики S принять за начальное состояние НКА.
Из не терминалов образовать множество состояний автомата Q =V_n ∪ {N},
а из терминалов – множество символов входного алфавита T = V_t.

Шаг 3. Каждое правило A → aB преобразовать в функцию переходов
F (A, a) = B, где A, B ∈ V_n, a ∈ V_t.

Шаг 4. Во множество заключительных состояний включить все вершины,
помеченные символами B ∈ V_n из правил вида A → aB, для которых имеются
соответствующие правила A→a, где A, B ∈ V_n, a ∈ V_t.

Шаг 5. Если в грамматике имеется правило S → ε, где S - начальный
символ грамматики, то поместить S во множество заключительных
состояний.

Примеры смотрите в методичке.
"""
import os
from collections import defaultdict
from typing import Final, Any

from automata.fa.nfa import NFA

from python_language.formal_languages.fifth_laboratory.grammar_class import Grammar

PATH_TO_DIAGRAM: Final = os.path.join(os.path.curdir, "test_nfa.png")


class NonDeterministicFiniteAutomaton:
    def __init__(self, grammar: Grammar) -> None:
        """
        M = (Q, T, F, H, Z), где:
        - Q - множество состояний (set_of_states)
        - T - множество символов входного алфавита (set_of_input_alphabet_characters)
        - F - функции перехода (transition_function)
        - H - начальный символ автомата (start_state)
        - Z - множество заключительных состояний (final_states)
        """
        self.start_state: str = grammar.start_symbol
        self.set_of_states: set[str] = grammar.set_of_non_terminals | {grammar.start_symbol}
        self.set_of_input_alphabet_characters: set[str] = grammar.set_of_terminals
        self.transition_function = grammar.transition_rules
        self.final_states = grammar.transition_rules

    @property
    def transition_function(self) -> dict[str, defaultdict[Any, set]]:
        """
        Свойство - геттер, которую возвращает функцию переходов
        """
        return self.__transition_function

    @transition_function.setter
    def transition_function(self, transition_rules: dict[str, list[str]]) -> None:
        """
        Свойство - сеттер, которое устанавливает функцию перехода из грамматики

        Args:
            transition_rules: правила перехода в регулярной грамматике

        Returns:
            Ничего не возвращает, только создает функции перехода НДА автомата
        """
        self.__transition_function = {}

        for non_terminal, productions in transition_rules.items():
            transition_dict = defaultdict(set)
            for production in productions:
                self.__process_production(production=production, transition_dict=transition_dict)

            if transition_dict:
                self.__transition_function[non_terminal] = transition_dict

    def __process_production(self, production: str, transition_dict: dict) -> None:
        """
        Обрабатывает каждую продукцию и обновляет функцию перехода.

        Args:
            production: очередная продукция, которую мы хотим добавить в функцию перехода (значение словаря).
            transition_dict: словарь, в который добавляются переходы
        Returns:
            Ничего не возвращает, только добавляет элементы в словарь
        """
        for i in range(len(production) - 1):
            # Если символ - терминал
            if production[i] in self.set_of_input_alphabet_characters:
                transition_dict[production[i]].add(production[i + 1])

    @property
    def final_states(self) -> set[str]:
        """
        Свойство - геттер, которое возвращает множество заключительных состояний
        """
        return self.__final_states

    @final_states.setter
    def final_states(self, transition_rules: dict[str, list[str]]) -> None:
        """
        Множество заключительных состояний, здесь, видимо, идет поиск новых терминалов, как я понял из примера
        """
        self.__final_states = self.set_of_states - set(transition_rules.keys())

        if any(rule in ("E", "e", "ε") for rule in transition_rules[self.start_state]):
            self.__final_states.add(self.start_state)

    def __str__(self) -> str:
        """
        Магический метод, который нужен для перевода в строку. В моем случае использование для print
        """
        return (f"M = ({self.set_of_states},"
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
