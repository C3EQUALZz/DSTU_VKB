import logging
from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.views.gost_28147 import Gost28147DecryptionView
from cryptography_methods.domain.gost_28147.services.gost_28147_service import Gost28147Service

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class Gost28147DecryptCommand:
    text: str
    key: str


@final
class Gost28147DecryptCommandHandler:
    def __init__(self, gost_28147_service: Gost28147Service) -> None:
        self._gost_28147_service: Final[Gost28147Service] = gost_28147_service

    async def __call__(self, data: Gost28147DecryptCommand) -> Gost28147DecryptionView:
        logger.info("Started decryption using GOST 28147-89. Text length: %d", len(data.text))

        # Преобразуем ключ в байты (UTF-8 кодировка)
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

        # Преобразуем зашифрованный текст из hex-строки в байты
        try:
            # Убираем пробелы и другие разделители из hex-строки
            hex_text = data.text.replace(' ', '').replace('-', '').replace(':', '')
            text_bytes = bytes.fromhex(hex_text)
        except ValueError as e:
            raise ValueError(f"Encrypted text must be a valid hex string: {e}") from e

        logger.info("Key bytes length: %d, Text bytes length: %d", len(key_bytes), len(text_bytes))

        # Дешифруем данные
        decrypted_bytes = self._gost_28147_service.decrypt(text_bytes, key_bytes)

        # Удаляем дополняющие пробелы в конце (если они были добавлены при шифровании)
        # При шифровании текст дополняется пробелами до кратного 8 байтам
        decrypted_bytes = decrypted_bytes.rstrip(b' ')

        # Преобразуем расшифрованные данные обратно в строку UTF-8
        decrypted_text = decrypted_bytes.decode('utf-8', errors='replace')

        logger.info("Decryption completed successfully")

        return Gost28147DecryptionView(
            original_text=data.text,
            decrypted_text=decrypted_text,
            key=data.key,
        )

