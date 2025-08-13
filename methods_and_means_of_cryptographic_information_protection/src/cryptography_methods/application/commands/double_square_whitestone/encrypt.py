from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.views.double_square_whitestone import DoubleSquareWhitestoneEncryptView
from cryptography_methods.domain.cipher_table.entities.table import Table
from cryptography_methods.domain.cipher_table.services.cipher_table_service import CipherTableService
from cryptography_methods.domain.common.values.text import Text
from cryptography_methods.domain.double_square_whitestone.entities.double_table import DoubleTableWhitestone
from cryptography_methods.domain.double_square_whitestone.services.double_square_whitestone_service import (
    DoubleSquareWhitestoneService
)

DEFAULT_FIRST_TABLE_DATA: Final[list[str]] = [
    'Ж', 'Щ', 'Н', 'Ю', 'Р', 'И', 'Т', 'Ь', 'Ц', 'Б', 'Я', 'М', 'Е',
    '.', 'С', 'В', 'Ы', 'П', 'Х', ' ', ':', 'Д', 'У', 'О', 'К', 'З',
    'Э', 'Ф', 'Г', 'Ш', 'Ч', "А", ",", "Л", "Ъ"
]

DEFAULT_SECOND_TABLE_DATA: Final[list[str]] = [
    'И', 'Ч', 'Г', 'Я', 'Т', ',', 'Ж', 'Ь', 'М', 'О', 'З', 'Ю', 'Р',
    'В', 'Щ', 'Ц', ':', 'П', 'Е', 'Л', 'Ъ', 'А', 'Н', '.', 'Х', 'Э',
    'К', 'С', 'Ш', 'Д', 'Б', "Ф", "У", "Ы", " "
]


@dataclass(frozen=True, slots=True, kw_only=True)
class EncryptDoubleSquareWhitestoneCommand:
    text: str
    key_for_encryption: tuple[list[str], list[str]] | None = None


@final
class EncryptDoubleSquareWhitestoneCommandHandler:
    def __init__(
            self,
            double_square_whitestone_service: DoubleSquareWhitestoneService,
            cipher_table_service: CipherTableService,
    ) -> None:
        self._double_whitestone_service: Final[DoubleSquareWhitestoneService] = double_square_whitestone_service
        self._cipher_table_service: Final[CipherTableService] = cipher_table_service

    async def __call__(self, data: EncryptDoubleSquareWhitestoneCommand) -> DoubleSquareWhitestoneEncryptView:
        key_for_encryption: tuple[list[str], list[str]]

        if data.key_for_encryption is None:
            key_for_encryption = (DEFAULT_FIRST_TABLE_DATA, DEFAULT_SECOND_TABLE_DATA)
        else:
            key_for_encryption = data.key_for_encryption

        text_for_encryption: Text = Text(data.text)


        left_table: Table = self._cipher_table_service.create(
            width=len(key_for_encryption[0][0]),
            height=len(key_for_encryption[0]),
            data="".join(str(x) for x in key_for_encryption[0])
        )

        right_table: Table = self._cipher_table_service.create(
            width=len(key_for_encryption[1][0]),
            height=len(key_for_encryption[1]),
            data="".join(str(x) for x in key_for_encryption[1])
        )

        double_table_whitestone: DoubleTableWhitestone = self._double_whitestone_service.create_with_tables(
            left_table=left_table,
            right_table=right_table,
        )

        encrypted_text: Text = self._double_whitestone_service.encrypt(
            text=text_for_encryption,
            key_for_encryption=double_table_whitestone
        )

        return DoubleSquareWhitestoneEncryptView(
            text=data.text,
            encrypted_text=encrypted_text.value,
            key_for_encryption=key_for_encryption,
        )
