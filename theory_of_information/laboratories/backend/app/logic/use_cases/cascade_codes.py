import logging
from itertools import product
from typing import cast

import numpy as np
from app.infrastructure.services.block_codes import BlockCodesService
from app.infrastructure.services.convolutional_codes import \
    ConvolutionalCodesService
from app.infrastructure.services.interleaver import InterleaveService
from app.logic.commands.cascade_codes import (DecodeCascadeCodeCommand,
                                              EncodeCascadeCodeCommand,
                                              ShowNoisyImageCommand)
from app.logic.use_cases.base import BaseUseCase
from app.logic.use_cases.convolutional_codes import SEQUENCE

logger = logging.getLogger(__name__)


class EncodeCascadeCodeUseCase(BaseUseCase[EncodeCascadeCodeCommand]):
    def __init__(
        self,
        block_code: BlockCodesService,
        interleave_service: InterleaveService,
        convolutional_service: ConvolutionalCodesService,
    ) -> None:
        self._block_code_service: BlockCodesService = block_code
        self._interleave_service: InterleaveService = interleave_service
        self._convolutional_service: ConvolutionalCodesService = convolutional_service

    async def __call__(self, command: EncodeCascadeCodeCommand) -> str:
        block_encoded: np.ndarray[np.ndarray[str]] = self._block_code_service.encode(
            data=command.data,
            matrix=command.matrix_for_block_code,
            type_matrix=command.type_of_matrix,
        )

        logger.info(
            "Закодированная последовательность после блочного кодирования: %s",
            block_encoded,
        )

        interleaved_matrix: np.ndarray[np.ndarray[str]] = (
            self._interleave_service.execute(block_encoded)
        )

        logger.info("После блочного перемежителя: %s", interleaved_matrix)

        data: str = "".join("".join(x) for x in interleaved_matrix)

        count_of_register: int = max(max(sublist) for sublist in command.indexes) + 1

        logger.info("Количество регистров: %s", count_of_register)

        non_filtered_pols = (
            "".join(comb) for comb in product(SEQUENCE, repeat=count_of_register)
        )
        filtered_pols: filter = filter(
            lambda pol: pol.count("1") > 2, non_filtered_pols
        )
        pols: str = ",".join(filtered_pols)

        encoded_data: str = self._convolutional_service.encode(
            data=data,
            pols=pols,
        )

        logger.info(
            "Закодированная последовательность после алгоритма Витерби: %s",
            encoded_data,
        )

        if command.add_errors:
            result: list[str] = []
            bits_per_pixel: int = 24

            for i in range(0, len(encoded_data), bits_per_pixel):
                pixel_bits: list[str] = list(encoded_data[i : i + bits_per_pixel])

                logger.info("Старый набор битов: %s", pixel_bits)
                # Инвертируем случайный бит в пикселе
                error_pos: int = 3
                pixel_bits[error_pos] = "1" if pixel_bits[error_pos] == "0" else "0"
                logger.info(
                    "Новый набор битов, где инвертировали на позиции 3: %s", pixel_bits
                )

                result.append("".join(pixel_bits))

            return "".join(result)

        return encoded_data


class DecodeCascadeCodeUseCase(BaseUseCase[DecodeCascadeCodeCommand]):
    def __init__(
        self,
        block_code: BlockCodesService,
        interleave_service: InterleaveService,
        convolutional_service: ConvolutionalCodesService,
    ) -> None:
        self._block_code_service: BlockCodesService = block_code
        self._interleave_service: InterleaveService = interleave_service
        self._convolutional_service: ConvolutionalCodesService = convolutional_service

    async def __call__(
        self, command: DecodeCascadeCodeCommand
    ) -> np.ndarray[list[str, str, str]]:
        count_of_register: int = max(max(sublist) for sublist in command.indexes) + 1

        logger.info("Количество регистров: %s", count_of_register)

        non_filtered_pols = (
            "".join(comb) for comb in product(SEQUENCE, repeat=count_of_register)
        )
        filtered_pols = filter(lambda pol: pol.count("1") > 2, non_filtered_pols)
        pols: str = ",".join(filtered_pols)

        binary_word = self._convolutional_service.decode(
            data=command.data,
            pols=pols,
        )

        logger.info("Декодированное после алгоритма Витерби: %s", binary_word)

        count_of_columns: int = len(command.matrix_for_block_code[0])

        split_indices = np.linspace(
            0, len(binary_word), count_of_columns + 1, dtype=int
        )

        chunked_array = cast(
            np.ndarray[np.ndarray[str]],
            np.array(
                [
                    list(binary_word[start:end])
                    for start, end in zip(split_indices[:-1], split_indices[1:])
                ]
            ),
        )

        logger.info("Разбили после Витерби на равные части: %s", chunked_array)

        transposed_matrix = self._interleave_service.execute(chunked_array)

        logger.info("Транспонированная матрица: %s", transposed_matrix)

        result = self._block_code_service.decode(
            encoded_with_errors="".join("".join(x) for x in transposed_matrix),
            matrix=command.matrix_for_block_code,
            type_matrix=command.type_of_matrix,
        )

        logger.info("Декодированная после блочного кода: %s", result)

        return result


class ShowNoisyImageUseCase(BaseUseCase[ShowNoisyImageCommand]):
    async def __call__(
        self, command: ShowNoisyImageCommand
    ) -> np.ndarray[np.ndarray[[str]]]:
        data = command.data
        error_pos = 3

        # Инвертируем бит в каждом канале каждого пикселя
        for y in range(data.shape[0]):
            for x in range(data.shape[1]):
                data[y, x] = self.invert_bit(data[y, x], error_pos)

        return data

    @staticmethod
    def invert_bit(binary_str: str, pos: int) -> str:
        """Инвертирует бит в позиции `pos` (считая с 0)"""
        if pos < 0 or pos >= 8:
            raise ValueError("Позиция должна быть между 0 и 7")
        return (
            binary_str[:pos]
            + ("1" if binary_str[pos] == "0" else "0")
            + binary_str[pos + 1 :]
        )
