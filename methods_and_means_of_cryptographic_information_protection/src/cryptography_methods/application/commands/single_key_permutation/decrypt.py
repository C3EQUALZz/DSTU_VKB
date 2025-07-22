from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.domain.cipher_table.services.single_key_permutation_service import (
    SingleKeyPermutationService
)
from cryptography_methods.application.common.views.single_key_permutation import SingleKeyPermutationDecryptView


@dataclass(frozen=True, slots=True)
class SingleKeyPermutationDecryptCommand:
    width: int
    height: int
    data: str
    key: str


@final
class SingleKeyPermutationDecryptCommandHandler:
    def __init__(
            self,
            single_key_permutation_service: SingleKeyPermutationService,
    ) -> None:
        self._single_key_permutation_service: Final[SingleKeyPermutationService] = single_key_permutation_service

    async def __call__(self, data: SingleKeyPermutationDecryptCommand) -> SingleKeyPermutationDecryptView:
        decrypted_text: str = self._single_key_permutation_service.decrypt(
            data=data.data,
            key=data.key,
            width=data.width,
            height=data.height,
        )

        return SingleKeyPermutationDecryptView(
            original_text=data.data,
            decrypted_text=decrypted_text,
            key=data.key,
            width=data.width,
            height=data.height,
        )
