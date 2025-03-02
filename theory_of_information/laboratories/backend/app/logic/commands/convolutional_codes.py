from app.logic.commands.base import AbstractCommand
from dataclasses import dataclass


@dataclass(frozen=True)
class EncodeConvolutionalCodeCommand(AbstractCommand):
    data: str
    indexes: list[list[int]]


@dataclass(frozen=True)
class DecodeConvolutionalCodeCommand(AbstractCommand):
    data: str
    indexes: list[list[int]]
