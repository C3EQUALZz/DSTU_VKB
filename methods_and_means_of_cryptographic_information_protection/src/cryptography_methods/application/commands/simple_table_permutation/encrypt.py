from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.ports.simple_table_permutation.view_models import \
    SimpleTablePermutationEncryptView
from cryptography_methods.domain.cipher_table.services.simple_table_permutation_service import \
    SimpleTablePermutationService


@dataclass(frozen=True, slots=True)
class SimpleTablePermutationEncryptCommand:
    width: int
    height: int
    data: str


@final
class SimpleTablePermutationEncryptCommandHandler:
    def __init__(
            self,
            simple_table_permutation_service: SimpleTablePermutationService
    ) -> None:
        self._simple_table_permutation_service: Final[SimpleTablePermutationService] = simple_table_permutation_service

    async def __call__(self, data: SimpleTablePermutationEncryptCommand) -> SimpleTablePermutationEncryptView:
        encrypted_text: str = self._simple_table_permutation_service.encrypt(
            data=data.data,
            width=data.width,
            height=data.height,
        )

        return SimpleTablePermutationEncryptView(
            encrypted_text=encrypted_text,
            original_text=data.data,
            width=data.width,
            height=data.height,
        )
