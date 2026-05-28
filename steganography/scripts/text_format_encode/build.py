"""Сборка docx-отчётов по ПР2 для всех 25 вариантов.

Каждый отчёт сохраняется в docs/reports/2025/2/<вариант>/ПР2.docx и содержит
персонализированный титульный лист (Вариант №N) + реальный результат
встраивания заданной пословицы в cover-стих.
"""

import asyncio
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT / "scripts"))

from report_builder import (  # noqa: E402
    LabMeta,
    add_heading,
    add_label,
    add_listing,
    add_page_break,
    add_para,
    add_table_simple,
    add_title_page,
    make_doc,
    save,
)
from variants_data import VARIANTS, VariantSpec  # noqa: E402

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

_COVERS_DIR = _ROOT / "resources" / "steganographic_concealment" / "covers"
_GENERATED_DIR = _ROOT / "resources" / "steganographic_concealment" / "generated"
_REPORTS_ROOT = _ROOT / "docs" / "reports" / "2025" / "2"


_GOAL = (
    "Изучить методы встраивания информации в текстовый docx-контейнер для "
    "скрытой передачи данных. Реализовать программное средство, которое "
    "по заданному cover-тексту, секретному сообщению и выбранным методу "
    "форматирования и кодировке формирует новый docx-файл со встроенным "
    "сообщением."
)


_THEORY = (
    "ПР2 решает обратную задачу относительно ПР1. Секретное сообщение "
    "кодируется в битовую строку выбранной кодировкой. Для каждого бита "
    "назначается одно из двух значений выбранного параметра форматирования: "
    "«незаметное» — для нуля и «слегка изменённое» — для единицы. Каждый "
    "символ cover-текста получает соответствующий run в docx с этими "
    "значениями, и итоговый документ визуально не отличается от исходного, "
    "но корректно декодируется обратно программой ПР1."
)


_TASK_ITEMS = (
    "программно закодировать секретное сообщение (пословицу) с использованием "
    "выбранного метода стеганографического сокрытия и кодировки;",
    "сохранить полученный контейнер в новый docx-файл для последующего "
    "декодирования программой ПР1;",
    "поддержать форматирующие признаки: цвет символов, цвет фона, размер "
    "шрифта, масштаб шрифта, межсимвольный интервал;",
    "поддержать кодировки: код Бодо (МТК-2), КОИ-8R, cp866, Windows-1251, "
    "ASCII;",
    "уметь использовать в качестве cover-текста как существующий docx, так "
    "и произвольную строку.",
)


_ARCH_BULLETS = (
    "domain/common/encodings/ — общие кодировки с методами encode/decode.",
    "domain/text_format_encode/services/container_plan_builder.py — берёт "
    "секретный текст, кодирует его в биты и сопоставляет каждому символу "
    "cover значение параметра форматирования.",
    "domain/text_format_encode/services/hiding_value_defaults.py — "
    "«незаметные» пары значений по умолчанию для каждого параметра.",
    "domain/text_format_encode/errors/ — ContainerTooSmallError и "
    "UnencodableSecretError.",
    "infrastructure/text_format_encode/docx_container_writer.py — пишет "
    "docx через python-docx и прямые OOXML-элементы (w:color, w:sz, w:w, "
    "w:spacing, ...).",
    "infrastructure/text_format_encode/docx_cover_text_reader.py — читает "
    "плоский cover-текст из существующего docx.",
    "application/commands/text_format_encode/encode.py — async Command "
    "Handler EncodeSecretCommandHandler.",
    "presentation/cli/handlers/text_format_encode.py — click-команда "
    "encode с инжектом через dishka.",
)


