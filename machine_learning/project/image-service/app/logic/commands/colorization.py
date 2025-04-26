from dataclasses import dataclass

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class ConvertColorToGrayScaleCommand(AbstractCommand):
    data: bytes
    width: int
    height: int
    name: str


@dataclass(frozen=True)
class ConvertColorToGrayScaleAndSendToChatCommand(ConvertColorToGrayScaleCommand):
    chat_id: int


@dataclass(frozen=True)
class ConvertGrayScaleToColorCommand(AbstractCommand):
    data: bytes
    width: int
    height: int
    name: str


@dataclass(frozen=True)
class ConvertGrayScaleToColorAndSendToChatCommand(ConvertGrayScaleToColorCommand):
    chat_id: int
