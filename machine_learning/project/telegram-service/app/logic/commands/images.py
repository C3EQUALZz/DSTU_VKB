from dataclasses import dataclass

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class ConvertColorImageToGrayScaleImageCommand(AbstractCommand):
    data: bytes
    name: str
    width: int
    height: int
    chat_id: int


@dataclass(frozen=True)
class GetMetadataFromImageCommand(ConvertColorImageToGrayScaleImageCommand):
    ...


@dataclass(frozen=True)
class ConvertGrayScaleImageToColorImageCommand(ConvertColorImageToGrayScaleImageCommand):
    ...


@dataclass(frozen=True)
class CropImageCommand(AbstractCommand):
    data: bytes
    name: str
    old_width: int
    old_height: int
    new_width: int
    new_height: int
    chat_id: int


@dataclass(frozen=True)
class RotateImageCommand(ConvertColorImageToGrayScaleImageCommand):
    angle: int
