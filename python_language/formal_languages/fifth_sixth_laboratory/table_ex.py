"""
Данный отрывок был взят с библиотеки automata
Нужен для ребят с ВМО и ВПР, для ВКБ не надо
"""

import pandas as pd


def make_table(target_fa) -> pd.DataFrame:
    initial_state = target_fa.initial_state
    final_states = target_fa.final_states

    table = {}

    for from_state, to_state, symbol in target_fa.iter_transitions():
        # Prepare nice string for from_state
        from_state_str = ''.join(map(str, *from_state))
        if from_state in final_states:
            from_state_str = "*" + from_state_str
        if from_state == initial_state:
            from_state_str = "→" + from_state_str

        # Prepare nice string for to_state
        to_state_str = ''.join(map(str, *to_state))
        if to_state in final_states:
            to_state_str = "*" + to_state_str

        # Prepare nice symbol
        if symbol == "":
            symbol = "λ"

        from_state_dict = table.setdefault(from_state_str, dict())
        from_state_dict.setdefault(symbol, set()).add(to_state_str)

    # Convert sets to strings
    for from_state, transitions in table.items():
        for symbol, to_states in transitions.items():
            table[from_state][symbol] = ', '.join(to_states)

    df = pd.DataFrame.from_dict(table).fillna("∅").T
    return df.reindex(sorted(df.columns), axis=1)
