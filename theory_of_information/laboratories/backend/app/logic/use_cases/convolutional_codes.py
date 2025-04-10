from itertools import product
from typing import Final

from app.infrastructure.services.convolutional_codes import \
    ConvolutionalCodesService
from app.logic.commands.convolutional_codes import (
    DecodeConvolutionalCodeCommand, EncodeConvolutionalCodeCommand)
from app.logic.use_cases.base import BaseUseCase

SEQUENCE: Final[tuple[str, str]] = ("0", "1")


class EncodeConvolutionalCodeUseCase(BaseUseCase[EncodeConvolutionalCodeCommand]):
    def __init__(self, service: ConvolutionalCodesService) -> None:
        self._service = service

    async def __call__(self, command: EncodeConvolutionalCodeCommand) -> str:
        binary_string = "".join(
            format(x, "08b") for x in bytearray(command.data, "utf-8")
        )

        count_of_register: int = max(max(sublist) for sublist in command.indexes) + 1

        non_filtered_pols = (
            "".join(comb) for comb in product(SEQUENCE, repeat=count_of_register)
        )
        filtered_pols = filter(lambda pol: pol.count("1") > 2, non_filtered_pols)
        pols: str = ",".join(filtered_pols)

        return self._service.encode(binary_string, pols)


class DecodeConvolutionalCodeUseCase(BaseUseCase[DecodeConvolutionalCodeCommand]):
    def __init__(self, service: ConvolutionalCodesService) -> None:
        self._service = service

    async def __call__(self, command: DecodeConvolutionalCodeCommand) -> str:
        count_of_register: int = max(max(sublist) for sublist in command.indexes) + 1

        non_filtered_pols = (
            "".join(comb) for comb in product(SEQUENCE, repeat=count_of_register)
        )
        filtered_pols = filter(lambda pol: pol.count("1") > 2, non_filtered_pols)
        pols: str = ",".join(filtered_pols)

        binary_string = self._service.decode(command.data, pols)

        byte_chunks = [
            binary_string[i : i + 8] for i in range(0, len(binary_string), 8)
        ]

        byte_array = bytearray(int(byte, 2) for byte in byte_chunks)

        return "".join(
            char for char in byte_array.decode("utf-8") if char.isprintable()
        )
