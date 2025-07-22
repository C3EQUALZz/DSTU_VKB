from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.views.single_key_permutation import SingleKeyPermutationEncryptView
from cryptography_methods.domain.cipher_table.services.single_key_permutation_service import SingleKeyPermutationService


@dataclass(frozen=True, slots=True)
class SingleKeyPermutationEncryptCommand:
    width: int
    height: int
    data: str
    key: str


@final
class SingleKeyPermutationEncryptCommandHandler:
    def __init__(
            self,
            single_key_permutation_service: SingleKeyPermutationService,
    ) -> None:
        self._single_key_permutation_service: Final[SingleKeyPermutationService] = single_key_permutation_service

    async def __call__(self, data: SingleKeyPermutationEncryptCommand) -> SingleKeyPermutationEncryptView:
        encrypted_string: str = self._single_key_permutation_service.encrypt(
            data=data.data,
            width=data.width,
            height=data.height,
            key=data.key,
        )

        return SingleKeyPermutationEncryptView(
            original_text=data.data,
            encrypted_text=encrypted_string,
            width=data.width,
            height=data.height,
            key=data.key,
        )



