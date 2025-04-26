from dataclasses import dataclass

from app.logic.events.base import AbstractEvent


@dataclass(frozen=True)
class ConvertColorImageToGrayScaleImageEvent(AbstractEvent):
    data: bytes
    name: str
    width: int
    height: int
    chat_id: int


@dataclass(frozen=True)
class GetMetadataFromImageEvent(ConvertColorImageToGrayScaleImageEvent):
    ...


@dataclass(frozen=True)
class ConvertGrayScaleImageToColorImageEvent(ConvertColorImageToGrayScaleImageEvent):
    ...


@dataclass(frozen=True)
class CropImageEvent(ConvertColorImageToGrayScaleImageEvent):
    ...


@dataclass(frozen=True)
class RotateImageEvent(ConvertColorImageToGrayScaleImageEvent):
    ...
