"""Сборка docx-отчёта по ПР1 «Декодирование стег-сокрытия в тексте»."""

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

_LOGO = _ROOT / "docs" / "assets" / "dstu_logo.png"
_OUTPUT = _ROOT / "docs" / "reports" / "text_format_decode" / "ПР1_декодирование.docx"


_META = LabMeta(
    number=1,
    title="Декодирование стеганографического сокрытия в текстовом контейнере",
    work_kind="Практическая работа",
    variant=15,
)


_GOAL = (
    "Изучить виды стеганографического сокрытия информации в текстовых "
    "документах MS Word, реализовать программное средство, которое для "
    "произвольного контейнера определяет использованный параметр "
    "форматирования, восстанавливает битовую строку и подбирает кодировку "
    "(МТК-2, КОИ-8R, cp866, Windows-1251, ASCII), после чего извлекает "
    "скрытое сообщение."
)


_THEORY = (
    "Стеганографические методы получили широкое распространение для защиты "
    "конфиденциальной информации. В рассматриваемой работе используется "
    "сокрытие в текстовых документах за счёт специфического форматирования "
    "символов: каждый символ контейнера несёт один бит сообщения. Для нуля "
    "оставляется исходное форматирование, для единицы — незначительно "
    "изменённое (например, размер шрифта 14 → 14,5 пт или цвет RGB(0,0,0) "
    "→ RGB(1,0,0)). Битовая строка собирается посимвольно, после чего "
    "разделяется на кодовые слова длиной 5 (МТК-2) или 8 бит "
    "(остальные кодировки)."
)


_TASK_ITEMS = [
    "программно реализовать все методы стеганографического сокрытия и все "
    "поддерживаемые кодировки;",
    "для заданного файла определить использованный параметр форматирования, "
    "кодировку и восстановить скрытое сообщение;",
    "поддержать форматирующие признаки: цвет символов, цвет фона, размер "
    "шрифта, масштаб шрифта, межсимвольный интервал;",
    "поддержать кодировки: код Бодо (МТК-2), КОИ-8R, cp866, Windows-1251, "
    "ASCII.",
]


_ARCH_BULLETS = [
    "domain/common/encodings/ — общие кодировки (двунаправленные encode/decode).",
    "domain/text_format_decode/services/formatting_detector.py — выбирает "
    "параметр форматирования, принимающий ровно два значения.",
    "domain/text_format_decode/services/code_decoder.py — перебирает "
    "кодировки и обе инверсии 0/1, оценивает кандидатов по частотам "
    "русского языка.",
    "domain/text_format_decode/language/russian_language_statistics.py — "
    "эталонные частоты букв русского литературного языка.",
    "infrastructure/text_format_decode/docx_reader.py — читает docx через "
    "lxml, ловит как явные значения (w:color/w:sz/...), так и тег-флаг "
    "mc:numSpacing из Office 2010.",
    "application/commands/text_format_decode/decode.py — async Command "
    "Handler (Clean Architecture).",
    "presentation/cli/handlers/text_format_decode.py — click-команды "
    "detect / detect-all с инжектом через dishka.",
]


# Результаты прогона на 25 вариантах преподавателя.
_RESULTS_HEADER = ["Файл", "Параметр", "Кодировка", "Сообщение"]
_RESULTS_ROWS: list[list[str]] = [
    ["variant01.docx", "цвет символов", "КОИ-8R",
     "Завтра подует завтрашний ветер."],
    ["variant02.docx", "межсимвольный интервал", "Windows-1251",
     "Пусть не хвалят, лишь бы не ругали."],
    ["variant03.docx", "—", "—",
     "не распознано (наложение сокрытия и оформления стиха)"],
    ["variant04.docx", "межсимвольный интервал", "cp866",
     "В споре побеждает тот, кто громче кричит."],
    ["variant05.docx", "масштаб шрифта", "Windows-1251",
     "У других цветы красней."],
    ["variant06.docx", "цвет символов", "cp866",
     "Все, что цветет, неизбежно увянет."],
    ["variant07.docx", "масштаб шрифта", "cp866",
     "Где права сила, там бессильно право."],
    ["variant08.docx", "цвет символов", "Windows-1251",
     "Прямой человек, что прямой бамбук, встречается редко."],
    ["variant09.docx", "размер шрифта", "КОИ-8R",
     "Женщина захочет ) сквозь скалу пройдет."],
    ["variant10.docx", "размер шрифта", "cp866",
     "Баклажан на стебле дыни не вырастет."],
    ["variant11.docx", "масштаб шрифта", "КОИ-8R",
     "И мотылек живет целую жизнь."],
    ["variant12.docx", "размер шрифта", "Windows-1251",
     "Пятьдесят сегодня лучше, чем сто завтра."],
    ["variant13.docx", "размер шрифта", "КОИ-8R",
     "Крупная рыба в болоте не водится."],
    ["variant14.docx", "цвет символов", "КОИ-8R",
     "Нет врага опаснее дурака."],
    ["variant15.docx", "размер шрифта", "cp866",
     "Ветер дует, но горы не двигаются."],
    ["variant16.docx", "межсимвольный интервал", "КОИ-8R",
     "Об обычаях не спорят."],
    ["variant17.docx", "размер шрифта", "Windows-1251",
     "Один бог забыл ) другой поможет."],
    ["variant18.docx", "межсимвольный интервал", "cp866",
     "Дела говорят громче слов."],
    ["variant19.docx", "масштаб шрифта", "Windows-1251",
     "Пустая бочка громче гремит."],
    ["variant20.docx", "цвет символов", "cp866",
     "Бесполезнее, чем писать цифры на текущей воде."],
    ["variant21.docx", "межсимвольный интервал", "КОИ-8R",
     "Конец болтовни ) начало дела."],
    ["variant22.docx", "цвет символов", "Windows-1251",
     "Таланты не наследуют."],
    ["variant23.docx", "масштаб шрифта", "КОИ-8R",
     "Никто не спотыкается, лежа в постели."],
    ["variant24.docx", "межсимвольный интервал", "Windows-1251",
     "Уступай дорогу дуракам и сумасшедшим."],
    ["variant25.docx", "цвет символов", "Windows-1251",
     "Ячмень у соседа вкуснее риса дома."],
]


