"""Encode a DOCX copy, preserving all properties except the selected bit carrier.

Plain-text covers are rendered into a new document. DOCX covers retain their
original ZIP parts; only text runs in word/document.xml are split and patched.
"""

from collections import Counter
from collections.abc import Iterator
from copy import deepcopy
from dataclasses import replace
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.run import Run
from lxml import etree

from steganography.domain.common.services.formatting_shift import (
    shifted_value,
)
from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
)
from steganography.domain.text_format_encode.ports.container_writer import (
    ContainerWriter,
)
from steganography.domain.text_format_encode.value_objects.char_formatting import (
    AUTO_VALUE,
    CharFormatting,
)
from steganography.domain.text_format_encode.value_objects.formatting_plan import (
    FormattingPlan,
)


def _append_val(rpr: object, tag: str, value: str) -> None:
    element = OxmlElement(tag)
    element.set(qn("w:val"), value)
    rpr.append(element)  # type: ignore[attr-defined]


class DocxContainerWriterImpl(ContainerWriter):
    """Реализация порта записи через python-docx + прямые OOXML-элементы."""

    def write(self, plan: FormattingPlan, path: Path) -> None:
        if plan.source_docx is not None:
            self._write_source(plan, path, plan.source_docx)
            return

        document = Document()
        line_lengths = plan.line_lengths or (len(plan.chars),)

        offset = 0
        for length in line_lengths:
            paragraph = document.add_paragraph()
            for char_formatting in plan.chars[offset : offset + length]:
                run = paragraph.add_run(char_formatting.char)
                self._apply(run, char_formatting, plan)
            offset += length

        path.parent.mkdir(parents=True, exist_ok=True)
        document.save(str(path))

    @staticmethod
    def _write_source(plan: FormattingPlan, path: Path, source_docx: bytes) -> None:
        with ZipFile(BytesIO(source_docx)) as source:
            root = etree.fromstring(source.read("word/document.xml"))
            resolver: _RelativeResolver | None = None
            if plan.chars and plan.chars[0].value == AUTO_VALUE:
                param = plan.chars[0].param
                # font_size — осмысленный запасной вариант только для размера.
                font_size = plan.font_size if param is FormattingParam.SIZE else None
                resolver = _RelativeResolver(root, param, font_size)
            chars = iter(plan.chars)
            # Snapshot before splitting; each original run is processed once.
            for run in list(root.iter(qn("w:r"))):
                if not any(child.tag == qn("w:t") and child.text for child in run):
                    continue
                _split_run(run, chars, resolver)
            if next(chars, None) is not None:
                raise ValueError(_PLAN_MISMATCH)
            xml = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
            path.parent.mkdir(parents=True, exist_ok=True)
            with ZipFile(path, "w") as output:
                output.comment = source.comment
                for entry in source.infolist():
                    output.writestr(entry, xml if entry.filename == "word/document.xml" else source.read(entry))

    @staticmethod
    def _apply(
        run: Run, formatting: CharFormatting, plan: FormattingPlan,
    ) -> None:
        param = formatting.param
        value = formatting.value
        rpr = run._element.get_or_add_rPr()  # noqa: SLF001

        # Порядок дочерних элементов соответствует схеме CT_RPr.
        if plan.font_name:
            fonts = OxmlElement("w:rFonts")
            for attr in ("w:ascii", "w:hAnsi", "w:cs"):
                fonts.set(qn(attr), plan.font_name)
            rpr.append(fonts)
        if param is FormattingParam.COLOR:
            _append_val(rpr, "w:color", value)
        if param is FormattingParam.SPACING:
            _append_val(rpr, "w:spacing", value)
        if param is FormattingParam.SCALE:
            _append_val(rpr, "w:w", value)

        # Размер: носитель бита (param SIZE) или базовый шрифт контейнера.
        size_value = value if param is FormattingParam.SIZE else plan.font_size
        if size_value:
            _append_val(rpr, "w:sz", size_value)
            _append_val(rpr, "w:szCs", size_value)

        if param is FormattingParam.HIGHLIGHT:
            _append_val(rpr, "w:highlight", value)


_PLAN_MISMATCH = "DOCX text does not match the formatting plan"

# CT_RPr order starting at the earliest property used for embedding.
_PROPERTY_ORDER = (
    "color", "spacing", "w", "kern", "position", "sz", "szCs", "highlight",
    "u", "effect", "bdr", "shd", "fitText", "vertAlign", "rtl", "cs", "em",
    "lang", "eastAsianLayout", "specVanish", "oMath", "rPrChange",
)
_PROPERTY_TAGS = {
    FormattingParam.COLOR: "color",
    FormattingParam.SPACING: "spacing",
    FormattingParam.SCALE: "w",
    FormattingParam.SIZE: "sz",
    FormattingParam.HIGHLIGHT: "highlight",
}


