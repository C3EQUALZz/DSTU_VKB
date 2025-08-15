from dataclasses import dataclass

from typing_extensions import override

from cryptography_methods.domain.common.entities.base_entity import BaseEntity
from cryptography_methods.domain.linear_feedback_shift_register.values.feedback_positions import FeedbackPositions
from cryptography_methods.domain.linear_feedback_shift_register.values.register_id import RegisterID
from cryptography_methods.domain.linear_feedback_shift_register.values.register_state import RegisterState


@dataclass(eq=False, kw_only=True)
class LinearFeedbackShiftRegister(BaseEntity[RegisterID]):
    """
    Регистр сдвига с линейной обратной связью (LFSR)

    :param state: Начальное состояние регистра (список битов)
    :param feedback_positions: Позиции для обратной связи (индексы с конца регистра)
    """
    state: RegisterState
    feedback_positions: FeedbackPositions

    def __post_init__(self) -> None:
        super().__post_init__()

        if len(self.state) == 0:
            raise ValueError("Длина состояния регистра должна быть > 0")

        if len(self.feedback_positions) == 0:
            raise ValueError("Должна быть указана хотя бы одна позиция обратной связи")

        if max(self.feedback_positions) >= len(self.state):
            raise ValueError(f"Позиции должны быть меньше длины регистра ({len(self.state)})")

    def shift(self) -> int:
        """
        Выполняет один такт работы регистра
        """
        feedback_bit: int = sum(self.state[-(pos + 1)] for pos in self.feedback_positions) % 2
        out_bit: int = self.state.pop()
        self.state.append_left(feedback_bit)
        return out_bit

    @override
    def __str__(self) -> str:
        return "".join(map(str, self.state))
