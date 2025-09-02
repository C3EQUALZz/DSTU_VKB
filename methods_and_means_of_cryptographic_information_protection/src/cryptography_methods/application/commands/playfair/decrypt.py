import logging
from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.views.playfair import PlayfairDecryptView
from cryptography_methods.domain.cipher_table.values.table_dimension import TableDimension
from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.common.values.text import Text
from cryptography_methods.domain.playfair.services.playfair_service import PlayfairService

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class PlayfairDecryptCommand:
    text: str
    key: str


@final
class PlayfairDecryptCommandHandler:
    def __init__(
            self,
            alphabet_service: AlphabetService,
            playfair_service: PlayfairService
    ) -> None:
        self._alphabet_service: Final[AlphabetService] = alphabet_service
        self._playfair_service: Final[PlayfairService] = playfair_service

    async def __call__(self, data: PlayfairDecryptCommand) -> PlayfairDecryptView:
        logger.info("Started playfair decryption")
        table_width: TableDimension
        table_height: TableDimension
        key_for_decryption: Text = Text(data.key)
        logger.info("Validate key for decryption: %s", key_for_decryption)
        text_for_decryption: Text = Text(data.text)
        logger.info("Decrypted text: %s", text_for_decryption)

        length_of_alphabet: int = len(self._alphabet_service.build_alphabet_by_provided_text(
            text=text_for_decryption
        ))
        logger.info("Get length of current alphabet: %s", length_of_alphabet)

        if length_of_alphabet == 33:
            table_width: TableDimension = TableDimension(8)
            table_height: TableDimension = TableDimension(4)
        elif length_of_alphabet == 26:
            table_width: TableDimension = TableDimension(5)
            table_height: TableDimension = TableDimension(5)
        else:
            raise NotImplementedError("Not implemented for this language")

        logger.info("table width: %s, table height: %s", table_width, table_height)

        decrypted_text: Text = self._playfair_service.decrypt(
            table_width=table_width,
            table_height=table_height,
            keyword=key_for_decryption,
            text_for_encryption=text_for_decryption,
        )

        return PlayfairDecryptView(
            original_text=data.text,
            decrypted_text=decrypted_text.value,
            key=data.key,
            width=table_width.value,
            height=table_height.value,
            length_of_alphabet=length_of_alphabet
        )
