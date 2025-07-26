from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.views.playfair import PlayfairEncryptView
from cryptography_methods.domain.cipher_table.values.table_dimension import TableDimension
from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.common.values.text import Text
from cryptography_methods.domain.playfair.services.playfair_service import PlayfairService


@dataclass(frozen=True, slots=True)
class PlayfairEncryptCommand:
    text: str
    key: str
    columns: int
    rows: int


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
        table_width: TableDimension = TableDimension(data.columns)
        table_height: TableDimension = TableDimension(data.rows)
        key_for_encryption: Text = Text(data.key)
        text_for_encryption: Text = Text(data.text)

        length_of_alphabet: int = len(self._alphabet_service.build_alphabet_by_provided_text(
            text=text_for_encryption
        ))

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
            width=data.columns,
            height=data.rows,
            length_of_alphabet=length_of_alphabet
        )
