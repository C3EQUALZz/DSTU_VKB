import logging
from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.views.playfair import PlayfairEncryptView
from cryptography_methods.domain.cipher_table.values.table_dimension import TableDimension
from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.common.values.text import Text
from cryptography_methods.domain.playfair.services.playfair_service import PlayfairService

logger: Final[logging.Logger] = logging.getLogger(__name__)

@dataclass(frozen=True, slots=True)
class PlayfairEncryptCommand:
    text: str
    key: str


@final
class PlayfairEncryptCommandHandler:
    def __init__(
            self,
            alphabet_service: AlphabetService,
            playfair_service: PlayfairService
    ) -> None:
        self._alphabet_service: Final[AlphabetService] = alphabet_service
        self._playfair_service: Final[PlayfairService] = playfair_service

    async def __call__(self, data: PlayfairEncryptCommand) -> PlayfairEncryptView:
        logger.info("Started playfair encryption")
        key_for_encryption: Text = Text(data.key)
        logger.info("Validated key for encryption")
        text_for_encryption: Text = Text(data.text)
        logger.info("Validated text for encryption")
        table_width: TableDimension
        table_height: TableDimension

        length_of_alphabet: int = len(self._alphabet_service.build_alphabet_by_provided_text(
            text=text_for_encryption
        ))
        logger.info("Current length of alphabet - %s", length_of_alphabet)

        if length_of_alphabet == 33:
            table_width: TableDimension = TableDimension(8)
            table_height: TableDimension = TableDimension(4)
        elif length_of_alphabet == 26:
            table_width: TableDimension = TableDimension(5)
            table_height: TableDimension = TableDimension(5)
        else:
            raise NotImplementedError("Not implemented for this language")

        logger.info("table width - %s, table height - %s", table_width, table_height)

        encrypted_text: Text = self._playfair_service.encrypt(
            table_width=table_width,
            table_height=table_height,
            keyword=key_for_encryption,
            text_for_encryption=text_for_encryption,
        )

        return PlayfairEncryptView(
            original_text=data.text,
            encrypted_text=encrypted_text.value,
            key=data.key,
            width=table_width.value,
            height=table_height.value,
            length_of_alphabet=length_of_alphabet
        )
