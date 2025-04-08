from itertools import product
from typing import cast

import numpy as np

from app.infrastructure.services.block_codes import BlockCodesService
from app.infrastructure.services.convolutional_codes import ConvolutionalCodesService
from app.infrastructure.services.interleaver import InterleaveService
from app.logic.commands.block_codes import EncodeCascadeCodeCommand, DecodeCascadeCodeCommand
from app.logic.use_cases.base import BaseUseCase
from app.logic.use_cases.convolutional_codes import SEQUENCE


class EncodeCascadeCodeUseCase(BaseUseCase[EncodeCascadeCodeCommand]):
    def __init__(
            self,
            block_code: BlockCodesService,
            interleave_service: InterleaveService,
            convolutional_service: ConvolutionalCodesService
    ) -> None:
        self._block_code_service: BlockCodesService = block_code
        self._interleave_service: InterleaveService = interleave_service
        self._convolutional_service: ConvolutionalCodesService = convolutional_service

    async def __call__(self, command: EncodeCascadeCodeCommand):
        block_encoded: np.ndarray[np.ndarray[str]] = self._block_code_service.encode(
            data=command.data,
            matrix=command.matrix_for_block_code,
            type_matrix=command.type_of_matrix
        )

        interleaved_matrix: np.ndarray[np.ndarray[str]] = self._interleave_service.execute(
            block_encoded
        )

        data: str = "".join("".join(x) for x in interleaved_matrix)

        count_of_register: int = max(max(sublist) for sublist in command.indexes) + 1

        non_filtered_pols = ("".join(comb) for comb in product(SEQUENCE, repeat=count_of_register))
        filtered_pols: filter = filter(lambda pol: pol.count("1") > 2, non_filtered_pols)
        pols: str = ','.join(filtered_pols)

        return self._convolutional_service.encode(
            data=data,
            pols=pols,
        )


class DecodeCascadeCodeUseCase(BaseUseCase[DecodeCascadeCodeCommand]):
    def __init__(
            self,
            block_code: BlockCodesService,
            interleave_service: InterleaveService,
            convolutional_service: ConvolutionalCodesService
    ) -> None:
        self._block_code_service: BlockCodesService = block_code
        self._interleave_service: InterleaveService = interleave_service
        self._convolutional_service: ConvolutionalCodesService = convolutional_service

    async def __call__(self, command: DecodeCascadeCodeCommand):
        count_of_register: int = max(max(sublist) for sublist in command.indexes) + 1

        non_filtered_pols = ("".join(comb) for comb in product(SEQUENCE, repeat=count_of_register))
        filtered_pols = filter(lambda pol: pol.count("1") > 2, non_filtered_pols)
        pols: str = ','.join(filtered_pols)

        binary_word = self._convolutional_service.decode(
            data=command.data,
            pols=pols,
        )

        count_of_rows = len(command.matrix_for_block_code[0])

        split_indices = np.linspace(0, len(binary_word), count_of_rows + 1, dtype=int)

        chunked_array = cast(np.ndarray[np.ndarray[str]], np.array([
            list(binary_word[start:end]) for start, end in zip(split_indices[:-1], split_indices[1:])
        ]))

        transposed_matrix = self._interleave_service.execute(
            chunked_array
        )

        return self._block_code_service.decode(
            encoded_with_errors="".join("".join(x) for x in transposed_matrix),
            matrix=command.matrix_for_block_code,
            type_matrix=command.type_of_matrix
        )