_PLAN_BUILDER_LISTING = '''\
class ContainerPlanBuilder:
    """Строит план форматирования контейнера-результата."""

    def build(self, payload: SecretPayload, cover_text: str) -> FormattingPlan:
        bits = payload.encoding.encode(payload.secret_text)
        if bits is None:
            raise UnencodableSecretError(payload.encoding.name)
        if len(bits) > len(cover_text):
            raise ContainerTooSmallError(
                required_bits=len(bits),
                available_chars=len(cover_text),
            )

        method = payload.method
        chars: list[CharFormatting] = []
        for index, char in enumerate(cover_text):
            is_one = index < len(bits) and bits[index] == "1"
            chars.append(CharFormatting(
                char=char,
                param=method.param,
                value=method.one_value if is_one else method.zero_value,
                is_one=is_one,
            ))
        return FormattingPlan(chars=tuple(chars), payload_bits=len(bits))
'''


_WRITER_LISTING = '''\
class DocxContainerWriterImpl(ContainerWriter):
    """Пишет план форматирования в docx через python-docx + OOXML."""

    def write(self, plan: FormattingPlan, path: Path) -> None:
        document = Document()
        paragraph = document.add_paragraph()
        for char_formatting in plan.chars:
            run = paragraph.add_run(char_formatting.char)
            self._apply(run, char_formatting)
        document.save(str(path))

    def _apply(self, run: Run, formatting: CharFormatting) -> None:
        tag = _PARAM_TAG[formatting.param]
        rpr = run._element.get_or_add_rPr()
        element = OxmlElement(tag)
        element.set(qn("w:val"), formatting.value)
        rpr.append(element)
'''


def _make_handler() -> EncodeSecretCommandHandler:
    return EncodeSecretCommandHandler(
        registry=EncodingRegistry(),
        plan_builder=ContainerPlanBuilder(),
        writer=DocxContainerWriterImpl(),
    )


def _cli_listing(variant: VariantSpec, view: EncodeSecretView) -> str:
    if view.method is None:
        return f"ошибка: {view.error}"
    return (
        f"$ steganography text-format-encode encode \\\n"
        f"    -s \"{variant.secret}\" \\\n"
        f"    --cover-file resources/steganographic_concealment/covers/"
        f"{variant.cover_index}.docx \\\n"
        f"    -e {variant.encoding_name} -p {variant.param.value} \\\n"
        f"    -o resources/steganographic_concealment/generated/"
        f"variant{variant.number:02d}.docx\n"
        f"\n"
        f"+-----------------------+--------------------------------+\n"
        f"|       Встраивание в variant{variant.number:02d}.docx           |\n"
        f"+-----------------------+--------------------------------+\n"
        f"| Сообщение             | {view.secret_text}\n"
        f"| Кодировка             | {view.encoding_name}\n"
        f"| Параметр              | {view.method.param.human_name}\n"
        f"| Значение для 0        | {view.method.zero_value}\n"
        f"| Значение для 1        | {view.method.one_value}\n"
        f"| Полезных бит          | {view.payload_bits}\n"
        f"| Символов в контейнере | {view.container_chars}\n"
        f"| Статус                | {'успешно' if view.success else 'ошибка'}\n"
        f"+-----------------------+--------------------------------+\n"
    )


