"""Массовая генерация 25 docx-вариантов через ПР2 «Энкод docx»."""

import asyncio
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Final

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT / "scripts"))

from variants_data import VARIANTS  # noqa: E402

from steganography.application.commands.text_format_encode.encode import (  # noqa: E402
    EncodeSecretCommand,
    EncodeSecretCommandHandler,
)
from steganography.application.common.views.text_format_encode import (  # noqa: E402
    EncodeSecretView,
)
from steganography.domain.common.encodings.encoding_registry import (  # noqa: E402
    EncodingRegistry,
)
from steganography.domain.text_format_encode.services.container_plan_builder import (  # noqa: E402
    ContainerPlanBuilder,
)
from steganography.domain.text_format_encode.services.hiding_value_defaults import (  # noqa: E402
    HidingValueDefaults,
)
from steganography.infrastructure.text_format_encode.docx_container_writer import (  # noqa: E402
    DocxContainerWriterImpl,
)
from steganography.infrastructure.text_format_encode.docx_cover_text_reader import (  # noqa: E402
    DocxCoverTextReaderImpl,
)

_COVERS_DIR: Final[Path] = (
    _ROOT / "resources" / "steganographic_concealment" / "covers"
)
_OUTPUT_DIR: Final[Path] = (
    _ROOT / "resources" / "steganographic_concealment" / "generated"
)


def _build_handler() -> EncodeSecretCommandHandler:
    return EncodeSecretCommandHandler(
        registry=EncodingRegistry(),
        plan_builder=ContainerPlanBuilder(),
        writer=DocxContainerWriterImpl(),
    )


def _commands() -> Iterable[EncodeSecretCommand]:
    cover_reader = DocxCoverTextReaderImpl()
    defaults = HidingValueDefaults()
    for variant in VARIANTS:
        cover_text = cover_reader.read(
            _COVERS_DIR / f"{variant.cover_index}.docx",
        )
        zero_value, one_value = defaults.for_param(variant.param)
        yield EncodeSecretCommand(
            secret_text=variant.secret,
            cover_text=cover_text,
            encoding_name=variant.encoding_name,
            param=variant.param,
            zero_value=zero_value,
            one_value=one_value,
            output_path=_OUTPUT_DIR / f"variant{variant.number:02d}.docx",
        )


async def _run() -> list[EncodeSecretView]:
    _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    handler = _build_handler()
    views: list[EncodeSecretView] = []
    for command in _commands():
        view = await handler(command)
        views.append(view)
    return views


def main() -> None:
    views = asyncio.run(_run())
    successes = sum(1 for v in views if v.success)
    print(f"\nГенерация завершена: {successes}/{len(views)} успешно")
    for view in views:
        status = "OK" if view.success else f"FAIL: {view.error}"
        param = view.method.param.human_name if view.method else "—"
        print(
            f"  {view.output_path.name}: {status} "
            f"({view.encoding_name}, {param}, "
            f"{view.payload_bits} бит / {view.container_chars} симв)",
        )


if __name__ == "__main__":
    main()
