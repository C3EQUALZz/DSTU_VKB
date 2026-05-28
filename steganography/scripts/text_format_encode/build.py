"""Сборка docx-отчёта по ПР2 «Встраивание стег-сокрытия в текст»."""

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

_OUTPUT = _ROOT / "docs" / "reports" / "text_format_encode" / "ПР2_встраивание.docx"


_META = LabMeta(
    number=2,
    title="Встраивание секретного сообщения в текстовый docx-контейнер",
    work_kind="Практическая работа",
    variant=15,
)


_GOAL = (
    "Изучить методы встраивания информации в текстовый контейнер для "
    "скрытой передачи данных. Реализовать программное средство, которое "
    "по заданному cover-тексту, секретному сообщению и выбранным методу "
    "форматирования и кодировке формирует новый docx-файл со встроенным "
    "сообщением, а также массово генерирует 25 вариантов задания "
    "преподавателя."
)


_THEORY = (
    "ПР2 решает обратную задачу относительно ПР1. Секретное сообщение "
    "кодируется в битовую строку выбранной кодировкой (МТК-2, КОИ-8R, "
    "cp866, Windows-1251 или ASCII). Для каждого бита назначается одно из "
    "двух значений выбранного параметра форматирования: «незаметное» — для "
    "нуля и «слегка изменённое» — для единицы (например, размер шрифта "
    "14 пт vs 14,5 пт, цвет RGB(0,0,0) vs RGB(1,0,0)). Каждый символ "
    "cover-текста получает соответствующий run в docx с этими значениями, "
    "и итоговый документ визуально не отличается от исходного, но "
    "корректно декодируется обратно."
)


_TASK_ITEMS = [
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
]


_ARCH_BULLETS = [
    "domain/common/encodings/ — общие кодировки, у каждой два метода: "
    "encode(text) → bits и decode(bits) → text. Используется и в ПР1, и в "
    "ПР2 без перекрёстных зависимостей.",
    "domain/text_format_encode/services/container_plan_builder.py — берёт "
    "SecretPayload (текст + кодировка + метод) и cover-текст, кодирует "
    "сообщение в биты и сопоставляет каждому символу cover значение "
    "параметра форматирования.",
    "domain/text_format_encode/services/hiding_value_defaults.py — «незаметные» "
    "пары значений по умолчанию для каждого параметра.",
    "domain/text_format_encode/errors/ — доменные ошибки "
    "ContainerTooSmallError и UnencodableSecretError.",
    "infrastructure/text_format_encode/docx_container_writer.py — пишет "
    "docx через python-docx, добавляя соответствующие OOXML-элементы "
    "(w:color, w:sz, w:w, w:spacing, ...) с значениями плана.",
    "infrastructure/text_format_encode/docx_cover_text_reader.py — читает "
    "плоский cover-текст из существующего docx.",
    "application/commands/text_format_encode/encode.py — async Command "
    "Handler EncodeSecretCommandHandler.",
    "presentation/cli/handlers/text_format_encode.py — click-команда "
    "encode с инжектом через dishka.",
    "scripts/text_format_encode/generate_variants.py — массовая генерация "
    "25 вариантов из таблицы пословиц/методов/кодировок.",
]


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


_CLI_RUN_LISTING = """\
$ steganography text-format-encode encode \\
    -s "Без труда не вытащишь и рыбку из пруда." \\
    --cover-file resources/steganographic_concealment/covers/1.docx \\
    -e cp866 -p size -o /tmp/encoded.docx

+-----------------------+-----------------------------------------+
|              Встраивание в encoded.docx                         |
+-----------------------+-----------------------------------------+
| Поле                  | Значение                                |
+-----------------------+-----------------------------------------+
| Файл-результат        | /tmp/encoded.docx                       |
| Сообщение             | Без труда не вытащишь и рыбку из пруда. |
| Кодировка             | cp866                                   |
| Параметр              | размер шрифта                           |
| Значение для 0        | 28                                      |
| Значение для 1        | 29                                      |
| Полезных бит          | 312                                     |
| Символов в контейнере | 1798                                    |
| Статус                | успешно                                 |
+-----------------------+-----------------------------------------+
"""


