"""
Построение КА по регулярной грамматике

Полезные источники:
- https://youtu.be/kAIc96Jk-0s?si=ohJRxUQEt69cKnsh
- https://youtu.be/oQvjgb0EHvw?si=ntVYjok9tLf3F-Dc

"""
import re
from random import choice
from string import ascii_uppercase
from typing import Final

RANDOM_SYMBOL: Final = choice(ascii_uppercase)


class Grammar:
    def __init__(self,
                 set_of_terminals: set[str],
                 set_of_non_terminals: set[str],
                 transition_rules: dict[str, list[str]],
                 start_symbol: str = 'S') -> None:

        self._set_of_terminals = set_of_terminals
        self._set_of_non_terminals = set_of_non_terminals
        self._transition_rules = transition_rules
        self._start_symbol = start_symbol

    @property
    def transition_rules(self) -> dict[str, list[str]]:
        return self._transition_rules

    @transition_rules.setter
    def transition_rules(self, transition_rules) -> None:
        for non_terminal, productions in transition_rules.items():
            self.__update_production(productions)

    def __update_production(self, productions: list[str]) -> None:
        # if any(re.match(r'^[A-Z] -> (?:[^A-Z]*[A-Z]|\W+)', production) for production in productions):
        #     return

        for index, production in enumerate(productions):
            if len(production) == 1 and production.islower():
                productions[index] = production + RANDOM_SYMBOL
                self._set_of_terminals.add(RANDOM_SYMBOL)
                return

    def __str__(self) -> str:
        return (f"G = (V_t = {self._set_of_terminals},"
                f" V_n = {self._set_of_non_terminals},"
                f" P = ({", ".join(f"{key} -> {'|'.join(value)}" for key, value in self.transition_rules.items())}),"
                f" S = {self._start_symbol})")


# S -> 1C|0D; C -> 0D|0S|1; D -> 1C|1S|0

if __name__ == "__main__":
    g = Grammar(
        {"S", "C", "D"},
        {"0", "1"},
        {"S": ["1", "0"], "C": ["0D", "OS", "1"], "D": ["1C", "1S", "0"]},
        "S"
    )

    print(g)
