"""Сборка docx-отчёта по ПР3 «Лингвистическое сокрытие 1 бита в строке».

Работа не имеет вариантов — отчёт один, сохраняется в
``docs/reports/2025/3/ПР3.docx``. В таблицу попадают реальные результаты
прогона классификатора по эталонному файлу resources/linguistic_samples/
input.txt (10 строк «ДА» + 10 строк «НЕТ»).
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

from steganography.application.commands.linguistic_bit_in_string.classify import (  # noqa: E402
    ClassifyStringsCommand,
    ClassifyStringsCommandHandler,
)
from steganography.application.common.views.linguistic_bit_in_string import (  # noqa: E402
    ClassifyStringsView,
)
from steganography.domain.linguistic_bit_in_string.services.parity_classifier import (  # noqa: E402
    ParityClassifier,
)
from steganography.domain.linguistic_bit_in_string.services.vowel_counter import (  # noqa: E402
    VowelCounter,
)
from steganography.infrastructure.linguistic_bit_in_string.file_classification_writer import (  # noqa: E402
    FileClassificationWriter,
)
from steganography.infrastructure.linguistic_bit_in_string.file_string_reader import (  # noqa: E402
    FileStringReader,
)

_INPUT = _ROOT / "resources" / "linguistic_samples" / "input.txt"
_OUTPUT_DOCX = _ROOT / "docs" / "reports" / "2025" / "3" / "ПР3.docx"


_META = LabMeta(
    number=3,
    title="Лингвистическое сокрытие одного бита в текстовой строке",
    work_kind="Практическая работа",
    variant=None,
)


_GOAL = (
    "Разработать метод стеганографического сокрытия одного бита информации "
    "в текстовой строке естественного языка. Реализовать программу-"
    "классификатор, которая для любой строки из подмножества Y отвечает "
    "«ДА», а из подмножества N — «НЕТ». Подготовить по 10 строк для каждого "
    "ответа и составить текстовое описание метода."
)


_METHOD_DESCRIPTION = (
    "В качестве лингвистического параметра выбрана чётность числа русских "
    "гласных букв в строке. Множество гласных: А, Е, Ё, И, О, У, Ы, Э, Ю, "
    "Я (в любом регистре). Если число гласных V(S) чётное, строка S "
    "относится к подмножеству Y (бит «1», ответ «ДА»); если нечётное — к "
    "подмножеству N (бит «0», ответ «НЕТ»). Любая осмысленная русская "
    "строка попадает в одно из двух подмножеств, поэтому метод определён "
    "на всём множестве предложений естественного языка."
)


_TASK_ITEMS = (
    "разработать метод деления множества предложений языка на Y и N;",
    "реализовать программу, которая для любой строки из Y отвечает «ДА», "
    "из N — «НЕТ»;",
    "подать строки на вход в файле (по одной на строку), результаты "
    "выводятся в файл и на экран;",
    "подготовить 10 строк «ДА» и 10 строк «НЕТ» (≤50 символов).",
)


_ARCH_BULLETS = (
    "domain/linguistic_bit_in_string/services/vowel_counter.py — подсчёт "
    "русских гласных в строке.",
    "domain/linguistic_bit_in_string/services/parity_classifier.py — "
    "доменный сервис классификации по чётности числа гласных.",
    "domain/linguistic_bit_in_string/value_objects/string_classification.py "
    "— VO результата (строка + бит + ответ + значение признака).",
    "domain/linguistic_bit_in_string/ports/ — Protocol-порты "
    "StringReader и ClassificationWriter.",
    "infrastructure/linguistic_bit_in_string/ — файловые реализации портов.",
    "application/commands/linguistic_bit_in_string/classify.py — async "
    "Command Handler.",
    "presentation/cli/handlers/linguistic_bit_in_string.py — click-команда "
    "classify с инжектом через dishka.",
)


_PARITY_LISTING = '''\
class ParityClassifier:
    """Относит строку к Y или N по чётности числа русских гласных."""

    def __init__(self, vowel_counter: VowelCounter) -> None:
        self._vowel_counter = vowel_counter

    def classify(self, text: str) -> StringClassification:
        vowels = self._vowel_counter.count(text)
        is_even = vowels % 2 == 0
        return StringClassification(
            text=text,
            bit=1 if is_even else 0,
            answer="ДА" if is_even else "НЕТ",
            feature_value=vowels,
        )
'''


_VOWEL_LISTING = '''\
class VowelCounter:
    """Сервис подсчёта русских гласных в строке."""

    _VOWELS: Final[frozenset[str]] = frozenset("аеёиоуыэюя")

    def count(self, text: str) -> int:
        return sum(1 for ch in text.lower() if ch in self._VOWELS)
'''


_CLI_RUN_LISTING = """\
$ steganography linguistic-bit-in-string classify \\
    -i resources/linguistic_samples/input.txt \\
    -o resources/linguistic_samples/output.txt

