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
from collections import defaultdict

from python_language.formal_languages.fifth_laboratory.grammar_class import Grammar


class FiniteAutomaton:
    def __init__(self, grammar: Grammar) -> None:
        """
        M = (Q, T, F, H, Z), где:
        - Q - множество состояний (set_of_states)
        - T - множество символов входного алфавита (set_of_input_alphabet_characters)
        - F - функции перехода (transition_function)
        - H - начальный символ автомата (start_state)
        - Z - множество конечных состояний (final_states)
        """
        self.start_state: str = grammar.start_symbol
        self.set_of_states: set[str] = grammar.set_of_non_terminals | {grammar.start_symbol}
        self.set_of_input_alphabet_characters: set[str] = grammar.set_of_terminals
        self.transition_function = grammar.transition_rules
        self.final_states: set[str] = self.calculate_final_states(grammar)

    @property
    def transition_function(self) -> dict[tuple[str, str], list[str]]:
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
        self.__transition_function = defaultdict(list)

        for non_terminal, productions in transition_rules.items():
            for production in productions:
                self.__process_production(production=production, non_terminal=non_terminal)

    def __process_production(self, production: str, non_terminal: str) -> None:
        """
        Обрабатывает каждую продукцию и обновляет функцию перехода.

        Args:
            production: очередная продукция, которую мы хотим добавить в функцию перехода (значение словаря).
            non_terminal: не терминальный символ, который идет в качестве ключа.
        Returns:
            Ничего не возвращает, только добавляет элементы в словарь
        """
        for i in range(len(production) - 1):
            # Если символ - терминал
            if production[i] in self.set_of_input_alphabet_characters:
                self.__transition_function[(non_terminal, production[i])].append(production[i + 1])

    def calculate_final_states(self, grammar: Grammar) -> set[str]:
        final_states = set()
        for non_terminal, productions in grammar.transition_rules.items():
            for production in productions:

                if len(production) == 1 and production[0] in ('ε', "E", "e"):
                    final_states.add(self.start_state)

                for i in range(len(production) - 1):
                    if production[i + 1] in grammar.set_of_non_terminals:
                        final_states.add(production[i])

        return final_states

    def __str__(self) -> str:
        """
        Магический метод, который нужен для перевода в строку. В моем случае использование для print
        """
        return (f"M = ({self.set_of_states},"
                f" {self.set_of_input_alphabet_characters},"
                f" {self.transition_function},"
                f" {self.start_state},"
                f" {self.final_states})")


if __name__ == '__main__':
    grammar = Grammar({"a", "b"}, {"S", "A", "B"}, {"S": ["aB", "aA"], "B": ["bB", "a"], "A": ["aA", "b"]})
    print(grammar.transition_rules)
    nda = FiniteAutomaton(grammar)
    print(nda)