_VARIANT_15_LISTING = """\
$ steganography text-format-decode detect \\
    -f resources/steganographic_concealment/variants/variant15.docx

+-------------------------+-----------------------------------------+
|                Анализ контейнера variant15.docx                   |
+-------------------------+-----------------------------------------+
| Поле                    | Значение                                |
+-------------------------+-----------------------------------------+
| Файл                    | .../variants/variant15.docx             |
| Параметр форматирования | размер шрифта                           |
| Атрибут docx            | w:size                                  |
| Значение для 0          | 28                                      |
| Значение для 1          | 29                                      |
| Кодировка               | cp866                                   |
| Длина битовой строки    | 264                                     |
| Сообщение               | Ветер дует, но горы не двигаются.       |
+-------------------------+-----------------------------------------+
"""


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
                weight = self._confidence(text, score, encoding)
                candidates.append((weight, DecodedMessage(...)))
        return max(candidates, key=lambda x: x[0])[1] if candidates else None
'''


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
        "Программа разделена на слои domain / application / infrastructure / "
        "presentation с инжектом зависимостей через dishka. Кодировки и общие "
        "параметры форматирования вынесены в domain/common, что позволит ПР2 "
        "переиспользовать их без перекрёстных зависимостей.",
    )
    for bullet in _ARCH_BULLETS:
        add_para(doc, "• " + bullet, indent=False)

    add_heading(doc, "5. Ключевые фрагменты кода", level=2)
    add_label(doc, "Листинг 1 — детектор метода форматирования")
    add_listing(doc, _DETECTOR_LISTING)
    add_label(doc, "Листинг 2 — декодер с языковым скорингом")
    add_listing(doc, _DECODER_LISTING)

    add_page_break(doc)
    add_heading(doc, "6. Результаты прогона", level=2)
    add_para(
        doc,
        "Программа применена ко всем 25 файлам variantNN.docx, "
        "предоставленным преподавателем. 24 контейнера успешно декодированы "
        "(параметр, кодировка и сообщение приведены ниже); один файл "
        "(variant03.docx) содержит наложение сокрытия и декоративного "
        "форматирования стиха, и в осмысленный текст не разбирается.",
    )
    add_table_simple(
        doc,
        [_RESULTS_HEADER, *_RESULTS_ROWS],
        caption=(
            "Таблица 1 — Параметры сокрытия и расшифрованные пословицы "
            "по 25 контейнерам"
        ),
    )

    add_heading(doc, "7. Демонстрация работы CLI (вариант 15)", level=2)
    add_listing(doc, _VARIANT_15_LISTING, caption="Листинг 3 — вывод CLI")

    add_heading(doc, "8. Вывод")
    add_para(
        doc,
        "В рамках практической работы реализован детектор стеганографического "
        "сокрытия в текстовых docx-документах, поддерживающий пять параметров "
        "форматирования и пять кодировок. На контрольном наборе из 25 "
        "контейнеров правильное сообщение восстановлено в 24 случаях; "
        "качество обеспечивается весовой моделью кандидатов, учитывающей "
        "длину результата, априорный штраф для МТК-2 (склонной выдавать "
        "псевдо-кириллический шум) и сходство распределения букв с эталоном "
        "русского языка.",
    )

    save(doc, _OUTPUT)
    print(f"Отчёт сохранён: {_OUTPUT}")


if __name__ == "__main__":
    _build()
