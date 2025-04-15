from dataclasses import dataclass

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class ColorizeImageCommand(AbstractCommand):
    data: bytes
    chat_id: int