def _build_one(variant: VariantSpec, view: EncodeSecretView) -> Path:
    meta = LabMeta(
        number=2,
        title="Встраивание секретного сообщения в текстовый docx-контейнер",
        work_kind="Практическая работа",
        variant=variant.number,
    )
    doc = make_doc()
    add_title_page(doc, meta)
    add_page_break(doc)

    add_heading(doc, "1. Цель работы")
    add_para(doc, _GOAL)

    add_heading(doc, "2. Теоретическая часть")
    add_para(doc, _THEORY)

    add_heading(doc, "3. Задание на выполнение")
    for item in _TASK_ITEMS:
        add_para(doc, "— " + item, indent=False)

    add_heading(doc, "4. Архитектура решения (Clean Architecture)")
    add_para(
        doc,
        "Программа симметрична ПР1 по слоям. Кодировки и общий параметр "
        "форматирования вынесены в domain/common, поэтому ПР1 и ПР2 делят "
        "одно ядро. Запись docx через python-docx + прямые OOXML-элементы "
        "позволяет работать с любым из пяти параметров единообразно.",
    )
    for bullet in _ARCH_BULLETS:
        add_para(doc, "• " + bullet, indent=False)

    add_heading(doc, "5. Ключевые фрагменты кода", level=2)
    add_label(doc, "Листинг 1 — построитель плана встраивания")
    add_listing(doc, _PLAN_BUILDER_LISTING)
    add_label(doc, "Листинг 2 — запись docx-результата через OOXML")
    add_listing(doc, _WRITER_LISTING)

    add_page_break(doc)
    add_heading(doc, f"6. Индивидуальный вариант №{variant.number}", level=2)
    add_para(
        doc,
        f"Для варианта {variant.number} требуется встроить пословицу "
        f"«{variant.secret}» в стих-контейнер covers/{variant.cover_index}.docx, "
        f"используя параметр форматирования «{variant.param.human_name}» и "
        f"кодировку «{variant.encoding_name}».",
    )

    success = view.success and view.method is not None
    add_table_simple(
        doc,
        rows=[
            ["Поле", "Значение"],
            ["Cover-контейнер", f"covers/{variant.cover_index}.docx"],
            ["Файл-результат", f"variant{variant.number:02d}.docx"],
            ["Сообщение", variant.secret],
            ["Кодировка", view.encoding_name],
            ["Параметр", view.method.param.human_name if success else "—"],
            ["Значение для 0", view.method.zero_value if success else "—"],
            ["Значение для 1", view.method.one_value if success else "—"],
            ["Полезных бит", str(view.payload_bits)],
            ["Символов в cover", str(view.container_chars)],
            ["Статус", "успешно" if success else f"ошибка: {view.error}"],
        ],
        caption=(
            f"Таблица 1 — Параметры встраивания для варианта №{variant.number}"
        ),
    )

    add_label(doc, "Листинг 3 — вывод CLI-программы")
    add_listing(doc, _cli_listing(variant, view))

    add_heading(doc, "7. Вывод")
    if success:
        conclusion = (
            f"Для индивидуального варианта №{variant.number} реализованной "
            f"программой ПР2 пословица «{variant.secret}» успешно встроена в "
            f"стих-контейнер covers/{variant.cover_index}.docx через "
            f"«{view.method.param.human_name}» с кодировкой "
            f"«{view.encoding_name}» ({view.payload_bits} полезных бит на "
            f"{view.container_chars} символов контейнера). Полученный файл "
            f"variant{variant.number:02d}.docx может быть расшифрован "
            f"программой ПР1 без потери данных."
        )
    else:
        conclusion = (
            f"Для варианта №{variant.number} встраивание не удалось: "
            f"{view.error}."
        )
    add_para(doc, conclusion)

    output = _REPORTS_ROOT / str(variant.number) / "ПР2.docx"
    save(doc, output)
    return output


async def _run() -> list[tuple[VariantSpec, EncodeSecretView]]:
    handler = _make_handler()
    cover_reader = DocxCoverTextReaderImpl()
    defaults = HidingValueDefaults()
    pairs: list[tuple[VariantSpec, EncodeSecretView]] = []
    for variant in VARIANTS:
        cover_text = cover_reader.read(
            _COVERS_DIR / f"{variant.cover_index}.docx",
        )
        zero_value, one_value = defaults.for_param(variant.param)
        command = EncodeSecretCommand(
            secret_text=variant.secret,
            cover_text=cover_text,
            encoding_name=variant.encoding_name,
            param=variant.param,
            zero_value=zero_value,
            one_value=one_value,
            output_path=_GENERATED_DIR / f"variant{variant.number:02d}.docx",
        )
        view = await handler(command)
        pairs.append((variant, view))
    return pairs


def main() -> None:
    pairs = asyncio.run(_run())
    for variant, view in pairs:
        path = _build_one(variant, view)
        status = "OK" if view.success else f"FAIL: {view.error}"
        print(f"  variant {variant.number:02d}: {status} → {path}")


if __name__ == "__main__":
    main()
