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

    async def __call__(self, data: MutateLinearFeedbackShiftRegisterCommand):
        logger.info("Started LFSR algorithm...")
        initial_register: LinearFeedbackShiftRegister = LinearFeedbackShiftRegister(
            id=self._id_generator(),
            state=RegisterState(deque(map(int, list(data.sequence)))),
            feedback_positions=FeedbackPositions(list(map(int, data.polynom.split())))
        )

        dto: LinearFeedbackShiftRegisterSequencePeriodDTO = self._service.calculate_sequence_period(initial_register)
