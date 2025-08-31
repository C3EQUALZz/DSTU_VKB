from dataclasses import dataclass
from typing import final

from cryptography_methods.application.common.views.double_square_whitestone import DoubleSquareWhitestoneDecryptView


@dataclass(frozen=True, slots=True, kw_only=True)
class DecryptDoubleSquareWhitestoneCommand:
    text: str
    left_table: list[list[str]]
    right_table: list[list[str]]


@final
class DecryptDoubleSquareWhitestoneCommandHandler:
    def __init__(self) -> None:
        ...

    async def __call__(self, data: DecryptDoubleSquareWhitestoneCommand) -> DoubleSquareWhitestoneDecryptView:
        ...
