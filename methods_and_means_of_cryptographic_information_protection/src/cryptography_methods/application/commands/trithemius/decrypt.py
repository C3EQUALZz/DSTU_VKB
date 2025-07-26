from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.views.trithemius import TrithemiusDecryptView
from cryptography_methods.domain.ceaser.services.trithemius_service import TrithemiusService
from cryptography_methods.domain.cipher_table.values.table_dimension import TableDimension
from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.common.values.text import Text


@dataclass(frozen=True, slots=True)
class TrithemiusDecryptCommand:
    text: str
    key: str
    columns: int
    rows: int


@final
class TrithemiusDecryptCommandHandler:
    def __init__(
            self,
            trithemius_service: TrithemiusService,
            alphabet_service: AlphabetService,
    ) -> None:
        self._trithemius_service: Final[TrithemiusService] = trithemius_service
        self._alphabet_service: Final[AlphabetService] = alphabet_service

    async def __call__(self, data: TrithemiusDecryptCommand) -> TrithemiusDecryptView:
        table_width: TableDimension = TableDimension(data.columns)
        table_height: TableDimension = TableDimension(data.rows)
        keyword: Text = Text(data.key)
        text_for_decryption: Text = Text(data.text)

        length_of_alphabet: int = len(self._alphabet_service.build_alphabet_by_provided_text(
            text=text_for_decryption
        ))

        decrypted_text: Text = self._trithemius_service.decrypt(
            table_width=table_width,
            table_height=table_height,
            keyword=keyword,
            text_for_decryption=text_for_decryption,
        )

        return TrithemiusDecryptView(
            original_text=data.text,
            decrypted_text=decrypted_text.value,
            key=data.key,
            width=data.columns,
            height=data.rows,
            length_of_alphabet=length_of_alphabet,
        )
