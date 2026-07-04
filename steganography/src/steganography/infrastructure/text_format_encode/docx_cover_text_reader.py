"""Чтение текста-контейнера из docx с сохранением построчной структуры.

Обходит word/document.xml через :mod:`lxml`. Каждый абзац (``w:p``) и
каждый явный перевод строки (``w:br`` / ``w:cr``) внутри него становится
отдельной строкой :class:`CoverText`. Из первого run-а с заданным шрифтом
считываются имя шрифта (``w:rFonts/@w:ascii``) и размер (``w:sz/@w:val``),
чтобы писатель воссоздал контейнер в исходном оформлении.

Поток видимых символов (``w:t``) при этом не меняется — переносы строк в
OOXML не являются символами, поэтому встраивание и последующее
декодирование остаются побитово согласованными.
"""

import zipfile
from pathlib import Path
from typing import Final

from lxml import etree

from steganography.domain.text_format_encode.ports.cover_text_reader import (
    CoverTextReader,
)
from steganography.domain.text_format_encode.value_objects.cover_text import (
    CoverText,
)

_W_NS: Final[str] = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def _local(tag: object) -> str:
    return str(tag).rsplit("}", 1)[-1]


class DocxCoverTextReaderImpl(CoverTextReader):
    """Реализация порта чтения cover-текста из docx."""

    def read(self, path: Path) -> CoverText:
        with (
            zipfile.ZipFile(path) as archive,
            archive.open("word/document.xml") as document_xml,
        ):
            root = etree.parse(document_xml).getroot()

        lines: list[str] = []
        font_name: str | None = None
        font_size: str | None = None

        for paragraph in root.iter(f"{{{_W_NS}}}p"):
            current: list[str] = []
            for node in paragraph.iter():
                tag = _local(node.tag)
                if tag == "rFonts" and font_name is None:
                    font_name = node.get(f"{{{_W_NS}}}ascii")
                elif tag == "sz" and font_size is None:
                    font_size = node.get(f"{{{_W_NS}}}val")
                elif tag == "t" and node.text:
                    current.append(node.text)
                elif tag in ("br", "cr"):
                    lines.append("".join(current))
                    current = []
            lines.append("".join(current))

        return CoverText(
            lines=tuple(lines),
            font_name=font_name,
            font_size=font_size,
        )
