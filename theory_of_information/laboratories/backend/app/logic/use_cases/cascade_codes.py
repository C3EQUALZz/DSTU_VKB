from app.infrastructure.services.block_codes import BlockCodesService
from app.logic.commands.block_codes import EncodeCascadeCodeCommand, DecodeCascadeCodeCommand
from app.logic.use_cases.base import BaseUseCase


class EncodeCascadeCodeUseCase(BaseUseCase[EncodeCascadeCodeCommand]):
    def __init__(self, block_code: BlockCodesService) -> None:
        self._block_code_service = block_code

    async def __call__(self, command: EncodeCascadeCodeCommand):
        return self._block_code_service.encode(
            data=command.data,
            matrix=command.matrix_for_block_code,
            type_matrix=command.type_of_matrix
        )


class DecodeCascadeCodeUseCase(BaseUseCase[DecodeCascadeCodeCommand]):
    def __init__(self, block_code: BlockCodesService) -> None:
        self._block_code_service = block_code

    async def __call__(self, command: DecodeCascadeCodeCommand):
        return self._block_code_service.decode(
            encoded_with_errors=command.data,
            matrix=command.matrix_for_block_code,
            type_matrix=command.type_of_matrix
        )
