"""Command for GOST 3410-94 document signing."""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from cryptography_methods.application.common.views.gost_3410_94 import Gost341094SignView
from cryptography_methods.domain.gost_3410_94 import Gost341094Service

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class Gost341094SignCommand:
    """Command for GOST 3410-94 document signing."""

    document: Path
    parameters_file: Path
    private_key_file: Path
    signature_file: Path
    hash_file: Path | None = None


@final
class Gost341094SignCommandHandler:
    """Handler for GOST 3410-94 document signing command."""

    def __init__(self, gost_service: Gost341094Service) -> None:
        """Initialize handler.

        Args:
            gost_service: GOST 3410-94 domain service
        """
        self._service: Final[Gost341094Service] = gost_service

    async def __call__(self, data: Gost341094SignCommand) -> Gost341094SignView:
        """Execute GOST 3410-94 document signing command.

        Args:
            data: Signing command data

        Returns:
            Signing view with results
        """
        logger.info(
            "Starting GOST 3410-94 document signing. document=%s, parameters_file=%s, private_key_file=%s, signature_file=%s",
            data.document,
            data.parameters_file,
            data.private_key_file,
            data.signature_file,
        )

        # Загрузка параметров и ключа
        logger.info("Загрузка параметров и закрытого ключа...")
        parameters = self._service.load_parameters(data.parameters_file)
        private_key = self._service.load_private_key(data.private_key_file)

        # Чтение документа
        logger.info("Чтение файла: %s", data.document)
        file_data = data.document.read_bytes()
        logger.info("Размер файла: %s байт", len(file_data))

        # Вычисление хеша
        hash_value = self._service.compute_hash(file_data, parameters.q)

        # Сохранение хеша
        hash_path = data.hash_file or Path(f"Хеш_{data.document.name}.txt")
        hash_path.write_text(str(hash_value), encoding="utf-8")
        logger.info("Хеш сохранён в файл: %s", hash_path)

        # Создание подписи
        logger.info("Создание цифровой подписи...")
        signature = self._service.create_signature(hash_value, parameters, private_key)

        # Сохранение подписи
        self._service.save_signature(signature, parameters.q, data.signature_file)
        logger.info("Подпись сохранена: %s", data.signature_file)

        return Gost341094SignView(
            document_path=str(data.document),
            hash_value=str(hash_value),
            hash_file=str(hash_path),
            signature_file=str(data.signature_file),
            r=str(signature.r),
            s=str(signature.s),
        )

