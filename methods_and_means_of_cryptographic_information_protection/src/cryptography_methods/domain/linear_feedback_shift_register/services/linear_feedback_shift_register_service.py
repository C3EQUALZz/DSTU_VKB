import logging
from dataclasses import dataclass
from typing import Final
from collections import deque
from copy import copy
from cryptography_methods.domain.common.services.base import DomainService
from cryptography_methods.domain.linear_feedback_shift_register.entities.linear_feedback_shift_register import (
    LinearFeedbackShiftRegister
)
from cryptography_methods.domain.linear_feedback_shift_register.values.register_state import RegisterState

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class LinearFeedbackShiftRegisterSequencePeriodDTO:
    period: int
    output_sequence: str


class LinearFeedbackShiftRegisterService(DomainService):
    def __init__(self) -> None:
        super().__init__()

    # noinspection PyMethodMayBeStatic
    def calculate_sequence_period(
            self,
            register: LinearFeedbackShiftRegister
    ) -> LinearFeedbackShiftRegisterSequencePeriodDTO:
        """
        Вычисляет период последовательности регистра

        Args:
            register:

        Returns: LinearFeedbackShiftRegisterSequencePeriodDTO, где есть период и выходная_последовательность
        """
        # Сохраняем начальное состояние
        initial_state: RegisterState = copy(register.state)
        output_sequence: deque[str] = deque()
        iteration: int = 0

        max_iterations: int = 2 ** len(register.state) * 2  # Защита от бесконечного цикла

        logger.info(f"{'Итерация':<10}{'Новый бит':<10}{'Состояние':<20}{'Выходной бит'}")

        while iteration < max_iterations:
            iteration += 1

            out_bit: int = register.shift()
            output_sequence.append(str(out_bit))

            logger.info(
                f"Iteration: {iteration:<10}"
                f"State: {register.state[0]:<10}"
                f"Register: {str(register):<20}"
                f"Out bit: {out_bit}"
            )

            # Проверяем возврат в исходное состояние
            if register.state == initial_state:
                return LinearFeedbackShiftRegisterSequencePeriodDTO(
                    period=iteration,
                    output_sequence="".join(output_sequence)
                )

        raise ...
