from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.views.ceaser_keyword import CeaserKeywordEncryptionView
from cryptography_methods.domain.ceaser.services.ceaser_keyword_service import CeaserKeywordService
from cryptography_methods.domain.ceaser.values.key_ceaser_keyword import KeyCeaserKeyword
from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.common.values.text import Text


@dataclass(frozen=True, slots=True)
class CeaserKeywordEncryptCommand:
    k: int
    keyword: str
    text: str


@final
class CeaserKeywordEncryptCommandHandler:
    def __init__(
            self,
            alphabet_service: AlphabetService,
            ceaser_keyword_service: CeaserKeywordService
    ) -> None:
        self._alphabet_service: Final[AlphabetService] = alphabet_service
        self._ceaser_keyword_service: Final[CeaserKeywordService] = ceaser_keyword_service

    async def __call__(self, data: CeaserKeywordEncryptCommand) -> CeaserKeywordEncryptionView:
        text_for_encryption: Text = Text(data.text)

        alphabet: str = self._alphabet_service.build_alphabet_by_provided_text(
            text=text_for_encryption
        )

        m: int = len(alphabet)

        key_for_encryption: KeyCeaserKeyword = KeyCeaserKeyword(
            k=data.k,
            keyword=data.keyword,
            m=m,
        )

        encrypted_text: Text = self._ceaser_keyword_service.encrypt(
            key=key_for_encryption,
            text=text_for_encryption
        )

        return CeaserKeywordEncryptionView(
            original_text=data.text,
            encrypted_text=encrypted_text.value,
            keyword=data.keyword,
            k=data.k,
            m=m
        )


