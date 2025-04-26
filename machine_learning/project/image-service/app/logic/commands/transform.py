from dataclasses import dataclass

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class CropImageCommand(AbstractCommand):
    data: bytes
    name: str
    old_width: int
    old_height: int
    new_width: int
    new_height: int


@dataclass(frozen=True)
class CropImageAndSendToChatCommand(CropImageCommand):
    chat_id: int


@dataclass(frozen=True)
class RotateImageCommand(AbstractCommand):
    data: bytes
    name: str
    width: int
    height: int
    angle: int


@dataclass(frozen=True)
class RotateImageAndSendToChatCommand(RotateImageCommand):
    chat_id: int
