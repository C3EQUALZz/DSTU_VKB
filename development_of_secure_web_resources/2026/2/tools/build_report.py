"""Создать отчёт ЛР2 в DOCX и PDF из одних материалов и реальных снимков."""

import html
import re
import struct
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
NAME = "Ковалев Д.П. ВКБ53 ЛР2"


class Report:
    def __init__(self) -> None:
        self.doc = Document()
        self.parts: list[str] = []
        self.doc.core_properties.author = "Ковалев Данил Петрович"
        self.doc.core_properties.title = (
            "Лабораторная работа № 2. Разработка страницы расчёта температуры"
        )
        self.doc.core_properties.subject = "Разработка защищённых Web-ресурсов"
        section = self.doc.sections[0]
        section.page_width, section.page_height = Cm(21), Cm(29.7)
        section.top_margin, section.bottom_margin = Cm(2), Cm(2)
        section.left_margin, section.right_margin = Cm(3), Cm(1.5)
        section.different_first_page_header_footer = True
        normal = self.doc.styles["Normal"]
        normal.font.name, normal.font.size = "Times New Roman", Pt(14)
        normal.paragraph_format.line_spacing = 1.5
        normal.paragraph_format.first_line_indent = Cm(1.25)
        normal.paragraph_format.space_after = Pt(6)
        for name in ("Heading 1", "Heading 2"):
            style = self.doc.styles[name]
            style.font.name, style.font.size = "Times New Roman", Pt(14)
            style.font.color.rgb = RGBColor(0, 0, 0)
            style.paragraph_format.first_line_indent = Cm(0)
            style.paragraph_format.space_after = Pt(12)
        footer = section.footer.paragraphs[0]
        footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
        footer.paragraph_format.first_line_indent = Cm(0)
        field = OxmlElement("w:fldSimple")
        field.set(qn("w:instr"), "PAGE")
        footer._p.append(field)

    def paragraph(self, text: str, *, center: bool = False) -> None:
        p = self.doc.add_paragraph(text)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.JUSTIFY
        if center:
            p.paragraph_format.first_line_indent = Cm(0)
        self.parts.append(
            f'<p class="{"center" if center else "text"}">{html.escape(text)}</p>'
        )

    def heading(self, text: str) -> None:
        p = self.doc.add_heading(text, level=1)
        p.paragraph_format.page_break_before = True
        self.parts.append(f"<h2>{html.escape(text)}</h2>")

    def code(self, text: str, caption: str) -> None:
        p = self.doc.add_paragraph()
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.line_spacing = 1
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text.rstrip())
        run.font.name, run.font.size = "Courier New", Pt(8)
        self.parts.append(f"<pre>{html.escape(text.rstrip())}</pre>")
        self.paragraph(caption, center=True)

    def source(self, path: str, caption: str) -> None:
        self.code((ROOT / "src" / "blast_furnace" / path).read_text(), caption)

    def table(self, headers: tuple[str, ...], rows: list[tuple[str, ...]]) -> None:
        table = self.doc.add_table(rows=1, cols=len(headers))
        table.style = "Table Grid"
        for cell, text in zip(table.rows[0].cells, headers, strict=True):
            cell.text = text
        for row in rows:
            cells = table.add_row().cells
            for cell, text in zip(cells, row, strict=True):
                cell.text = text
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    p.paragraph_format.first_line_indent = Cm(0)
                    p.paragraph_format.line_spacing = 1.1
                    for run in p.runs:
                        run.font.size = Pt(11)
        self.parts.append(
            "<table><thead><tr>"
            + "".join(f"<th>{html.escape(x)}</th>" for x in headers)
            + "</tr></thead><tbody>"
            + "".join(
                "<tr>" + "".join(f"<td>{html.escape(x)}</td>" for x in row) + "</tr>"
                for row in rows
            )
            + "</tbody></table>"
        )

    def picture(self, filename: str, caption: str, *, max_height: float = 17) -> None:
        path = DOCS / "screenshots" / filename
        width, height = struct.unpack(">II", path.read_bytes()[16:24])
        width_cm = min(15.5, max_height * width / height)
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.line_spacing = 1
        p.add_run().add_picture(str(path), width=Cm(width_cm))
        self.parts.append(
            f'<figure><img src="{path.as_uri()}" style="width:{width_cm}cm" alt="{html.escape(caption)}"></figure>'
        )
        self.paragraph(caption, center=True)

    def cover(self) -> None:
        self.parts.append('<div class="cover">')
        for text in (
            "МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ",
            "ФГБОУ ВО «Донской государственный технический университет»",
            "Факультет «Информатика и вычислительная техника»",
            "Кафедра «Кибербезопасность информационных систем»",
            "",
            "",
            "ОТЧЁТ",
            "по лабораторной работе № 2",
            "по дисциплине «Разработка защищённых Web-ресурсов»",
            "«Разработка Web-приложения для расчёта теоретической температуры горения»",
            "Разработка страницы расчёта температуры",
            "",
        ):
            p = self.doc.add_paragraph(text)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.line_spacing = 1.1
            p.paragraph_format.space_after = Pt(10)
            if text in ("ОТЧЁТ", "по лабораторной работе № 2"):
                p.runs[0].bold = True
            self.parts.append(f"<p>{html.escape(text) or '&nbsp;'}</p>")
        for text in (
            "Выполнил: обучающийся гр. ВКБ53",
            "Ковалев Данил Петрович",
            "Проверил: Ковальчик Р. В.",
        ):
            p = self.doc.add_paragraph(text)
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.line_spacing = 1
            self.parts.append(f'<p class="right">{html.escape(text)}</p>')
        self.paragraph("Ростов-на-Дону, 2026", center=True)
        self.parts.append("</div>")

    def save(self) -> None:
        DOCS.mkdir(exist_ok=True)
        self.doc.save(DOCS / f"{NAME}.docx")
        css = """
        @page { size:A4; margin:20mm 15mm 20mm 30mm; }
        * { box-sizing:border-box; }
        body { font-family:'Times New Roman',serif; font-size:14pt; line-height:1.5; color:#000; }
        p { margin:0 0 6pt; orphans:3; widows:3; }
        p.text { text-align:justify; text-indent:1.25cm; }
        p.center { text-align:center; }
        h2 { break-before:page; font-size:14pt; line-height:1.4; margin:0 0 12pt; }
        h2, th { font-weight:bold; }
        .cover { text-align:center; line-height:1.1; }
        .cover p { margin-bottom:10pt; }
        .cover .right { text-align:right; }
        .cover .center { margin-top:25pt; }
        pre { font-family:'Courier New',monospace; font-size:8pt; line-height:1.1; white-space:pre-wrap; overflow-wrap:anywhere; margin:8pt 0; }
        table { width:100%; border-collapse:collapse; margin:10pt 0; font-size:11pt; line-height:1.2; }
        th,td { border:1px solid black; padding:6pt; text-align:left; vertical-align:top; }
        tr { break-inside:avoid; }
        figure { margin:8pt 0; text-align:center; break-inside:avoid; }
        img { max-height:17cm; object-fit:contain; }
        """
        report_html = DOCS / "report.html"
        report_html.write_text(
            '<!doctype html><html lang="ru"><meta charset="utf-8"><title>Отчёт ЛР2</title><style>'
            + css
            + "</style><body>"
            + "\n".join(self.parts)
            + "</body></html>",
            encoding="utf-8",
        )
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(channel="chrome", headless=True)
            page = browser.new_page()
            page.goto(report_html.as_uri(), wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            page.pdf(
                path=str(DOCS / f"{NAME}.pdf"),
                format="A4",
                print_background=True,
                prefer_css_page_size=True,
                display_header_footer=True,
                header_template="<span></span>",
                footer_template='<div style="font-family:Times New Roman;font-size:10pt;width:100%;text-align:center"><span class="pageNumber"></span></div>',
            )
            browser.close()
        print(DOCS / f"{NAME}.docx")
        print(DOCS / f"{NAME}.pdf")


def main() -> None:
    r = Report()
    r.cover()
    r.heading("1. Цель работы и постановка задачи")
    r.paragraph(
        "Цель работы — дополнить веб-приложение, созданное в лабораторной работе № 1, второй страницей с формой ввода параметров дутья, выводом результата расчёта теоретической температуры горения и сохранением выполненных расчётов в файл."
    )
    r.paragraph(
        "По заданию необходимо вынести формулу в отдельный Python-модуль, реализовать шаблон tempr.html и обработку GET/POST на маршруте /tempr, добавить необязательный комментарий и журнал static/calc_log.txt. Правильность формулы проверяется по четырём контрольным наборам из методических указаний. В завершение требуется ответить на пять контрольных вопросов."
    )
    r.paragraph(
        "В качестве основы использован проект лабораторной № 1 из соседнего каталога 2026/1. Его исходники и конфигурации перенесены в каталог 2026/2. Сохранены справочная таблица главной страницы, семантическая разметка, оформление, src-структура и внедрение зависимостей Dishka."
    )
    r.paragraph(
        "Работа выполнена локально с Python 3.14.3 и Flask 3.1.3. Зависимости установлены через uv в отдельное окружение .venv. Проверка страниц выполнена в Google Chrome через Playwright по адресу http://127.0.0.1:5002. Docker не собирался и не запускался."
    )
    r.code(
        "uv sync --frozen --group report\nuv run blast-furnace run --host 127.0.0.1 --port 5002",
        "Листинг 1 — подготовка окружения и локальный запуск",
    )
    r.heading("2. Предметная область и расчётная формула")
    r.paragraph(
        "Теоретическая температура горения — расчётная температура продуктов сгорания кокса в фурменном очаге доменной печи при условии, что выделенное тепло полностью расходуется на их нагрев. В модели не учитываются теплопотери и теплообмен с шихтой. Для оперативной оценки применяется эмпирическая зависимость из методических указаний."
    )
    r.paragraph(
        "Тг = 2405 + 0,75 · (Тд − 1200) − 5,40 · Wд + 43,00 · (w − 21) − 52,00 · Vпг.",
        center=True,
    )
    r.table(
        ("Параметр", "Обозначение", "Единица", "Диапазон"),
        [
            ("Температура дутья", "Тд", "°C", "900–1300"),
            ("Влажность дутья", "Wд", "г/м³", "1–40"),
            ("Содержание кислорода", "w", "%", "21–35"),
            ("Расход природного газа", "Vпг", "м³/100 м³ дутья", "0–15"),
        ],
    )
    r.paragraph(
        "Горячее дутьё повышает температуру, поскольку вносит дополнительное тепло. Влага и природный газ понижают её из-за эндотермических процессов разложения. Обогащение кислородом повышает температуру: уменьшается доля балластного азота, на нагрев которого расходуется тепло."
    )
    r.table(
        ("№", "Тд", "Wд", "w", "Vпг", "Тг, °C"),
        [
            ("1", "1000", "10", "21", "0", "2201,0"),
            ("2", "1200", "15", "25", "8", "2080,0"),
            ("3", "1100", "20", "23", "5", "2048,0"),
            ("4", "1300", "1", "35", "0", "3076,6"),
        ],
    )
    r.paragraph(
        "Например, для первого набора: Тг = 2405 + 0,75 · (1000 − 1200) − 5,4 · 10 + 43 · (21 − 21) − 52 · 0 = 2405 − 150 − 54 = 2201,0 °C. Все четыре результата совпали с контрольными значениями."
    )
    r.heading("3. Структура проекта и бизнес-логика")
    r.paragraph(
        "Формула размещена в domain/services/calculations.py. Пакет services с пустым __init__.py соответствует требованию методички; он находится внутри domain для сохранения архитектуры первой лабораторной. Функция не зависит от Flask, HTML и файловой системы, поэтому проверяется отдельно от веб-сервера."
    )
    r.code(
        "src/blast_furnace/\n  app.py                         WSGI-точка входа\n  domain/\n    reference.py                 справочник из ЛР1\n    temperature.py               параметры и диапазоны\n    services/\n      __init__.py                пустой файл пакета\n      calculations.py            формула calculate_ttg\n  application/\n    get_blast_reference.py        справочник\n    calculate_temperature.py     расчёт и порт журнала\n  infrastructure/\n    calculation_log.py           запись UTF-8 файла\n  presentation/http/\n    routes.py                    обработчики HTTP\n    templates/                   base, index, tempr\n    static/styles.css            оформление\n  setup/                         конфигурация и Dishka\nstatic/calc_log.txt              журнал, создаётся при расчёте\ntests/                           модульные и HTTP-тесты\ndocs/                            отчёт и подтверждения",
        "Листинг 2 — структура дополненного проекта",
    )
    r.source("domain/services/calculations.py", "Листинг 3 — независимая функция расчёта")
    r.paragraph(
        "Модель BlastParameters проверяет допустимые диапазоны и конечность чисел. Прикладной сценарий CalculateTemperature вызывает формулу и порт CalculationLog. Конкретный файловый адаптер подключается в setup через Dishka; внутренние слои не импортируют Flask или инфраструктуру."
    )
    r.heading("4. Обработка формы и передача результата")
    r.paragraph(
        "GET /tempr возвращает пустую форму. POST читает поля t_blast, humidity, oxygen, gas и comment из request.form. Числа преобразуются из строк в float, что позволяет вводить дробные значения. Запятая заменяется точкой. Ошибки преобразования и выхода за диапазон дают HTTP 400; введённые значения сохраняются в форме. Комментарий необязателен, его длина ограничена 500 символами."
    )
    r.source("presentation/http/routes.py", "Листинг 4 — контроллер страниц и расчёта")
    r.heading("5. HTML-форма и журнал расчётов")
    r.paragraph(
        "Шаблон tempr.html наследует base.html с блоками header, nav, main и footer. Каждое поле связано с label через id/for и имеет name для передачи в контроллер. Обязательные параметры имеют required и подсказки диапазонов. type=text и inputmode=decimal позволяют вводить десятичную запятую. Серверная проверка выполняется независимо от проверки браузера."
    )
    r.code(
        '<form action="{{ url_for(\'pages.temperature\') }}" method="POST">\n  <label for="t_blast">Температура дутья, °C</label>\n  <input type="text" inputmode="decimal" id="t_blast"\n         name="t_blast" value="{{ values.t_blast }}" required>\n  <!-- Аналогично: humidity, oxygen, gas -->\n  <label for="comment">Комментарий к расчёту</label>\n  <input type="text" id="comment" name="comment"\n         value="{{ values.comment }}" maxlength="500">\n  <button type="submit">Рассчитать</button>\n</form>\n{% if tempr is not none %}\n  <output>{{ \'%.1f\' | format(tempr) | replace(\'.\', \',\') }}</output> °C\n  <p>Комментарий: {{ values.comment or \'Не указан\' }}</p>\n{% endif %}',
        "Листинг 5 — сокращённый фрагмент формы и вывода результата",
    )
    r.paragraph(
        "Результат передаётся как tempr=result в render_template. Условие tempr is not none скрывает блок при первом открытии и корректно отличает отсутствие результата от числового нуля. Jinja автоматически экранирует комментарий и значения полей: введённые HTML-теги отображаются как текст."
    )
    r.paragraph(
        "В соответствии с заданием журнал ведётся в static/calc_log.txt. Режим a сохраняет предыдущие записи. Каждая строка содержит время с часовым поясом, четыре параметра, результат и комментарий. Каталог создаётся автоматически. Путь настраивается CALC_LOG_PATH. Файл журнала находится вне каталога статических ресурсов Blueprint и не доступен по HTTP."
    )
    r.heading("5.1. Реализация записи в файл")
    r.source("infrastructure/calculation_log.py", "Листинг 6 — файловый журнал расчётов")
    r.paragraph(
        "Блокировка fcntl предотвращает перемешивание строк при конкурентных записях в Linux/macOS. Переносы строк и разделители комментария экранируются для сохранения формата «одна запись — одна строка». Если файл недоступен, приложение возвращает HTTP 503 и сообщение об ошибке сохранения, не показывая успешный результат."
    )
    log_path = ROOT / "static" / "calc_log.txt"
    log_lines = log_path.read_text(encoding="utf-8").splitlines()[:4]
    r.code(
        "\n".join(log_lines), "Листинг 7 — реальные записи четырёх контрольных расчётов"
    )
    r.heading("6. Проверка формы в браузере")
    r.paragraph(
        "Из главной страницы выполнен переход по ссылке «Расчёт ТТГ». При первом открытии отображаются четыре обязательных числовых поля, необязательный комментарий и кнопка расчёта; блока результата нет."
    )
    r.picture("tempr-form.png", "Рисунок 1 — начальное состояние страницы расчёта ТТГ")
    r.heading("6.1. Результат контрольного расчёта")
    r.paragraph(
        "После отправки параметров Тд = 1000 °C, Wд = 10 г/м³, w = 21 %, Vпг = 0 получено 2201,0 °C. Введённые параметры и комментарий отображаются на странице, результат дописан в журнал."
    )
    r.picture(
        "tempr-result.png",
        "Рисунок 2 — первый контрольный расчёт и подтверждение сохранения",
    )
    r.heading("6.2. Обработка неверного ввода")
    r.paragraph(
        "Для проверки серверной валидации вместо температуры введено abc. Сервер вернул HTTP 400, показал сообщение «Температура дутья: введите число», сохранил остальные значения и не выполнил запись в журнал. Отдельно проверены ввод вне диапазонов, NaN, бесконечность и отсутствующие поля."
    )
    r.picture(
        "tempr-error.png",
        "Рисунок 3 — сообщение при вводе нечислового значения",
        max_height=14,
    )
    r.paragraph(
        "Дополнительно форма и главная страница проверены при ширине 390 px: горизонтальное переполнение отсутствует, расчёт выполняется. Снимки index-mobile.png и tempr-mobile.png находятся в docs/screenshots. Комментарий с тегом script отображён текстом, выполнение JavaScript не произошло."
    )
    r.heading("7. Автоматическая проверка")
    verification = (DOCS / "verification.txt").read_text()
    passed = re.search(r"(\d+) passed", verification)
    coverage = re.search(r"TOTAL\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+%)", verification)
    r.paragraph(
        "Выполнены модульные проверки формулы и физического смысла коэффициентов, интеграционные HTTP-тесты формы и журнала, проверки сохранённой главной страницы. Проверки работают с временными файлами и не изменяют пользовательский журнал. Дополнительно выполнены статические проверки и браузерный сценарий."
    )
    r.code(
        "uv run ruff format --check .\nuv run ruff check .\nuv run mypy\nuv run bandit -c pyproject.toml -r src\nuv run lint-imports\nuv run pytest --cov --cov-report=term-missing\nuv run --group report python tools/capture_pages.py",
        "Листинг 8 — команды проверки",
    )
    r.table(
        ("Проверка", "Фактический результат"),
        [
            (
                "pytest",
                f"{passed.group(1) if passed else 'См. протокол'} тестов пройдено",
            ),
            (
                "Покрытие исходников",
                coverage.group(1) if coverage else "См. docs/verification.txt",
            ),
            (
                "4 контрольных значения",
                "Совпали в модульных, HTTP- и браузерных проверках",
            ),
            ("Ruff / mypy", "Проверки пройдены"),
            ("Bandit", "Замечаний не обнаружено"),
            ("import-linter", "4 архитектурных контракта соблюдены"),
            (
                "Журнал",
                "Дописывание, создание каталога, экранирование переносов, ошибка записи",
            ),
            (
                "Chrome / Playwright",
                "Форма, расчёты, ошибка, экранирование, экран 390 px — успешно",
            ),
            ("Docker", "Сборка и запуск не выполнялись"),
        ],
    )
    r.paragraph(
        "Протокол команд сохранён в docs/verification.txt, результаты Chrome — в docs/browser-verification.txt. Непокрытые строки относятся к точкам запуска приложения; сама формула, валидация, HTTP-контроллер, сценарий расчёта и файловый адаптер покрыты тестами полностью."
    )
    r.heading("8. Ответы на контрольные вопросы")
    questions = [
        (
            "1. Чем GET отличается от POST и почему выбран POST?",
            "GET запрашивает представление ресурса; параметры обычно передаются в строке URL. POST передаёт данные в теле запроса для обработки. В приложении GET открывает форму без записи в журнал, а POST отправляет параметры, выполняет расчёт и сохраняет запись. POST не обеспечивает шифрование: для защиты передачи нужен HTTPS.",
        ),
        (
            "2. Как данные формы попадают в контроллер? Какой атрибут служит ключом?",
            "Браузер сериализует успешные элементы формы и отправляет их на URL из action методом POST. Flask предоставляет поля через request.form. Ключ — атрибут name, например request.form.get('t_blast'). Атрибут id нужен для связи с label, CSS и DOM и не определяет имя передаваемого параметра.",
        ),
        (
            "3. Почему данные приходят строками? Что будет без преобразования?",
            "В обычной HTML-форме значения передаются как текст в кодировке формы; числовой тип Python не сохраняется протоколом. Перед вычислением требуется int() либо float(). В данной работе float() поддерживает дроби. Если подставить строку в вычитание t_blast − 1200, Python вызовет TypeError. Некорректный текст вызывает ValueError при преобразовании; сервер обрабатывает эту ошибку и возвращает понятное сообщение.",
        ),
        (
            "4. Как значение передаётся в шаблон? Что делает {% if tempr %}?",
            "Контроллер вызывает render_template('tempr.html', tempr=result), а шаблон использует имя tempr. Конструкция {% if tempr %} выводит блок только при истинном значении и скрывает его при первом открытии. Для чисел она также скрывает нулевой результат, поэтому в реализации применено более точное условие {% if tempr is not none %}. Комментарий передаётся вместе со значениями формы и выводится с автоматическим экранированием Jinja.",
        ),
        (
            "5. Какие семантические теги использованы и как объясняются знаки коэффициентов?",
            "header содержит заголовок, nav — меню, main — основное содержимое, section — тематический раздел, footer — автора и номер работы. В форме используются form, fieldset, legend, label, input, button и output; в справочнике — table, caption, thead, tbody и th. Положительный коэффициент 0,75 отражает поступление тепла с горячим дутьём. Отрицательный −5,40 соответствует затратам тепла на влагу. Положительный +43 учитывает уменьшение доли балластного азота при обогащении кислородом выше 21 %. Отрицательный −52 связан с эндотермическим разложением метана.",
        ),
    ]
    for index, (question, answer) in enumerate(questions):
        if index == 3:
            r.heading("8.1. Ответы на вопросы 4–5")
        r.paragraph(question)
        r.paragraph(answer)
    r.heading("9. Вывод")
    r.paragraph(
        "В лабораторной работе № 2 завершена страница расчёта теоретической температуры горения. В проект первой лабораторной добавлены независимая функция расчёта, модель параметров с проверкой диапазонов, форма ввода и обработчик GET/POST, вывод результата и комментария, а также файловый журнал с дописыванием записей."
    )
    r.paragraph(
        "Все четыре контрольных значения из методических указаний воспроизведены. Работоспособность подтверждена автоматическими тестами, статическими проверками и сценариями в Chrome, включая мобильную ширину, неверный ввод и экранирование пользовательского комментария. Приложение проверено локально без сборки Docker."
    )
    r.paragraph("10. Использованные материалы")
    for text in (
        "1. ДГТУ. Лабораторная работа № 2 «Разработка Web-приложения для расчёта теоретической температуры горения». Разработка страницы расчёта температуры. Ростов-на-Дону, 2026. Предоставленный PDF, с. 2–9.",
        "2. Исходный проект и отчёт лабораторной работы № 1: каталог ../1. Ковалев Данил Петрович, ВКБ53.",
        "3. Исходные тексты приложения, тестов и браузерного сценария ЛР2; протоколы docs/verification.txt и docs/browser-verification.txt.",
    ):
        r.paragraph(text)
    r.save()


if __name__ == "__main__":
    main()
