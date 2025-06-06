from dataclasses import dataclass

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class ConvertColorToGrayScaleCommand(AbstractCommand):
    data: bytes
    width: int
    height: int
    name: str


@dataclass(frozen=True)
class ConvertGrayScaleToColorCommand(AbstractCommand):
    data: bytes
    width: int
    height: int
    name: str


@dataclass(frozen=True)
class StylizeCommand(AbstractCommand):
    original_image_data: bytes
    original_width: int
    original_height: int
    original_name: str
    style_image_data: bytes
    style_width: int
    style_height: int
    style_name: str
