"""
Построение КА по регулярной грамматике

Полезные источники:
- https://youtu.be/kAIc96Jk-0s?si=ohJRxUQEt69cKnsh
- https://youtu.be/oQvjgb0EHvw?si=ntVYjok9tLf3F-Dc
- http://www.cs.um.edu.mt/gordon.pace/Research/Software/Relic/Transformations/RG/toFSA.html

"""

from formal_languages.fifth_sixth_laboratory.det_final_automat_class import \
    DeterministicFiniteAutomaton
from formal_languages.fifth_sixth_laboratory.grammar_class import Grammar
from formal_languages.fifth_sixth_laboratory.non_det_final_automat_class import \
    NonDeterministicFiniteAutomaton
from formal_languages.fifth_sixth_laboratory.table_ex import make_table


def main() -> None:
    """
    Здесь можете осуществить ввод с консоли, мне лично удобнее так сразу задавать, как сейчас, чем каждый раз вводить
    """
    grammar = Grammar(
        {"a", "b"},
        {"S", "A", "B"},
        {"S": ["aB", "aA"], "B": ["bB", "a"], "A": ["aA", "b"]},
        "S",
    )

    nfa = NonDeterministicFiniteAutomaton(grammar)
    nfa.show_diagram()
    print(nfa)

    dfa = DeterministicFiniteAutomaton.from_nfa(nfa)
    dfa.show_diagram()
    print(dfa)

    print(make_table(dfa.get_library_dfa()))


if __name__ == "__main__":
    main()
