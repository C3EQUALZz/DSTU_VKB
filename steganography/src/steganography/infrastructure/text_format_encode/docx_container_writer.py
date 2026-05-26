"""Запись контейнера-результата в docx по плану форматирования.

Для каждого символа создаётся отдельный run, в свойства которого
(``w:rPr``) добавляется элемент, соответствующий параметру сокрытия,
с предписанным значением. Тем самым полученный документ читается
детектором ПР «декод» симметрично.
"""

from pathlib import Path
from typing import Final

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.run import Run

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

_PARAM_TAG: Final[dict[FormattingParam, str]] = {
    FormattingParam.COLOR: "w:color",
    FormattingParam.HIGHLIGHT: "w:highlight",
    FormattingParam.SIZE: "w:sz",
    FormattingParam.SCALE: "w:w",
    FormattingParam.SPACING: "w:spacing",
}


class DocxContainerWriterImpl(ContainerWriter):
    """Реализация порта записи через python-docx + прямые OOXML-элементы."""

    def write(self, plan: FormattingPlan, path: Path) -> None:
        document = Document()
        paragraph = document.add_paragraph()
        for char_formatting in plan.chars:
            run = paragraph.add_run(char_formatting.char)
            self._apply(run, char_formatting)
        path.parent.mkdir(parents=True, exist_ok=True)
        document.save(str(path))

    def _apply(self, run: Run, formatting: CharFormatting) -> None:
        tag = _PARAM_TAG[formatting.param]
        rpr = run._element.get_or_add_rPr()  # noqa: SLF001
        element = OxmlElement(tag)
        element.set(qn("w:val"), formatting.value)
        rpr.append(element)
        if formatting.param is FormattingParam.SIZE:
            size_cs = OxmlElement("w:szCs")
            size_cs.set(qn("w:val"), formatting.value)
            rpr.append(size_cs)
