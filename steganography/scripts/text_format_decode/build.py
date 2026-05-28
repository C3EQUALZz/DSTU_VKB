"""Сборка docx-отчётов по ПР1 для всех 25 вариантов.

Каждый отчёт сохраняется в docs/reports/2025/1/<вариант>/ПР1.docx и содержит
персонализированный титульный лист (Вариант №N) + реальный результат прогона
программы детектирования по сгенерированному контейнеру variantNN.docx.
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

from steganography.application.commands.text_format_decode.decode import (  # noqa: E402
    DetectSecretCommand,
    DetectSecretCommandHandler,
)
from steganography.application.common.views.text_format_decode import (  # noqa: E402
    DetectSecretView,
)
from steganography.domain.common.encodings.encoding_registry import (  # noqa: E402
    EncodingRegistry,
)
from steganography.domain.text_format_decode.language.russian_language_statistics import (  # noqa: E402
    RussianLanguageStatistics,
)
from steganography.domain.text_format_decode.services.code_decoder import (  # noqa: E402
    CodeDecoder,
)
from steganography.domain.text_format_decode.services.formatting_detector import (  # noqa: E402
    FormattingDetector,
)
from steganography.infrastructure.text_format_decode.docx_reader import (  # noqa: E402
    DocxFormattingReaderImpl,
)

_GENERATED_DIR = (
    _ROOT / "resources" / "steganographic_concealment" / "generated"
)
_REPORTS_ROOT = _ROOT / "docs" / "reports" / "2025" / "1"


_GOAL = (
    "Изучить виды стеганографического сокрытия информации в текстовых "
    "документах MS Word, реализовать программное средство, которое для "
    "произвольного контейнера определяет использованный параметр "
    "форматирования, восстанавливает битовую строку и подбирает "
    "кодировку (МТК-2, КОИ-8R, cp866, Windows-1251, ASCII), после чего "
    "извлекает скрытое сообщение."
)


_THEORY = (
    "Стеганография в текстовых документах основана на специфическом "
    "форматировании отдельных символов. Каждый символ контейнера несёт один "
    "бит сообщения: для нуля оставляется исходное форматирование, для "
    "единицы — незначительно изменённое (размер шрифта 14 → 14,5 пт; цвет "
    "RGB(0,0,0) → RGB(1,0,0); масштаб 100 → 99 % и т.д.). Битовая строка "
    "собирается посимвольно, после чего разбивается на кодовые слова "
    "длиной 5 (МТК-2) или 8 бит (остальные кодировки)."
)


_TASK_ITEMS = (
    "программно реализовать все методы стеганографического сокрытия и все "
    "поддерживаемые кодировки;",
    "для заданного файла определить использованный параметр форматирования, "
    "кодировку и восстановить скрытое сообщение;",
    "поддержать форматирующие признаки: цвет символов, цвет фона, размер "
    "шрифта, масштаб шрифта, межсимвольный интервал;",
    "поддержать кодировки: код Бодо (МТК-2), КОИ-8R, cp866, Windows-1251, "
    "ASCII.",
)


_ARCH_BULLETS = (
    "domain/common/encodings/ — общие кодировки (двунаправленные encode/decode).",
    "domain/text_format_decode/services/formatting_detector.py — выбирает "
    "параметр форматирования, принимающий ровно два значения.",
    "domain/text_format_decode/services/code_decoder.py — перебирает "
    "кодировки и инверсии 0/1, оценивает кандидатов по частотам русского "
    "языка.",
    "infrastructure/text_format_decode/docx_reader.py — читает docx через "
    "lxml; ловит явные значения (w:color/w:sz/...) и тег-флаг mc:numSpacing "
    "из Office 2010.",
    "application/commands/text_format_decode/decode.py — async Command "
    "Handler.",
    "presentation/cli/handlers/text_format_decode.py — click-команды "
    "detect/detect-all с инжектом через dishka.",
)


_DETECTOR_LISTING = '''\
class FormattingDetector:
    """Находит несущий параметр форматирования."""

    def detect(self, chars: list[FormattedChar]) -> FormattingMethod | None:
        candidates: list[FormattingMethod] = []
        for param in FormattingParam:
            counter: Counter[str] = Counter(
                c.attrs[param] for c in chars if param in c.attrs
            )
            if len(counter) != 2:
                continue
            (zero_value, _), (one_value, _) = counter.most_common(2)
            candidates.append(FormattingMethod(
                param=param,
                zero_value=zero_value,
                one_value=one_value,
            ))
        if not candidates:
            return None
        candidates.sort(
            key=lambda m: _signal_strength(chars, m), reverse=True,
        )
        return candidates[0]
'''


_DECODER_LISTING = '''\
class CodeDecoder:
    """Перебирает кодировки и инверсию ролей 0/1, выбирает лучший вариант."""

    def decode(self, chars, method) -> DecodedMessage | None:
        inverted = FormattingMethod(
            param=method.param,
            zero_value=method.one_value,
            one_value=method.zero_value,
        )
        candidates: list[tuple[float, DecodedMessage]] = []
        for variant_method in (method, inverted):
            bits = build_bit_sequence(chars, variant_method)
            trimmed = trim_trailing_zeros(bits)
            for encoding in self._registry.all():
                text = encoding.decode(trimmed)
                if text is None or _meaningfulness_score(text) < self._min_score:
                    continue
                weight = self._confidence(text, _meaningfulness_score(text), encoding)
                candidates.append((weight, DecodedMessage(...)))
        return max(candidates, key=lambda x: x[0])[1] if candidates else None
'''


def _make_handler() -> DetectSecretCommandHandler:
    return DetectSecretCommandHandler(
        reader=DocxFormattingReaderImpl(),
        detector=FormattingDetector(),
        decoder=CodeDecoder(
            registry=EncodingRegistry(),
            language=RussianLanguageStatistics(),
            min_score=0.8,
        ),
    )


def _cli_listing(variant: VariantSpec, view: DetectSecretView) -> str:
    if not view.success or view.method is None or view.encoding is None:
        return (
            f"$ steganography text-format-decode detect -f variant{variant.number:02d}.docx\n"
            f"ошибка: {view.error}\n"
        )
    return (
        f"$ steganography text-format-decode detect \\\n"
        f"    -f resources/steganographic_concealment/generated/"
        f"variant{variant.number:02d}.docx\n"
        f"\n"
        f"+-------------------------+-------------------------------------+\n"
        f"|            Анализ контейнера variant{variant.number:02d}.docx"
        f"                       |\n"
        f"+-------------------------+-------------------------------------+\n"
        f"| Параметр форматирования | {view.method.param.human_name}\n"
        f"| Атрибут docx            | w:{view.method.param.value}\n"
        f"| Значение для 0          | {view.method.zero_value}\n"
        f"| Значение для 1          | {view.method.one_value}\n"
        f"| Кодировка               | {view.encoding.name}\n"
        f"| Длина битовой строки    | {len(view.bit_sequence)}\n"
        f"| Сообщение               | {view.message.strip()}\n"
        f"+-------------------------+-------------------------------------+\n"
    )


def _build_one(variant: VariantSpec, view: DetectSecretView) -> Path:
    meta = LabMeta(
        number=1,
        title="Декодирование стеганографического сокрытия в текстовом контейнере",
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
        "Программа разделена на слои domain / application / infrastructure / "
        "presentation с инжектом зависимостей через dishka. Кодировки и "
        "общие параметры форматирования вынесены в domain/common, что "
        "позволило ПР2 переиспользовать их без перекрёстных зависимостей.",
    )
    for bullet in _ARCH_BULLETS:
        add_para(doc, "• " + bullet, indent=False)

    add_heading(doc, "5. Ключевые фрагменты кода", level=2)
    add_label(doc, "Листинг 1 — детектор метода форматирования")
    add_listing(doc, _DETECTOR_LISTING)
    add_label(doc, "Листинг 2 — декодер с языковым скорингом")
    add_listing(doc, _DECODER_LISTING)

    add_page_break(doc)
    add_heading(doc, f"6. Индивидуальный вариант №{variant.number}", level=2)
    add_para(
        doc,
        f"Для варианта {variant.number} в качестве cover-контейнера "
        f"использован стих covers/{variant.cover_index}.docx, в который "
        f"посредством параметра «{variant.param.human_name}» и кодировки "
        f"«{variant.encoding_name}» встроено секретное сообщение: "
        f"«{variant.secret}». Файл-результат — "
        f"resources/steganographic_concealment/generated/"
        f"variant{variant.number:02d}.docx.",
    )

    success = view.success and view.method is not None and view.encoding is not None
    add_table_simple(
        doc,
        rows=[
            ["Поле", "Значение"],
            ["Файл", f"variant{variant.number:02d}.docx"],
            ["Параметр", view.method.param.human_name if success else "—"],
            ["Атрибут docx", f"w:{view.method.param.value}" if success else "—"],
            ["Значение для 0", view.method.zero_value if success else "—"],
            ["Значение для 1", view.method.one_value if success else "—"],
            ["Кодировка", view.encoding.name if success else "—"],
            ["Длина битовой строки", str(len(view.bit_sequence))],
            ["Извлечённое сообщение", view.message.strip() if success else f"ошибка: {view.error}"],
        ],
        caption=(
            f"Таблица 1 — Результат декодирования контейнера "
            f"variant{variant.number:02d}.docx"
        ),
    )

    add_label(doc, "Листинг 3 — вывод CLI-программы")
    add_listing(doc, _cli_listing(variant, view))

    add_heading(doc, "7. Вывод")
    if success:
        conclusion = (
            f"В рамках практической работы реализован детектор "
            f"стеганографического сокрытия в текстовых docx-документах. "
            f"Для индивидуального варианта №{variant.number} программа "
            f"определила, что сокрытие выполнено через "
            f"«{view.method.param.human_name}» с кодировкой "
            f"«{view.encoding.name}», и восстановила сообщение "
            f"«{view.message.strip()}»."
        )
    else:
        conclusion = (
            f"Для варианта №{variant.number} программа не смогла извлечь "
            f"осмысленное сообщение: {view.error}."
        )
    add_para(doc, conclusion)

    output = _REPORTS_ROOT / str(variant.number) / "ПР1.docx"
    save(doc, output)
    return output


async def _run() -> list[tuple[VariantSpec, DetectSecretView]]:
    handler = _make_handler()
    pairs: list[tuple[VariantSpec, DetectSecretView]] = []
    for variant in VARIANTS:
        docx_path = _GENERATED_DIR / f"variant{variant.number:02d}.docx"
        view = await handler(DetectSecretCommand(docx_path=docx_path))
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
