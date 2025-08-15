from abc import abstractmethod
from typing import Protocol

from cryptography_methods.domain.linear_feedback_shift_register.values.register_id import RegisterID


class LinearFeedbackShiftRegisterGeneratorID(Protocol):
    @abstractmethod
    def __call__(self) -> RegisterID:
        ...
