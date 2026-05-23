"""Генератор docx-отчётов по лабораторным курса «Криптографические протоколы».

Шаблон титульного листа повторяет эталон из методов и средств защиты информации.
Преподаватель — Дубровина А.С., год — 2026, студент — Ковалев Д.П. ВКБ43.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from docx import Document
from docx.document import Document as _Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.shared import Cm, Pt, RGBColor

STUDENT_NAME = "Ковалев Данил Петрович"
STUDENT_GROUP = "ВКБ43"
TEACHER = "Дубровина А.С."
DISCIPLINE = "Криптографические протоколы"
CITY = "Ростов-на-Дону"
YEAR = "2026"

BODY_FONT = "Times New Roman"
BODY_SIZE = Pt(14)
MONO_FONT = "Courier New"
MONO_SIZE = Pt(10)


@dataclass
class LabMeta:
    number: int
    title: str  # тема работы
    variant: int | None = None


def _setup_default_style(doc: _Document) -> None:
    style = doc.styles["Normal"]
    style.font.name = BODY_FONT
    style.font.size = BODY_SIZE
    pf = style.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.first_line_indent = Cm(1.25)
    pf.space_after = Pt(0)


def _set_margins(doc: _Document) -> None:
    for section in doc.sections:
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(3)
        section.right_margin = Cm(1.5)


def _add_centered(
    doc: _Document, text: str, *, bold: bool = False, size: Pt | None = None
) -> None:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    run = p.add_run(text)
    run.bold = bold
    if size is not None:
        run.font.size = size
    run.font.name = BODY_FONT


def _add_right(doc: _Document, text: str, *, bold: bool = False) -> None:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.first_line_indent = Cm(0)
    run = p.add_run(text)
    run.bold = bold
    run.font.name = BODY_FONT


def _add_left(doc: _Document, text: str, *, bold: bool = False) -> None:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.first_line_indent = Cm(0)
    run = p.add_run(text)
    run.bold = bold
    run.font.name = BODY_FONT


def add_title_page(doc: _Document, meta: LabMeta) -> None:
    """Добавляет стандартный титульник ДГТУ."""
    _add_centered(doc, "МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ", bold=True)
    _add_centered(doc, "ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ", bold=True)
    _add_centered(doc, "ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ ВЫСШЕГО ОБРАЗОВАНИЯ", bold=True)
    _add_centered(doc, "«ДОНСКОЙ ГОСУДАРСТВЕННЫЙ ТЕХНИЧЕСКИЙ УНИВЕРСИТЕТ»", bold=True)
    _add_centered(doc, "(ДГТУ)", bold=True)
    doc.add_paragraph()
    _add_centered(doc, "Факультет «Информатика и вычислительная техника»")
    _add_centered(doc, "Кафедра «Кибербезопасность информационных систем»")
    for _ in range(5):
        doc.add_paragraph()
    _add_centered(doc, f"Лабораторная работа №{meta.number}", bold=True, size=Pt(16))
    _add_centered(doc, f"по дисциплине: «{DISCIPLINE}»")
    variant_suffix = (
        f" (вариант №{meta.variant})" if meta.variant is not None else ""
    )
    _add_centered(doc, f"На тему «{meta.title}»{variant_suffix}", bold=True)
    for _ in range(6):
        doc.add_paragraph()
    _add_right(doc, f"Выполнил обучающийся гр. {STUDENT_GROUP}")
    _add_right(doc, STUDENT_NAME)
    doc.add_paragraph()
    _add_right(doc, "Проверила:")
    _add_right(doc, TEACHER)
    for _ in range(6):
        doc.add_paragraph()
    _add_centered(doc, CITY)
    _add_centered(doc, YEAR)


def add_heading(doc: _Document, text: str, *, level: int = 1) -> None:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.bold = True
    run.font.name = BODY_FONT
    run.font.size = Pt(16 if level == 1 else 14)


def add_para(doc: _Document, text: str, *, indent: bool = True) -> None:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if not indent:
        p.paragraph_format.first_line_indent = Cm(0)
    run = p.add_run(text)
    run.font.name = BODY_FONT
    run.font.size = BODY_SIZE


def add_label(doc: _Document, text: str) -> None:
    """Подпись к рисунку/листингу — по центру, с отступом."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run(text)
    run.italic = True
    run.font.name = BODY_FONT
    run.font.size = Pt(13)


def add_listing(doc: _Document, code: str, caption: str | None = None) -> None:
    """Листинг кода/вывода — моноширинный, рамка имитируется отступом и заливкой нельзя
    через python-docx без XML-хака, поэтому делаем просто сменой шрифта."""
    for line in code.rstrip("\n").splitlines():
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.left_indent = Cm(0.5)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        run = p.add_run(line if line else " ")
        run.font.name = MONO_FONT
        run.font.size = MONO_SIZE
        run.font.color.rgb = RGBColor(0x10, 0x10, 0x10)
    if caption:
        add_label(doc, caption)


def add_bullets(doc: _Document, items: list[str]) -> None:
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        run = p.add_run(item)
        run.font.name = BODY_FONT
        run.font.size = BODY_SIZE


def make_doc() -> _Document:
    doc = Document()
    _setup_default_style(doc)
    _set_margins(doc)
    return doc


def save(doc: _Document, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(path))
