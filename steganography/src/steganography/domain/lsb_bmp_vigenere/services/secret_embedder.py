"""SecretEmbedder — высокоуровневая операция «зашифровать и встроить»."""

from typing import Final, final

from steganography.domain.common.bmp.bmp_image import BmpImage
from steganography.domain.lsb_bmp_vigenere.services.lsb_embedder import (
    LsbEmbedder,
)
from steganography.domain.lsb_bmp_vigenere.services.marker_packager import (
    MarkerPackager,
)
from steganography.domain.lsb_bmp_vigenere.services.vigenere_cipher import (
    VigenereCipher,
)
from steganography.domain.lsb_bmp_vigenere.value_objects.secret_payload import (
    SecretPayload,
)


@final
class SecretEmbedder:
    """Шифрует сообщение Виженером, оборачивает метками, кладёт в LSB."""

    def __init__(
        self,
        cipher: VigenereCipher,
        packager: MarkerPackager,
        embedder: LsbEmbedder,
    ) -> None:
        self._cipher: Final[VigenereCipher] = cipher
        self._packager: Final[MarkerPackager] = packager
        self._embedder: Final[LsbEmbedder] = embedder

    def embed(self, image: BmpImage, payload: SecretPayload) -> BmpImage:
        plaintext = payload.plaintext.encode("utf-8")
        ciphertext = self._cipher.encrypt(plaintext, payload.key)
        framed = self._packager.pack(ciphertext)
        return self._embedder.embed(image, framed)