# Сводка по 25 сгенерированным вариантам (encode → roundtrip → decode 25/25).
_GENERATION_HEADER = ["Файл", "Кодировка", "Параметр", "Бит", "Символов в cover"]
_GENERATION_ROWS: list[list[str]] = [
    ["variant01.docx", "КОИ-8R",       "цвет символов",            "248", "1798"],
    ["variant02.docx", "Windows-1251", "межсимвольный интервал",   "280",  "865"],
    ["variant03.docx", "Windows-1251", "размер шрифта",            "232", "1442"],
    ["variant04.docx", "cp866",        "межсимвольный интервал",   "328",  "517"],
    ["variant05.docx", "Windows-1251", "масштаб шрифта",           "184",  "425"],
    ["variant06.docx", "cp866",        "цвет символов",            "272",  "471"],
    ["variant07.docx", "cp866",        "масштаб шрифта",           "288", "1671"],
    ["variant08.docx", "Windows-1251", "цвет символов",            "424", "1235"],
    ["variant09.docx", "КОИ-8R",       "размер шрифта",            "312", "1425"],
    ["variant10.docx", "cp866",        "размер шрифта",            "288", "1211"],
    ["variant11.docx", "КОИ-8R",       "масштаб шрифта",           "224", "1798"],
    ["variant12.docx", "Windows-1251", "размер шрифта",            "320",  "865"],
    ["variant13.docx", "КОИ-8R",       "размер шрифта",            "264", "1442"],
    ["variant14.docx", "КОИ-8R",       "цвет символов",            "200",  "517"],
    ["variant15.docx", "cp866",        "размер шрифта",            "264",  "425"],
    ["variant16.docx", "КОИ-8R",       "межсимвольный интервал",   "168",  "471"],
    ["variant17.docx", "Windows-1251", "размер шрифта",            "256", "1671"],
    ["variant18.docx", "cp866",        "межсимвольный интервал",   "200", "1235"],
    ["variant19.docx", "Windows-1251", "масштаб шрифта",           "216", "1425"],
    ["variant20.docx", "cp866",        "цвет символов",            "368", "1211"],
    ["variant21.docx", "КОИ-8R",       "межсимвольный интервал",   "232", "1798"],
    ["variant22.docx", "Windows-1251", "цвет символов",            "168",  "865"],
    ["variant23.docx", "КОИ-8R",       "масштаб шрифта",           "296", "1442"],
    ["variant24.docx", "Windows-1251", "межсимвольный интервал",   "296",  "517"],
    ["variant25.docx", "Windows-1251", "цвет символов",            "272",  "425"],
]


def _build() -> None:
    doc = make_doc()
    add_title_page(doc, _META)
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
    add_heading(doc, "6. Демонстрация работы CLI", level=2)
    add_listing(doc, _CLI_RUN_LISTING, caption="Листинг 3 — пример встраивания")

    add_heading(doc, "7. Массовая генерация 25 вариантов", level=2)
    add_para(
        doc,
        "Скрипт scripts/text_format_encode/generate_variants.py собирает "
        "все 25 контейнеров по таблице задания (одна пословица на каждый "
        "вариант). Cover-стихи Барто берутся циклически из covers/. Сводка "
        "приведена в таблице ниже.",
    )
    add_table_simple(
        doc,
        [_GENERATION_HEADER, *_GENERATION_ROWS],
        caption=(
            "Таблица 1 — параметры 25 сгенерированных контейнеров"
        ),
    )

    add_heading(doc, "8. Проверка roundtrip encode → decode")
    add_para(
        doc,
        "Все 25 сгенерированных контейнеров прогнаны через программу ПР1 "
        "(text-format-decode detect-all): для каждого файла восстановлены "
        "то же сообщение, тот же метод форматирования и та же кодировка. "
        "Таким образом, encode/decode-пара работает строго обратимо. "
        "Это также подтверждается интеграционным тестом "
        "tests/integration/text_format_encode/test_encode_decode_roundtrip.py.",
    )

    add_heading(doc, "9. Вывод")
    add_para(
        doc,
        "В рамках ПР2 реализован построитель docx-контейнеров со скрытым "
        "сообщением, поддерживающий пять параметров форматирования и пять "
        "кодировок. Общее ядро кодировок (domain/common) переиспользовано "
        "из ПР1, что соответствует принципам Clean Architecture и "
        "Open-Closed. Реализована массовая генерация 25 вариантов "
        "преподавателя; полный roundtrip encode → decode подтверждён "
        "автоматическими тестами и ручным прогоном CLI.",
    )

    save(doc, _OUTPUT)
    print(f"Отчёт сохранён: {_OUTPUT}")


if __name__ == "__main__":
    _build()