def _patch_property(run: etree._Element, formatting: CharFormatting) -> None:
    rpr = run.find(qn("w:rPr"))
    if rpr is None:
        rpr = etree.Element(qn("w:rPr"))
        run.insert(0, rpr)
    tag = _PROPERTY_TAGS[formatting.param]
    tags = (tag, "szCs") if formatting.param is FormattingParam.SIZE else (tag,)
    for name in tags:
        for existing in list(rpr.findall(qn(f"w:{name}"))):
            rpr.remove(existing)
        element = etree.Element(qn(f"w:{name}"))
        element.set(qn("w:val"), formatting.value)
        successors = {qn(f"w:{item}") for item in _PROPERTY_ORDER[_PROPERTY_ORDER.index(name) + 1:]}
        for child in rpr:
            if child.tag in successors:
                child.addprevious(element)
                break
        else:
            rpr.append(element)
    if formatting.param is FormattingParam.SPACING:
        # This alternate spacing flag would override w:spacing in our reader.
        for flag in list(rpr.findall("{http://schemas.microsoft.com/office/word/2010/wordml}numSpacing")):
            rpr.remove(flag)


def _apply_embedding(
    piece: etree._Element,
    formatting: CharFormatting,
    resolver: _RelativeResolver | None,
) -> None:
    if formatting.value != AUTO_VALUE:
        _patch_property(piece, formatting)
        return
    # auto: нулевые биты оставляют исходное форматирование нетронутым,
    # единичные получают минимальную дельту от значения самого run'а.
    if formatting.is_one and resolver is not None:
        value = resolver.one_value(piece)
        _patch_property(piece, replace(formatting, value=value))


def _split_run(
    run: etree._Element,
    chars: Iterator[CharFormatting],
    resolver: _RelativeResolver | None = None,
) -> None:
    parent = run.getparent()
    rpr = run.find(qn("w:rPr"))
    shell = deepcopy(run)
    for child in list(shell):
        shell.remove(child)
    if rpr is not None:
        shell.append(deepcopy(rpr))
    for child in run:
        if child.tag == qn("w:rPr"):
            continue
        if child.tag == qn("w:t") and child.text:
            for char in child.text:
                formatting = next(chars, None)
                if formatting is None or formatting.char != char:
                    raise ValueError(_PLAN_MISMATCH)
                piece = deepcopy(shell)
                text = deepcopy(child)
                text.text = char
                text.set(qn("xml:space"), "preserve")
                piece.append(text)
                _apply_embedding(piece, formatting, resolver)
                run.addprevious(piece)
        else:
            piece = deepcopy(shell)
            piece.append(deepcopy(child))
            run.addprevious(piece)
    parent.remove(run)


# Смысловые значения по умолчанию, если параметр нигде в документе не задан
# (наследуется из стилей): размер 10 pt, чёрный цвет, масштаб 100 %, интервал 0.
_BASE_DEFAULTS: dict[FormattingParam, str] = {
    FormattingParam.SIZE: "20",
    FormattingParam.COLOR: "000000",
    FormattingParam.SCALE: "100",
    FormattingParam.SPACING: "0",
    FormattingParam.HIGHLIGHT: "yellow",
}


class _RelativeResolver:
    """Вычисляет «единичное» значение параметра от исходного форматирования.

    База берётся из rPr самого run'а; если там параметр не задан — из
    доминирующего по документу значения, затем из шрифта контейнера и,
    наконец, из смыслового умолчания. Так контейнер остаётся визуально
    неотличимым от оригинала, а детектор группирует значения в пары
    «база / база+дельта» (см. domain/common/services/formatting_shift).
    """

    def __init__(
        self,
        root: etree._Element,
        param: FormattingParam,
        font_size: str | None,
    ) -> None:
        self._param = param
        self._fallback = font_size
        counter: Counter[str] = Counter()
        for rpr in root.iter(qn("w:rPr")):
            element = rpr.find(qn(f"w:{_PROPERTY_TAGS[param]}"))
            value = element.get(qn("w:val")) if element is not None else None
            if value:
                counter[value] += 1
        self._dominant = counter.most_common(1)[0][0] if counter else None

    def one_value(self, run: etree._Element) -> str:
        if self._param is FormattingParam.HIGHLIGHT:
            # Относительной дельты нет: ноль — без подсветки, единица — жёлтая.
            return "yellow"
        rpr = run.find(qn("w:rPr"))
        element = (
            rpr.find(qn(f"w:{_PROPERTY_TAGS[self._param]}"))
            if rpr is not None
            else None
        )
        base = element.get(qn("w:val")) if element is not None else None
        for candidate in (
            base,
            self._dominant,
            self._fallback,
            _BASE_DEFAULTS[self._param],
        ):
            if candidate is None:
                continue
            value = shifted_value(self._param, candidate)
            if value is not None:
                return value
        raise ValueError(_PLAN_MISMATCH)