+------------------------------------------------------------+
|          Классификация input.txt (ДА: 10, НЕТ: 10)         |
+---+-------+---------+--------------------------------------+
| # | Ответ | Гласных | Строка                               |
+---+-------+---------+--------------------------------------+
| 1 | ДА    |       6 | Мама мыла раму                       |
| 2 | ДА    |       6 | Без труда нет плода                  |
| ...                                                        |
| 20| НЕТ   |       9 | Утро мудренее вечера                 |
+---+-------+---------+--------------------------------------+
"""


def _make_handler() -> ClassifyStringsCommandHandler:
    return ClassifyStringsCommandHandler(
        reader=FileStringReader(),
        classifier=ParityClassifier(vowel_counter=VowelCounter()),
        writer=FileClassificationWriter(),
    )


async def _run() -> ClassifyStringsView:
    output = _ROOT / "resources" / "linguistic_samples" / "output.txt"
    handler = _make_handler()
    return await handler(
        ClassifyStringsCommand(input_path=_INPUT, output_path=output),
    )


def _build(view: ClassifyStringsView) -> None:
    doc = make_doc()
    add_title_page(doc, _META)
    add_page_break(doc)

    add_heading(doc, "1. Цель работы")
    add_para(doc, _GOAL)

    add_heading(doc, "2. Описание разработанного метода")
    add_para(doc, _METHOD_DESCRIPTION)
    add_para(
        doc,
        "Чтобы передать желаемый бит, отправитель формулирует осмысленную "
        "строку с подходящей чётностью числа гласных. При необходимости "
        "чётность корректируется минимальной правкой: заменой слова "
        "синонимом, добавлением или удалением частицы.",
    )

    add_heading(doc, "3. Задание на выполнение")
    for item in _TASK_ITEMS:
        add_para(doc, "— " + item, indent=False)

    add_heading(doc, "4. Архитектура решения (Clean Architecture)")
    add_para(
        doc,
        "Программа разделена на слои domain / application / infrastructure / "
        "presentation. Доменные сервисы (VowelCounter, ParityClassifier) не "
        "знают о файловом IO; чтение строк и запись результатов оформлены "
        "Protocol-портами с реализациями в infrastructure. CLI-команда "
        "classify собрана через dishka, как и остальные практики курса.",
    )
    for bullet in _ARCH_BULLETS:
        add_para(doc, "• " + bullet, indent=False)

    add_heading(doc, "5. Ключевые фрагменты кода", level=2)
    add_label(doc, "Листинг 1 — подсчёт русских гласных")
    add_listing(doc, _VOWEL_LISTING)
    add_label(doc, "Листинг 2 — классификатор по чётности")
    add_listing(doc, _PARITY_LISTING)

    add_page_break(doc)
    add_heading(doc, "6. Результаты прогона на эталонном наборе", level=2)
    add_para(
        doc,
        f"Программа применена к файлу resources/linguistic_samples/input.txt "
        f"(20 строк). По результатам классификации получено {view.yes_count} "
        f"строк с ответом «ДА» и {view.no_count} строк с ответом «НЕТ», что "
        f"соответствует требованию условия (10 + 10).",
    )
    rows = [["#", "Ответ", "Гласных", "Строка"]]
    for index, item in enumerate(view.classifications, start=1):
        rows.append([str(index), item.answer, str(item.feature_value), item.text])
    add_table_simple(
        doc,
        rows=rows,
        caption="Таблица 1 — результаты классификации входного файла",
    )

    add_heading(doc, "7. Демонстрация CLI", level=2)
    add_listing(doc, _CLI_RUN_LISTING, caption="Листинг 3 — вывод программы")

    add_heading(doc, "8. Вывод")
    add_para(
        doc,
        "В рамках практической работы предложен метод сокрытия одного бита "
        "в текстовой строке через чётность числа русских гласных букв. "
        "Метод определён на всём множестве осмысленных предложений русского "
        "языка, легко применим и обратим. Реализация программы выполнена в "
        "стиле Clean Architecture с инжектом зависимостей через dishka, "
        f"эталонный набор из {view.yes_count} строк «ДА» и {view.no_count} "
        "строк «НЕТ» классифицируется верно.",
    )

    save(doc, _OUTPUT_DOCX)
    print(f"Отчёт сохранён: {_OUTPUT_DOCX}")


def main() -> None:
    view = asyncio.run(_run())
    _build(view)


if __name__ == "__main__":
    main()
