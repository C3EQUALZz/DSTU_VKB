"""Массовая генерация 25 docx-вариантов через ПР2 «Энкод docx».

Для каждого варианта берётся пословица, метод форматирования и кодировка из
эталонной таблицы (декодированные значения оригинальных variantXX.docx
преподавателя), а cover-контейнер — циклически из ``covers/*.docx``.

Результаты сохраняются в ``resources/steganographic_concealment/generated/``.
Скрипт удобно прогонять как ``python -m scripts.text_format_encode.generate_variants``
или ``./.venv/bin/python scripts/text_format_encode/generate_variants.py``.
"""

import asyncio
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from steganography.application.commands.text_format_encode.encode import (
    EncodeSecretCommand,
    EncodeSecretCommandHandler,
)
from steganography.application.common.views.text_format_encode import (
    EncodeSecretView,
)
from steganography.domain.common.encodings.encoding_registry import (
    EncodingRegistry,
)
from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
)
from steganography.domain.text_format_encode.services.container_plan_builder import (
    ContainerPlanBuilder,
)
from steganography.domain.text_format_encode.services.hiding_value_defaults import (
    HidingValueDefaults,
)
from steganography.infrastructure.text_format_encode.docx_container_writer import (
    DocxContainerWriterImpl,
)
from steganography.infrastructure.text_format_encode.docx_cover_text_reader import (
    DocxCoverTextReaderImpl,
)


@dataclass(frozen=True, slots=True)
class VariantSpec:
    number: int
    secret: str
    param: FormattingParam
    encoding_name: str


_VARIANTS: Final[tuple[VariantSpec, ...]] = (
    VariantSpec(1, "Завтра подует завтрашний ветер.",
                FormattingParam.COLOR, "КОИ-8R"),
    VariantSpec(2, "Пусть не хвалят, лишь бы не ругали.",
                FormattingParam.SPACING, "Windows-1251"),
    VariantSpec(3, "Терпение и труд всё перетрут.",
                FormattingParam.SIZE, "Windows-1251"),
    VariantSpec(4, "В споре побеждает тот, кто громче кричит.",
                FormattingParam.SPACING, "cp866"),
    VariantSpec(5, "У других цветы красней.",
                FormattingParam.SCALE, "Windows-1251"),
    VariantSpec(6, "Все, что цветет, неизбежно увянет.",
                FormattingParam.COLOR, "cp866"),
    VariantSpec(7, "Где права сила, там бессильно право.",
                FormattingParam.SCALE, "cp866"),
    VariantSpec(8, "Прямой человек, что прямой бамбук, встречается редко.",
                FormattingParam.COLOR, "Windows-1251"),
    VariantSpec(9, "Женщина захочет - сквозь скалу пройдет.",
                FormattingParam.SIZE, "КОИ-8R"),
    VariantSpec(10, "Баклажан на стебле дыни не вырастет.",
                FormattingParam.SIZE, "cp866"),
    VariantSpec(11, "И мотылек живет целую жизнь.",
                FormattingParam.SCALE, "КОИ-8R"),
    VariantSpec(12, "Пятьдесят сегодня лучше, чем сто завтра.",
                FormattingParam.SIZE, "Windows-1251"),
    VariantSpec(13, "Крупная рыба в болоте не водится.",
                FormattingParam.SIZE, "КОИ-8R"),
    VariantSpec(14, "Нет врага опаснее дурака.",
                FormattingParam.COLOR, "КОИ-8R"),
    VariantSpec(15, "Ветер дует, но горы не двигаются.",
                FormattingParam.SIZE, "cp866"),
    VariantSpec(16, "Об обычаях не спорят.",
                FormattingParam.SPACING, "КОИ-8R"),
    VariantSpec(17, "Один бог забыл - другой поможет.",
                FormattingParam.SIZE, "Windows-1251"),
    VariantSpec(18, "Дела говорят громче слов.",
                FormattingParam.SPACING, "cp866"),
    VariantSpec(19, "Пустая бочка громче гремит.",
                FormattingParam.SCALE, "Windows-1251"),
    VariantSpec(20, "Бесполезнее, чем писать цифры на текущей воде.",
                FormattingParam.COLOR, "cp866"),
    VariantSpec(21, "Конец болтовни - начало дела.",
                FormattingParam.SPACING, "КОИ-8R"),
    VariantSpec(22, "Таланты не наследуют.",
                FormattingParam.COLOR, "Windows-1251"),
    VariantSpec(23, "Никто не спотыкается, лежа в постели.",
                FormattingParam.SCALE, "КОИ-8R"),
    VariantSpec(24, "Уступай дорогу дуракам и сумасшедшим.",
                FormattingParam.SPACING, "Windows-1251"),
    VariantSpec(25, "Ячмень у соседа вкуснее риса дома.",
                FormattingParam.COLOR, "Windows-1251"),
)

_PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parents[2]
_COVERS_DIR: Final[Path] = (
    _PROJECT_ROOT / "resources" / "steganographic_concealment" / "covers"
)
_OUTPUT_DIR: Final[Path] = (
    _PROJECT_ROOT / "resources" / "steganographic_concealment" / "generated"
)


def _build_handler() -> EncodeSecretCommandHandler:
    return EncodeSecretCommandHandler(
        registry=EncodingRegistry(),
        plan_builder=ContainerPlanBuilder(),
        writer=DocxContainerWriterImpl(),
    )


def _cover_path_for(number: int) -> Path:
    # ротация по 10 covers/N.docx (1..10) — обеспечивает разнообразие стихов
    index = ((number - 1) % 10) + 1
    return _COVERS_DIR / f"{index}.docx"


def _commands() -> Iterable[EncodeSecretCommand]:
    cover_reader = DocxCoverTextReaderImpl()
    defaults = HidingValueDefaults()
    for variant in _VARIANTS:
        cover_text = cover_reader.read(_cover_path_for(variant.number))
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
        print(
            f"  {view.output_path.name}: {status}"
            f" ({view.encoding_name}, "
            f"{view.method.param.human_name if view.method else '—'}, "
            f"{view.payload_bits} бит / "
            f"{view.container_chars} симв)",
        )


if __name__ == "__main__":
    main()
