"""Чтение docx-контейнера в плоскую последовательность размеченных символов.

Парсер работает напрямую с word/document.xml через :mod:`lxml`: python-docx
склеивает соседние run-ы со схожим форматированием и не отдаёт значения
атрибутов w:color/w:highlight/w:sz/w:w/w:spacing в удобной форме.

Каждому символу присваивается значение по каждому из пяти параметров
форматирования. Если атрибут в run-е отсутствует, записывается специальный
маркер :data:`_DEFAULT` — без него «по умолчанию» и «явно заданное»
значение нельзя было бы различить, и часть вариантов сокрытия (например,
через масштаб 99% при базовом 100%) оставалась незамеченной.

Помимо стандартных тегов с атрибутом ``val`` парсер обрабатывает
``mc:numSpacing`` из Office 2010 — это альтернатива ``w:spacing``,
которая записывается как пустой тег-флаг (его наличие означает изменённый
интервал, отсутствие — обычный).
"""

import zipfile
from pathlib import Path
from typing import Final

from lxml import etree

from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
)
from steganography.domain.text_format_decode.ports.docx_formatting_reader import (
    DocxFormattingReader,
)
from steganography.domain.text_format_decode.value_objects.formatted_char import (
    FormattedChar,
)

_W_NS: Final[str] = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
_W14_NS: Final[str] = "http://schemas.microsoft.com/office/word/2010/wordml"
_NS: Final[dict[str, str]] = {"w": _W_NS, "w14": _W14_NS}
_W_VAL: Final[str] = f"{{{_W_NS}}}val"

_DEFAULT: Final[str] = "<default>"
_FLAG_ON: Final[str] = "<on>"

_VAL_TAGS: Final[dict[FormattingParam, str]] = {
    FormattingParam.COLOR: f"{{{_W_NS}}}color",
    FormattingParam.HIGHLIGHT: f"{{{_W_NS}}}highlight",
    FormattingParam.SIZE: f"{{{_W_NS}}}sz",
    FormattingParam.SCALE: f"{{{_W_NS}}}w",
    FormattingParam.SPACING: f"{{{_W_NS}}}spacing",
}

_FLAG_TAGS: Final[dict[FormattingParam, str]] = {
    FormattingParam.SPACING: f"{{{_W14_NS}}}numSpacing",
}


class DocxFormattingReaderImpl(DocxFormattingReader):
    """Возвращает список :class:`FormattedChar` в порядке появления."""

    def read(self, path: Path) -> list[FormattedChar]:
        with zipfile.ZipFile(path) as zf, zf.open("word/document.xml") as fp:
            tree = etree.parse(fp)
        root = tree.getroot()

        chars: list[FormattedChar] = []
        for paragraph in root.iter(f"{{{_W_NS}}}p"):
            for run in paragraph.iter(f"{{{_W_NS}}}r"):
                text_el = run.find("w:t", _NS)
                if text_el is None or text_el.text is None:
                    continue
                attrs = _extract_attrs(run.find("w:rPr", _NS))
                chars.extend(
                    FormattedChar(char=ch, attrs=dict(attrs))
                    for ch in text_el.text
                )
        return chars


def _extract_attrs(
    rpr: etree._Element | None,
) -> dict[FormattingParam, str]:
    out: dict[FormattingParam, str] = dict.fromkeys(FormattingParam, _DEFAULT)
    if rpr is None:
        return out
    for param, tag in _VAL_TAGS.items():
        el = rpr.find(tag)
        if el is None:
            continue
        val = el.get(_W_VAL)
        if val is not None:
            out[param] = val
    for param, tag in _FLAG_TAGS.items():
        if rpr.find(tag) is not None:
            out[param] = _FLAG_ON
    return out
