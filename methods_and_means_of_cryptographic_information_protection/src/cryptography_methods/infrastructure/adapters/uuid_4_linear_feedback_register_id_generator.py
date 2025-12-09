import uuid
from typing_extensions import override, cast

from cryptography_methods.domain.linear_feedback_shift_register.services.id_generator import (
    LinearFeedbackShiftRegisterGeneratorID
)
from cryptography_methods.domain.linear_feedback_shift_register.values.register_id import RegisterID


class UUID4LinearFeedbackRegisterIDGenerator(LinearFeedbackShiftRegisterGeneratorID):
    @override
    def __call__(self) -> RegisterID:
        return cast(RegisterID, uuid.uuid4())