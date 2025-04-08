from dataclasses import dataclass
from typing import Literal

import numpy as np

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class EncodeCascadeCodeCommand(AbstractCommand):
    data: np.ndarray[tuple[str, str, str]]
    matrix_for_block_code: list[list[int]]
    type_of_matrix: Literal["G", "H"]
    indexes: list[list[int]]


@dataclass(frozen=True)
class DecodeCascadeCodeCommand(AbstractCommand):
    data: str
    matrix_for_block_code: list[list[int]]
    type_of_matrix: Literal["G", "H"]
    indexes: list[list[int]]
