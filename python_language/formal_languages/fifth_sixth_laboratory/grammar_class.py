"""
Шаг 1.
Пополнить грамматику правилом A → aN, где A ∈ VN, a ∈ VT и N - новый не терминал,
для каждого правила вида A → a, если в грамматике нет соответствующего ему правила A → aB, где B ∈ VN.
"""

import re
from typing import Final

RANDOM_SYMBOL: Final = "N"


class Grammar:
    def __init__(self,
                 set_of_terminals: set[str],
                 set_of_non_terminals: set[str],
                 transition_rules: dict[str, list[str]],
                 start_symbol: str = 'S') -> None:

        self.set_of_terminals = set_of_terminals
        self.set_of_non_terminals = set_of_non_terminals
        self.transition_rules = transition_rules
        self.start_symbol = start_symbol

    def __str__(self) -> str:
        """
        Магический метод, который переводит в строку, больше нужен был для вывода в консоль
        """
        string_rules = ', '.join(f'{key} -> {"|".join(value)}' for key, value in self.transition_rules.items())

        return (f"G = (V_t = {self.set_of_terminals},"
                f" V_n = {self.set_of_non_terminals},"
                f" P = ({string_rules}),"
                f" S = {self.start_symbol})")

    @property
    def transition_rules(self) -> dict[str, list[str]]:
        """
        Свойство - геттер, которое нужно, чтобы отрабатывал мой сеттер
        """
        return self.__transition_rules

    @transition_rules.setter
    def transition_rules(self, transition_rules: dict[str, list[str]]) -> None:
        """
        Свойство - сеттер, которое пополняет грамматику правилом A -> aN, где N - произвольный новый не терминал.
        Мы вводим новый не терминал, когда в правиле "не терминал -> терминал" и у нас нет правил вида A -> aB,
        где B принадлежит множеству не терминалов
        """
        for terminal_or_non_terminal_symbol, productions in transition_rules.items():
            if terminal_or_non_terminal_symbol in self.set_of_non_terminals:
                self.__update_production(productions)

        self.__transition_rules = transition_rules

    def __update_production(self, productions: list[str]) -> None:
        """
        Обновление правил и множества не терминалов, если слева до "->" у нас был не терминал
        """

        # Если есть продукция вида 'aB', то ничего не обновляем, переходим к следующей продукции
        for production in productions:
            if any(self.__is_terminal_followed_by_non_terminal(rule) for rule in production):
                return

        # Если все-таки не было продукции вида 'aB', то ищем продукцию вида 'a' и превращаем в 'aN'
        for index, production in enumerate(productions):
            if len(production) == 1 and production in self.set_of_terminals:
                productions[index] = production + RANDOM_SYMBOL
                self.set_of_non_terminals.add(RANDOM_SYMBOL)
                return

    def __is_terminal_followed_by_non_terminal(self, production: str) -> bool:
        """
        Метод для поиска строки вида 'aB' в продукциях
        """

        # Паттерн для поиска терминала, за которым следует не терминал
        pattern = re.compile(fr"[{''.join(self.set_of_terminals)}]([{''.join(self.set_of_non_terminals)}])")

        # Проверяем, соответствует ли строка паттерну
        return bool(re.search(pattern, production))
