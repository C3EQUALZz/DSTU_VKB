from dataclasses import dataclass
from typing import final


@dataclass(frozen=True, slots=True)
class MutateLinearFeedbackShiftRegisterCommand:
    sequence: str
    polynom: str


@final
class MutateLinearFeedbackShiftRegisterCommandHandler:
    def __init__(self) -> None:
        ...

    async def __call__(self, data: MutateLinearFeedbackShiftRegisterCommand):
        ...
