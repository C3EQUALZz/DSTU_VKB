from dataclasses import dataclass
from typing import override

from app.domain.values.base import BaseValueObject
from app.exceptions.domain import NonExistentNeuralNetworkWasSelected


@dataclass
class TextModel(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if self.value not in ("chat-gpt", "deepseek"):
            raise NonExistentNeuralNetworkWasSelected(f"{self.value} is not a valid neural network")

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass
class ImageModel(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if self.value not in ("chat-gpt", "stable-diffusion"):
            raise NonExistentNeuralNetworkWasSelected(f"{self.value} is not a valid neural network")

    @override
    def as_generic_type(self) -> str:
        return str(self.value)
