from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class GeffeGeneratorView:
    register1_polynomial: tuple[int, ...]
    register1_start_state: tuple[int, ...]
    register1_shift: int
    register1_column_index: int
    register1_max_period: int
    register2_polynomial: tuple[int, ...]
    register2_start_state: tuple[int, ...]
    register2_shift: int
    register2_column_index: int
    register2_max_period: int
    register3_polynomial: tuple[int, ...]
    register3_start_state: tuple[int, ...]
    register3_shift: int
    register3_column_index: int
    register3_max_period: int
    theoretical_period: int
    actual_sequence_period: int
    register1_sequence: tuple[int, ...]
    register2_sequence: tuple[int, ...]
    register3_sequence: tuple[int, ...]
    final_sequence: tuple[int, ...]
    final_decimal: str
    decimal_sequence: str
    steps: tuple[str, ...]
