from dataclasses import dataclass
from typing import final

from cryptography_methods.application.common.views.double_square_whitestone import DoubleSquareWhitestoneDecryptView


@dataclass(frozen=True, slots=True, kw_only=True)
class DecryptDoubleSquareWhitestoneCommand:
    text: str
    key_for_decryption: tuple[list[str], list[str]] | None = None


@final
class DecryptDoubleSquareWhitestoneCommandHandler:
    def __init__(self) -> None:
        ...

    async def __call__(self, data: DecryptDoubleSquareWhitestoneCommand) -> DoubleSquareWhitestoneDecryptView:
        ...
