from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.views.ceaser_keyword import CeaserKeywordDecryptionView
from cryptography_methods.domain.ceaser.services.ceaser_keyword_service import CeaserKeywordService
from cryptography_methods.domain.ceaser.values.key_ceaser_keyword import KeyCeaserKeyword
from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.common.values.text import Text


@dataclass(frozen=True, slots=True)
class CeaserKeywordDecryptCommand:
    k: int
    keyword: str
    text: str


@final
class CeaserKeywordDecryptCommandHandler:
    def __init__(
            self,
            alphabet_service: AlphabetService,
            ceaser_keyword_service: CeaserKeywordService
    ) -> None:
        self._alphabet_service: Final[AlphabetService] = alphabet_service
        self._ceaser_keyword_service: Final[CeaserKeywordService] = ceaser_keyword_service

    async def __call__(self, data: CeaserKeywordDecryptCommand) -> CeaserKeywordDecryptionView:
        text_for_decryption: Text = Text(data.text)

        alphabet: str = self._alphabet_service.build_alphabet_by_provided_text(
            text=text_for_decryption
        )

        m: int = len(alphabet)

        key_for_decryption: KeyCeaserKeyword = KeyCeaserKeyword(
            k=data.k,
            keyword=data.keyword,
            m=m,
        )

        decrypted_text: Text = self._ceaser_keyword_service.decrypt(
            key=key_for_decryption,
            text=text_for_decryption
        )

        return CeaserKeywordDecryptionView(
            original_text=data.text,
            keyword=data.keyword,
            k=data.k,
            m=m,
            decrypted_text=decrypted_text.value,
        )
