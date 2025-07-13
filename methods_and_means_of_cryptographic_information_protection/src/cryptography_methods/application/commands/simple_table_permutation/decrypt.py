from dataclasses import dataclass
from typing import Final, final

from cryptography_methods.application.common.ports.simple_table_permutation.view_models import (
    SimpleTablePermutationDecryptView
)
from cryptography_methods.domain.cipher_table.services.simple_table_permutation_service import (
    SimpleTablePermutationService
)


@dataclass(frozen=True, slots=True)
class SimpleTablePermutationDecryptCommand:
    width: int
    height: int
    data: str


@final
class SimpleTablePermutationDecryptCommandHandler:
    def __init__(
            self,
            simple_table_permutation_service: SimpleTablePermutationService
    ) -> None:
        self._simple_table_permutation_service: Final[SimpleTablePermutationService] = simple_table_permutation_service

    async def __call__(self, data: SimpleTablePermutationDecryptCommand) -> SimpleTablePermutationDecryptView:
        decrypted_text: str = self._simple_table_permutation_service.decrypt(
            data=data.data,
            width=data.width,
            height=data.height,
        )

        return SimpleTablePermutationDecryptView(
            original_text=data.data,
            decrypted_text=decrypted_text,
            width=data.width,
            height=data.height,
        )
