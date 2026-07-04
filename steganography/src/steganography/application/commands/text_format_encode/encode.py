"""EncodeSecretCommand + CommandHandler: встраивание сообщения в контейнер."""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from steganography.application.common.views.text_format_encode import (
    EncodeSecretView,
)
from steganography.domain.common.encodings.encoding_registry import (
    EncodingRegistry,
)
from steganography.domain.common.value_objects.formatting_method import (
    FormattingMethod,
)
from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
)
from steganography.domain.text_format_encode.errors.encode_errors import (
    EncodeError,
)
from steganography.domain.text_format_encode.ports.container_writer import (
    ContainerWriter,
)
from steganography.domain.text_format_encode.services.container_plan_builder import (
    ContainerPlanBuilder,
)
from steganography.domain.text_format_encode.value_objects.cover_text import (
    CoverText,
)
from steganography.domain.text_format_encode.value_objects.secret_payload import (
    SecretPayload,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class EncodeSecretCommand:
    """Встроить секретный текст в контейнер и сохранить новый docx."""

    secret_text: str
    cover: CoverText
    encoding_name: str
    param: FormattingParam
    zero_value: str
    one_value: str
    output_path: Path


@final
class EncodeSecretCommandHandler:
    """Координирует выбор кодировки, построение плана и запись контейнера."""

    def __init__(
        self,
        registry: EncodingRegistry,
        plan_builder: ContainerPlanBuilder,
        writer: ContainerWriter,
    ) -> None:
        self._registry: Final[EncodingRegistry] = registry
        self._plan_builder: Final[ContainerPlanBuilder] = plan_builder
        self._writer: Final[ContainerWriter] = writer

    async def __call__(self, data: EncodeSecretCommand) -> EncodeSecretView:
        logger.info(
            "Энкод docx: встраивание в %s (кодировка %s, параметр %s)",
            data.output_path, data.encoding_name, data.param.value,
        )
        encoding = self._registry.by_name(data.encoding_name)
        if encoding is None:
            return self._failure(data, "неизвестная кодировка")

        method = FormattingMethod(
            param=data.param,
            zero_value=data.zero_value,
            one_value=data.one_value,
        )
        payload = SecretPayload(
            secret_text=data.secret_text,
            encoding=encoding,
            method=method,
        )

        try:
            plan = self._plan_builder.build(payload, data.cover)
        except EncodeError as error:
            logger.warning("Энкод docx: ошибка встраивания — %s", error)
            return self._failure(data, str(error), method=method)

        self._writer.write(plan, data.output_path)
        logger.info(
            "Энкод docx: записано %d символов, полезных бит %d",
            len(plan.chars), plan.payload_bits,
        )
        return EncodeSecretView(
            output_path=data.output_path,
            success=True,
            secret_text=data.secret_text,
            encoding_name=data.encoding_name,
            method=method,
            payload_bits=plan.payload_bits,
            container_chars=len(plan.chars),
        )

    def _failure(
        self,
        data: EncodeSecretCommand,
        error: str,
        method: FormattingMethod | None = None,
    ) -> EncodeSecretView:
        return EncodeSecretView(
            output_path=data.output_path,
            success=False,
            secret_text=data.secret_text,
            encoding_name=data.encoding_name,
            method=method,
            payload_bits=0,
            container_chars=len(data.cover.text),
            error=error,
        )
