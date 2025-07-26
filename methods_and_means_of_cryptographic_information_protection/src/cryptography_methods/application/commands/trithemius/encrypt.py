from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.views.trithemius import TrithemiusEncryptView
from cryptography_methods.domain.ceaser.services.trithemius_service import TrithemiusService
from cryptography_methods.domain.cipher_table.values.table_dimension import TableDimension
from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.common.values.text import Text


@dataclass(frozen=True, slots=True)
class TrithemiusEncryptCommand:
    text: str
    key: str
    columns: int
    rows: int


@final
class TrithemiusEncryptCommandHandler:
    def __init__(
            self,
            trithemius_service: TrithemiusService,
            alphabet_service: AlphabetService,
    ) -> None:
        self._trithemius_service: Final[TrithemiusService] = trithemius_service
        self._alphabet_service: Final[AlphabetService] = alphabet_service

    async def __call__(self, data: TrithemiusEncryptCommand) -> TrithemiusEncryptView:
        table_width: TableDimension = TableDimension(data.columns)
        table_height: TableDimension = TableDimension(data.rows)
        keyword: Text = Text(data.key)
        text_for_encryption: Text = Text(data.text)

        length_of_alphabet: int = len(self._alphabet_service.build_alphabet_by_provided_text(
            text=text_for_encryption
        ))

        encrypted_text: Text = self._trithemius_service.encrypt(
            table_width=table_width,
            table_height=table_height,
            keyword=keyword,
            text_for_encryption=text_for_encryption,
        )

        return TrithemiusEncryptView(
            original_text=text_for_encryption.value,
            encrypted_text=encrypted_text.value,
            key=data.key,
            width=data.columns,
            height=data.rows,
            length_of_alphabet=length_of_alphabet
        )
