"""Encode a DOCX copy, preserving all properties except the selected bit carrier.

Plain-text covers are rendered into a new document. DOCX covers retain their
original ZIP parts; only text runs in word/document.xml are split and patched.
"""

from collections.abc import Iterator
from copy import deepcopy
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.run import Run
from lxml import etree

from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
)
from steganography.domain.text_format_encode.ports.container_writer import (
    ContainerWriter,
)
from steganography.domain.text_format_encode.value_objects.char_formatting import (
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
            chars = iter(plan.chars)
            # Snapshot before splitting; each original run is processed once.
            for run in list(root.iter(qn("w:r"))):
                if not any(child.tag == qn("w:t") and child.text for child in run):
                    continue
                _split_run(run, chars)
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


def _split_run(run: etree._Element, chars: Iterator[CharFormatting]) -> None:
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
                _patch_property(piece, formatting)
                run.addprevious(piece)
        else:
            piece = deepcopy(shell)
            piece.append(deepcopy(child))
            run.addprevious(piece)
    parent.remove(run)
