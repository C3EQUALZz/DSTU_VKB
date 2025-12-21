"""Command for GOST 3410-94 signature verification."""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from cryptography_methods.application.common.views.gost_3410_94 import Gost341094VerifyView
from cryptography_methods.domain.gost_3410_94 import Gost341094Service

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class Gost341094VerifyCommand:
    """Command for GOST 3410-94 signature verification."""

    document: Path
    signature_file: Path
    parameters_file: Path
    public_key_file: Path


@final
class Gost341094VerifyCommandHandler:
    """Handler for GOST 3410-94 signature verification command."""

    def __init__(self, gost_service: Gost341094Service) -> None:
        """Initialize handler.

        Args:
            gost_service: GOST 3410-94 domain service
        """
        self._service: Final[Gost341094Service] = gost_service

    async def __call__(self, data: Gost341094VerifyCommand) -> Gost341094VerifyView:
        """Execute GOST 3410-94 signature verification command.

        Args:
            data: Verification command data

        Returns:
            Verification view with results
        """
        logger.info(
            "Starting GOST 3410-94 signature verification. document=%s, signature_file=%s, parameters_file=%s, public_key_file=%s",
            data.document,
            data.signature_file,
            data.parameters_file,
            data.public_key_file,
        )

        # Загрузка параметров, ключа и подписи
        logger.info("Загрузка параметров, открытого ключа и подписи...")
        parameters = self._service.load_parameters(data.parameters_file)
        public_key = self._service.load_public_key(data.public_key_file)
        q_from_file, signature = self._service.load_signature(data.signature_file)

        logger.info("Прочитанные значения:")
        logger.info("  q: %s", q_from_file)
        logger.info("  r: %s", signature.r)
        logger.info("  s: %s", signature.s)

        # Чтение документа
        logger.info("Чтение файла для проверки: %s", data.document)
        file_data = data.document.read_bytes()
        logger.info("Размер файла: %s байт", len(file_data))

        # Вычисление хеша
        hash_value = self._service.compute_hash(file_data, parameters.q)
        logger.info("Полученный хеш: %s", hash_value)

        # Проверка подписи
        logger.info("Проверка подписи...")
        is_valid = self._service.verify_signature(hash_value, signature, parameters, public_key)

        logger.info("Итоговый результат: %s", "ВАЛИДНА" if is_valid else "НЕВАЛИДНА")

        return Gost341094VerifyView(
            document_path=str(data.document),
            signature_file=str(data.signature_file),
            hash_value=str(hash_value),
            is_valid=is_valid,
        )


