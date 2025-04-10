from dataclasses import dataclass

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class EncodeConvolutionalCodeCommand(AbstractCommand):
    data: str
    indexes: list[list[int]]


@dataclass(frozen=True)
class DecodeConvolutionalCodeCommand(AbstractCommand):
    data: str
    indexes: list[list[int]]
