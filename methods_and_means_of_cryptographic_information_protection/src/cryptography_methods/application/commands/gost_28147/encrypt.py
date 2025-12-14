import logging
from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.views.gost_28147 import Gost28147EncryptionView
from cryptography_methods.domain.gost_28147.services.gost_28147_service import Gost28147Service

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class Gost28147EncryptCommand:
    text: str
    key: str


@final
class Gost28147EncryptCommandHandler:
    def __init__(self, gost_28147_service: Gost28147Service) -> None:
        self._gost_28147_service: Final[Gost28147Service] = gost_28147_service

    async def __call__(self, data: Gost28147EncryptCommand) -> Gost28147EncryptionView:
        logger.info("Started encryption using GOST 28147-89. Text length: %d", len(data.text))

        # Преобразуем ключ и текст в байты (UTF-8 кодировка)
        try:
            key_bytes = data.key.encode('utf-8')
            # Нормализуем ключ до 32 байт
            if len(key_bytes) < 32:
                # Дополняем пробелами до 32 байт
                key_bytes = key_bytes + b' ' * (32 - len(key_bytes))
            elif len(key_bytes) > 32:
                # Обрезаем до 32 байт
                key_bytes = key_bytes[:32]
        except UnicodeEncodeError as e:
            raise ValueError(f"Key contains characters that cannot be encoded in UTF-8: {e}") from e

        try:
            text_bytes = data.text.encode('utf-8')
        except UnicodeEncodeError as e:
            raise ValueError(f"Text contains characters that cannot be encoded in UTF-8: {e}") from e

        logger.info("Key bytes length: %d, Text bytes length: %d", len(key_bytes), len(text_bytes))

        # Шифруем данные
        encrypted_bytes = self._gost_28147_service.encrypt(text_bytes, key_bytes)

        # Преобразуем зашифрованные данные в hex-строку для безопасного представления
        encrypted_text_hex = encrypted_bytes.hex()

        logger.info("Encryption completed successfully")

        return Gost28147EncryptionView(
            original_text=data.text,
            encrypted_text_hex=encrypted_text_hex,
            key=data.key,
        )

