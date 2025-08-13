from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MutateLinearFeedbackShiftRegisterView:
    result_sequence: str
    removed_chars: str
