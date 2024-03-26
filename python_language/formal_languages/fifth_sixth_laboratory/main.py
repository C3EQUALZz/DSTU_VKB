"""
Построение КА по регулярной грамматике

Полезные источники:
- https://youtu.be/kAIc96Jk-0s?si=ohJRxUQEt69cKnsh
- https://youtu.be/oQvjgb0EHvw?si=ntVYjok9tLf3F-Dc
- http://www.cs.um.edu.mt/gordon.pace/Research/Software/Relic/Transformations/RG/toFSA.html

"""
from python_language.formal_languages.fifth_sixth_laboratory.grammar_class import Grammar
from python_language.formal_languages.fifth_sixth_laboratory.non_det_final_automat_class import (
    NonDeterministicFiniteAutomaton)
from python_language.formal_languages.fifth_sixth_laboratory.det_final_automat_class import DeterministicFiniteAutomaton


def main() -> None:
    """
    Здесь ввод
    """
    grammar = Grammar(
        {"0", "1", "~", "!"},
        {"I", "J", "K", "M", "N"},
        {"I": ["0J", "1K", "0M"],
         "B": ["~K", "0M"],
         "K": ["~M", "0J", "0N"],
         "M": ["1K", "!"],
         "N": ["0I", "1I", "!"]},
        "I")
    nfa = NonDeterministicFiniteAutomaton(grammar)
    nfa.show_diagram()
    d = DeterministicFiniteAutomaton(nfa)
    d.show_diagram()


if __name__ == "__main__":
    main()
