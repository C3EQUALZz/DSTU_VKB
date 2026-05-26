"""Чтение «голого» текста-контейнера из docx-файла.

Собирает текст всех run-ов документа в одну строку. Переносы абзацев в
OOXML не попадают в ``w:t``, поэтому результат — плоский текст без
символов новой строки, что удобно для посимвольного встраивания.
"""

import zipfile
from pathlib import Path
from typing import Final

from lxml import etree

from steganography.domain.text_format_encode.ports.cover_text_reader import (
    CoverTextReader,
)

_W_NS: Final[str] = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


class DocxCoverTextReaderImpl(CoverTextReader):
    """Реализация порта чтения cover-текста из docx."""

    def read(self, path: Path) -> str:
        with (
            zipfile.ZipFile(path) as archive,
            archive.open("word/document.xml") as document_xml,
        ):
            tree = etree.parse(document_xml)
        return "".join(
            element.text
            for element in tree.getroot().iter(f"{{{_W_NS}}}t")
            if element.text
        )
