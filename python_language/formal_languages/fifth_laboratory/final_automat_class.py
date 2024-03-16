"""
Шаг 2.
Начальный символ грамматики S принять за начальное состояние НКА.
Из не терминалов образовать множество состояний автомата Q =V_n ∪ {N},
а из терминалов – множество символов входного алфавита T = V_t.
"""
from python_language.formal_languages.fifth_laboratory.grammar_class import Grammar


class FiniteAutomaton:
    def __init__(self, grammar: Grammar):
        self.start_state: str = grammar.start_symbol
        self.set_of_states: set[str] = grammar.set_of_non_terminals | {grammar.start_symbol}
        self.set_of_input_alphabet_characters: set[str] = grammar.set_of_terminals
        self.transition_function = grammar.transition_rules

    @property
    def transition_function(self) -> dict[tuple[str, str], str]:
        return self.__transition_function

    @transition_function.setter
    def transition_function(self, transition_rules: dict[str, list[str]]):
        self.__transition_function = {(non_terminal, terminal): next_non_terminal
                                      for non_terminal, productions in transition_rules.items()
                                      for production in productions
                                      for terminal, next_non_terminal in
                                      zip(production, transition_rules.get(non_terminal, []))}