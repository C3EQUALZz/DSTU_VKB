import logging
from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.views.single_key_permutation import SingleKeyPermutationEncryptView
from cryptography_methods.domain.cipher_table.services.single_key_permutation_service import SingleKeyPermutationService
from cryptography_methods.domain.cipher_table.values.table_dimension import TableDimension
from cryptography_methods.domain.common.values.text import Text

logger: Final[logging.Logger] = logging.getLogger(__name__)


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
        logger.info("Started single key permutation encryption....")

        mapped_data: str = data.data.replace("  ", "|").replace(" ", "_")
        logger.info("Replaced all spaces on symbols in text for encryption, changed data: %s", mapped_data)
        mapped_key: str = data.key.replace("  ", "|").replace(" ", "_")
        logger.info("Replace all spaces on symbols in key for encryption, changed data: %s", mapped_key)

        validated_data: Text = Text(mapped_data)
        logger.info("Validated data: %s", validated_data)
        validated_key: Text = Text(mapped_key)
        logger.info("Validated key: %s", validated_key)
        table_width: TableDimension = TableDimension(data.width)
        logger.info("Validated table width: %s", table_width)
        table_height: TableDimension = TableDimension(data.height)
        logger.info("Validated table height: %s", table_height)

        encrypted_string: Text = self._single_key_permutation_service.encrypt(
            data=validated_data,
            width=table_width,
            height=table_height,
            key=validated_key,
        )
        logger.info("Finished encryption, returning string: %s", encrypted_string)

        return SingleKeyPermutationEncryptView(
            original_text=data.data,
            encrypted_text=encrypted_string.value,
            width=data.width,
            height=data.height,
            key=data.key,
        )
