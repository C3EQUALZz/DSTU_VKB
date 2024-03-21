from python_language.formal_languages.fifth_sixth_laboratory.det_final_automat_class import DeterministicFiniteAutomaton


class MinifiedDFA:
    def __init__(self, dfa: DeterministicFiniteAutomaton) -> None:
        self.start_state: str = dfa.start_state
        self.set_of_input_alphabet_characters: set[str] = dfa.set_of_input_alphabet_characters
        self.set_of_states = dfa.set_of_states
        self.transition_function = dfa.transition_function
        self.final_states = dfa.final_states




def main() -> None:
    states = {"A", "B", "C", "D", "E", "F", "G"}
    alphabet = {"a", "b"}
    start = "A"
    final_states = {"D", "E"}
