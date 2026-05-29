"""SecretExtractor — высокоуровневая операция «извлечь и расшифровать»."""

from typing import Final, final

from steganography.domain.common.bmp.bmp_image import BmpImage
from steganography.domain.lsb_bmp_vigenere.services.lsb_extractor import (
    LsbExtractor,
)
from steganography.domain.lsb_bmp_vigenere.services.marker_packager import (
    MarkerPackager,
)
from steganography.domain.lsb_bmp_vigenere.services.vigenere_cipher import (
    VigenereCipher,
)


@final
class SecretExtractor:
    """Извлекает байты, ищет метки и расшифровывает сообщение."""

    def __init__(
        self,
        cipher: VigenereCipher,
        packager: MarkerPackager,
        extractor: LsbExtractor,
    ) -> None:
        self._cipher: Final[VigenereCipher] = cipher
        self._packager: Final[MarkerPackager] = packager
        self._extractor: Final[LsbExtractor] = extractor

    def extract(self, image: BmpImage, key: str) -> str:
        stream = self._extractor.extract(image)
        ciphertext = self._packager.unpack(stream)
        plaintext = self._cipher.decrypt(ciphertext, key)
        return plaintext.decode("utf-8", errors="replace")
