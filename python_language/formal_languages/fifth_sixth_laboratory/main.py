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


def main() -> None:
    """
    Здесь ввод
    """
    grammar = Grammar(
        {"a", "b"},
        {"S", "A", "B"},
        {"S": ["aB", "aA"], "B": ["bB", "a"], "A": ["aA", "b"]},
        "S")
    nfa = NonDeterministicFiniteAutomaton(grammar)
    nfa.show_diagram()
    print(nfa)


if __name__ == "__main__":
    main()
