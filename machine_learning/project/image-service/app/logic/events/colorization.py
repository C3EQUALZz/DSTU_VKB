from dataclasses import dataclass

from app.logic.events.base import AbstractEvent


@dataclass(frozen=True)
class ConvertColorToGrayScaleAndSendToChatEvent(AbstractEvent):
    data: bytes
    width: int
    height: int
    name: str
    chat_id: int


@dataclass(frozen=True)
class ConvertGrayScaleToColorAndSendToChatEvent(ConvertColorToGrayScaleAndSendToChatEvent):
    ...


@dataclass(frozen=True)
class StylizeAndSendToChatEvent(AbstractEvent):
    original_image_data: bytes
    original_width: int
    original_height: int
    original_name: str
    style_image_data: bytes
    style_width: int
    style_height: int
    style_name: str
    chat_id: int


@dataclass(frozen=True)
class ConvertImageInversionAndSendToChatEvent(ConvertColorToGrayScaleAndSendToChatEvent):
    ...
