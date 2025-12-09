import logging
from collections import deque
from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.domain.linear_feedback_shift_register.entities.linear_feedback_shift_register import (
    LinearFeedbackShiftRegister
)
from cryptography_methods.domain.linear_feedback_shift_register.services.id_generator import (
    LinearFeedbackShiftRegisterGeneratorID
)
from cryptography_methods.domain.linear_feedback_shift_register.services.linear_feedback_shift_register_service import (
    LinearFeedbackShiftRegisterService, LinearFeedbackShiftRegisterSequencePeriodDTO
)
from cryptography_methods.domain.linear_feedback_shift_register.values.feedback_positions import FeedbackPositions
from cryptography_methods.domain.linear_feedback_shift_register.values.register_state import RegisterState

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class MutateLinearFeedbackShiftRegisterCommand:
    sequence: str
    polynom: str


@final
class MutateLinearFeedbackShiftRegisterCommandHandler:
    def __init__(
            self,
            linear_feedback_shift_register_service: LinearFeedbackShiftRegisterService,
            id_generator: LinearFeedbackShiftRegisterGeneratorID
    ) -> None:
        self._service: Final[LinearFeedbackShiftRegisterService] = linear_feedback_shift_register_service
        self._id_generator: Final[LinearFeedbackShiftRegisterGeneratorID] = id_generator

    async def __call__(
            self,
            data: MutateLinearFeedbackShiftRegisterCommand
    ) -> LinearFeedbackShiftRegisterSequencePeriodDTO:
        logger.info(
            "Started LFSR algorithm with sequence: %s and polynom: %s",
            data.sequence,
            data.polynom
        )

        # if len(data.polynom) != len(data.sequence):
        #     logger.info(
        #         "Length of polynom %s and sequence %s are not equal",
        #         len(data.polynom),
        #         len(data.sequence)
        #     )
        #
        #     sequence = data.sequence[len(data.sequence) - len(data.polynom):]
        #
        #     logger.info("New sequence: %s", sequence)

        # Преобразуем бинарную строку полинома в список позиций обратной связи
        # Полином читается СПРАВА НАЛЕВО: младший бит (x^0) справа, старший (x^n) слева
        # Например, "1100011" читается справа налево как: x^0, x^1, x^5, x^6
        # Это означает полином x^6 + x^5 + x + 1
        # В LFSR позиции обратной связи указываются от конца регистра
        # Позиция от конца регистра = степень полинома
        polynom_bits = list(map(int, list(data.polynom)))
        register_length = len(data.sequence)
        feedback_positions_list = []
        
        # Проходим по битам полинома справа налево (от младшего к старшему)
        # Позиция i справа соответствует степени x^i
        # Позиция от конца регистра равна степени полинома
        for i, bit in enumerate(reversed(polynom_bits)):
            if bit == 1:
                # Степень полинома = позиция i (от младшего бита)
                degree = i
                # Позиция от конца регистра равна степени полинома
                # Проверяем, что позиция не выходит за границы регистра
                if degree < register_length:
                    feedback_positions_list.append(degree)
        
        # Убираем дубликаты и сортируем
        feedback_positions_list = sorted(set(feedback_positions_list))
        
        logger.info(
            "Polynom bits: %s, Feedback positions (from end): %s",
            polynom_bits,
            feedback_positions_list
        )
        
        if not feedback_positions_list:
            raise ValueError(
                f"Не удалось определить позиции обратной связи из полинома {data.polynom}. "
                f"Проверьте, что полином содержит хотя бы одну единицу."
            )
        
        initial_register: LinearFeedbackShiftRegister = LinearFeedbackShiftRegister(
            id=self._id_generator(),
            state=RegisterState(deque(map(int, list(data.sequence)))),
            feedback_positions=FeedbackPositions(feedback_positions_list)
        )

        dto: LinearFeedbackShiftRegisterSequencePeriodDTO = self._service.calculate_sequence_period(
            initial_register
        )

        return dto
