"""Собрать отчёт ЛР3 в DOCX и PDF по результатам проверок."""

import html
import re
from importlib.metadata import version
from pathlib import Path
from tempfile import TemporaryDirectory

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from playwright.sync_api import sync_playwright

DOCS = Path(__file__).resolve().parents[1] / "docs"
NAME = "Ковалев Д.П. ВКБ53 ЛР3"
TITLE = "Middleware для авторизации пользователей (сессии, cookies, SQLAlchemy)"


class Report:
    def __init__(self) -> None:
        self.doc = Document()
        self.parts: list[str] = []
        self.doc.core_properties.author = "Ковалев Данил Петрович"
        self.doc.core_properties.title = f"Лабораторная работа № 3. {TITLE}"
        self.doc.core_properties.subject = "Разработка защищённых Web-ресурсов"
        section = self.doc.sections[0]
        section.page_width, section.page_height = Cm(21), Cm(29.7)
        section.top_margin, section.bottom_margin = Cm(2), Cm(2)
        section.left_margin, section.right_margin = Cm(3), Cm(1.5)
        section.different_first_page_header_footer = True
        normal = self.doc.styles["Normal"]
        normal.font.name, normal.font.size = "Times New Roman", Pt(14)
        normal.paragraph_format.line_spacing = 1.35
        normal.paragraph_format.first_line_indent = Cm(1.25)
        normal.paragraph_format.space_after = Pt(6)
        for name in ("Heading 1", "Heading 2"):
            style = self.doc.styles[name]
            style.font.name, style.font.size = "Times New Roman", Pt(14)
            style.font.color.rgb = RGBColor(0, 0, 0)
            style.paragraph_format.first_line_indent = Cm(0)
        footer = section.footer.paragraphs[0]
        footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
        footer.paragraph_format.first_line_indent = Cm(0)
        page = OxmlElement("w:fldSimple")
        page.set(qn("w:instr"), "PAGE")
        footer._p.append(page)

    def cover(self) -> None:
        self.parts.append('<div class="cover">')
        lines = (
            (
                "МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ",
                "center",
                0,
            ),
            ("ФГБОУ ВО «Донской государственный технический университет»", "center", 0),
            ("Факультет «Информатика и вычислительная техника»", "center", 0),
            ("Кафедра «Кибербезопасность информационных систем»", "center", 0),
            ("ОТЧЁТ", "center", 62),
            ("по лабораторной работе № 3", "center", 0),
            ("по дисциплине «Разработка защищённых Web-ресурсов»", "center", 0),
            (f"«{TITLE}»", "center", 0),
            ("Выполнил обучающийся группы ВКБ53", "right", 54),
            ("Ковалев Данил Петрович", "right", 0),
            ("Проверил Ковальчик Р. В.", "right", 0),
            ("Ростов-на-Дону, 2026", "center", 65),
        )
        for text, align, space in lines:
            p = self.doc.add_paragraph(text)
            p.alignment = (
                WD_ALIGN_PARAGRAPH.CENTER
                if align == "center"
                else WD_ALIGN_PARAGRAPH.RIGHT
            )
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.line_spacing = 1.08
            p.paragraph_format.space_before = Pt(space)
            p.paragraph_format.space_after = Pt(8)
            if text == "ОТЧЁТ":
                p.runs[0].bold = True
            self.parts.append(
                f'<p class="{align}" style="margin-top:{space}pt">{html.escape(text)}</p>'
            )
        self.parts.append("</div>")
        self.doc.add_page_break()

    def heading(self, text: str, level: int = 1) -> None:
        self.doc.add_heading(text, level=level)
        tag = f"h{level + 1}"
        self.parts.append(f"<{tag}>{html.escape(text)}</{tag}>")

    def paragraph(self, text: str) -> None:
        p = self.doc.add_paragraph(text)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        self.parts.append(f'<p class="text">{html.escape(text)}</p>')

    def code(self, text: str) -> None:
        p = self.doc.add_paragraph()
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.line_spacing = 1.1
        run = p.add_run(text)
        run.font.name, run.font.size = "Courier New", Pt(10)
        self.parts.append(f"<pre>{html.escape(text)}</pre>")

    def table(self, header: tuple[str, ...], rows: tuple[tuple[str, ...], ...]) -> None:
        table = self.doc.add_table(rows=0, cols=len(header))
        table.style = "Table Grid"
        body = []
        for index, columns in enumerate((header, *rows)):
            row = table.add_row()
            row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
            if index == 0:
                row._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))
            for cell, content in zip(row.cells, columns, strict=True):
                p = cell.paragraphs[0]
                p.paragraph_format.first_line_indent = Cm(0)
                p.paragraph_format.line_spacing = 1.1
                run = p.add_run(content)
                run.font.size, run.bold = Pt(11), index == 0
            tag = "th" if index == 0 else "td"
            cells = "".join(f"<{tag}>{html.escape(x)}</{tag}>" for x in columns)
            body.append(f"<tr>{cells}</tr>")
        self.parts.append(
            f"<table><thead>{body[0]}</thead><tbody>{''.join(body[1:])}</tbody></table>"
        )

    def picture(self, filename: str, caption: str) -> None:
        path = DOCS / "screenshots" / filename
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.keep_with_next = True
        p.add_run().add_picture(str(path), width=Cm(15.3))
        c = self.doc.add_paragraph(caption)
        c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        c.paragraph_format.first_line_indent = Cm(0)
        c.runs[0].font.size = Pt(11)
        self.parts.append(
            f'<figure><img src="{path.as_uri()}" alt="{html.escape(caption)}">'
            f"<figcaption>{html.escape(caption)}</figcaption></figure>"
        )

    def save(self) -> None:
        self.doc.save(DOCS / f"{NAME}.docx")
        css = """
        @page { size:A4; margin:20mm 15mm 20mm 30mm; @bottom-center { content:counter(page); } }
        @page :first { @bottom-center { content:none; } }
        * { box-sizing:border-box; }
        body { font:14pt/1.35 'Times New Roman',serif; color:#000; }
        p { margin:0 0 6pt; orphans:3; widows:3; }
        p.text { text-align:justify; text-indent:1.25cm; }
        h2,h3 { break-after:avoid; font-size:14pt; line-height:1.25; margin:16pt 0 8pt; }
        .cover { break-after:page; line-height:1.08; }
        .cover p { margin:0 0 8pt; }
        .cover .center { text-align:center; }
        .cover .right { text-align:right; }
        .cover p:nth-child(5) { font-weight:bold; }
        pre { font:10pt/1.1 'Courier New',monospace; white-space:pre-wrap; break-inside:avoid; }
        table { width:100%; border-collapse:collapse; margin:10pt 0; font:11pt/1.2 'Times New Roman',serif; }
        th,td { padding:5pt; border:1px solid; text-align:left; vertical-align:top; }
        tr { break-inside:avoid; }
        figure { margin:8pt 0 12pt; text-align:center; break-inside:avoid; }
        img { display:block; max-width:15.3cm; max-height:17cm; margin:auto; }
        figcaption { margin-top:5pt; font-size:11pt; }
        """
        document = (
            '<!doctype html><html lang="ru"><meta charset="utf-8">'
            f"<title>ЛР3 · SecureDev</title><style>{css}</style><body>"
            + "\n".join(self.parts)
            + "</body></html>"
        )
        with TemporaryDirectory() as tmp, sync_playwright() as playwright:
            path = Path(tmp) / "report.html"
            path.write_text(document)
            browser = playwright.chromium.launch(channel="chrome", headless=True)
            page = browser.new_page()
            page.goto(path.as_uri(), wait_until="networkidle")
            assert page.locator("img").evaluate_all(
                "(images) => images.every(image => image.complete && image.naturalWidth > 0)"
            )
            page.pdf(
                path=DOCS / f"{NAME}.pdf",
                prefer_css_page_size=True,
                print_background=True,
            )
            browser.close()


def implementation(report: Report) -> None:
    report.heading("1. Цель и задание")
    report.paragraph(
        "Реализовать регистрацию, аутентификацию и авторизацию в SecureDev. "
        "Закрыть расчёт /tempr и сравнение /compare для гостей, сохранить email и хеш пароля "
        "в модели пользователя, перенести сессии в SQLite и удалять их через час."
    )
    versions = ", ".join(
        f"{name} {version(name)}"
        for name in ("Flask", "Werkzeug", "SQLAlchemy", "Alembic")
    )
    report.paragraph(
        f"Использованы Python 3.14, {versions} и SQLite. Из ЛР2 перенесены "
        "справочная таблица, формула ТТГ, диапазоны входных данных, журнал и шаблоны."
    )
    report.heading("2. Реализация")
    report.heading("2.1. Учётные записи и миграции", 2)
    report.paragraph(
        "Миграция 0001 создаёт users с уникальными именем и email. Миграция 0002 создаёт "
        "sessions. SQLAlchemy связывает таблицы внешним ключом с каскадным удалением. "
        "Индекс по created_at нужен для поиска просроченных записей."
    )
    report.table(
        ("Таблица", "Поля и назначение"),
        (
            (
                "users",
                "id — первичный ключ, username — имя, email — адрес, password_hash — хеш",
            ),
            (
                "sessions",
                "session_id — хеш идентификатора, user_id — связь с users, created_at — время UTC",
            ),
        ),
    )
    report.paragraph(
        "Форма регистрации проверяет имя, синтаксис email, длину пароля от 12 до 128 "
        "символов и совпадение подтверждения. Пробелы пароля сохраняются при обработке. "
        "Werkzeug сохраняет PBKDF2-HMAC-SHA-256 с 1 000 000 итераций и уникальной случайной "
        "солью. Пользователь и его первая сессия создаются одной транзакцией."
    )
    report.heading("2.2. Вход, проверка доступа и выход", 2)
    report.paragraph(
        "Успешный вход проверяет хеш через check_password_hash(), выдаёт новый случайный "
        "идентификатор длиной 256 бит и сохраняет его SHA-256 в БД. Flask подписывает cookie "
        "с идентификатором и признаком постоянной сессии. Для следующих запросов "
        "браузер автоматически передаёт эту cookie."
    )
    report.paragraph(
        "Хук before_request читает идентификатор из проверенной Flask cookie. Хранилище "
        "удаляет строки с created_at ≤ UTC now − 1 час, затем по хешу идентификатора "
        "находит действующий сеанс и связанную запись users. Хук помещает id и имя "
        "в g.current_user на время запроса."
    )
    report.paragraph(
        "Белый список включает главную, вход, регистрацию и публичную статику. "
        "Гость с закрытого маршрута получает HTTP 302 и Location: /login. "
        "POST /logout с токеном формы удаляет запись текущего сеанса, очищает cookie "
        "и перенаправляет на главную. Предел в один час считается от входа."
    )
    report.heading("2.3. Расчёт и сравнение", 2)
    report.paragraph(
        "Обе формы применяют формулу и диапазоны из ЛР2. /tempr выводит ТТГ и записывает "
        "расчёт с комментарием в журнал. /compare принимает два режима, выводит две "
        "температуры и разницу «режим 2 − режим 1». При неверных данных форма сохраняет "
        "введённые значения и возвращает HTTP 400."
    )
    report.code("Тг = 2405 + 0,75 · (Тд − 1200) − 5,40 · Wд + 43 · (w − 21) − 52 · Vпг")


def verification(report: Report) -> None:
    report.heading("3. Проверка работы")
    report.paragraph(
        "Для локального запуска зависимости устанавливаются по uv.lock. "
        "Перед применением миграций задаётся случайный SECRET_KEY, сгенерированный "
        "через secrets.token_hex(32). Команды выполняются из каталога ЛР3."
    )
    report.code(
        "uv sync --locked\n"
        "uv run alembic upgrade head\n"
        "uv run blast-furnace run --host 127.0.0.1 --port 5003"
    )
    report.paragraph(
        "Сценарий выполнен в Google Chrome на локальном HTTP. Сначала гость открывает "
        "/tempr и /compare, в обоих случаях браузер получает HTTP 302 и показывает форму входа "
        "со стилями. После регистрации с email браузер возвращается на главную, где "
        "в меню отображаются имя пользователя, обе расчётные страницы и кнопка выхода."
    )
    report.picture(
        "01-login.png", "Рисунок 1 — Форма входа после перехода с закрытого маршрута"
    )
    report.picture("02-register.png", "Рисунок 2 — Регистрация с полем электронной почты")
    report.paragraph(
        "Для первого режима заданы 1000 °C, 10 г/м³, 21 % и 0 м³/100 м³. "
        "При расчёте получено 2201,0 °C. Для второго режима заданы 1200 °C, 15 г/м³, "
        "25 % и 8 м³/100 м³, результат 2080,0 °C. Разность составила −121,0 °C."
    )
    report.picture("03-tempr.png", "Рисунок 3 — Результат расчёта ТТГ")
    report.picture("04-compare.png", "Рисунок 4 — Сравнение режимов и разница температур")
    report.paragraph(
        "После выхода браузер удалил cookie. Прямое обращение к /tempr снова открыло "
        "форму входа. При ошибочном пароле сервер вернул HTTP 401 с сообщением "
        "«Неверное имя или пароль.» Повторный вход с верным паролем открыл расчётные страницы."
    )
    report.picture("05-bad-login.png", "Рисунок 5 — Общее сообщение при неверном пароле")
    log = (DOCS / "verification.txt").read_text()
    count = re.search(r"(\d+) passed", log)
    coverage = re.search(r"^TOTAL\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+%)", log, re.MULTILINE)
    assert count is not None and coverage is not None
    report.paragraph(
        f"Pytest подтвердил прохождение {count[1]} тестов, суммарное покрытие составило "
        f"{coverage[1]}. Проверены миграции, применение уникальных ограничений, повторный "
        "вход, токены форм, подпись cookie, сохранение сессии при перезапуске и удаление "
        "просроченной записи. В тесте с подменой часов сессия действовала на 59-й минуте "
        "и была удалена при запросе через час. Более новая сессия сохранилась."
    )
    report.heading("4. Содержимое cookie и подготовка к эксплуатации")
    report.paragraph(
        "В базовом примере методички Flask помещает user_id и username в подписанную "
        "клиентскую сессию. Полезная нагрузка, отметка времени и подпись образуют cookie. "
        "Кодировка Base64 доступна для чтения, а подпись связывает полезную нагрузку "
        "с SECRET_KEY."
    )
    report.code('{"user_id":1, "username":"anna"}')
    report.paragraph(
        "В Chrome атрибуты локальной cookie можно увидеть через DevTools → Application → "
        "Cookies. В итоговой версии Playwright прочитал те же атрибуты и поля. Значение "
        "идентификатора скрыто в отчёте."
    )
    report.code('{"session_id":"[скрыт]", "_permanent":true}')
    report.paragraph(
        "В локальном HTTP наблюдались HttpOnly и SameSite=Lax, а Secure включается "
        "на HTTPS установкой SESSION_COOKIE_SECURE=1. Тест повреждённой подписи подтвердил "
        "перенаправление на /login. Данные пользователя восстановлены из SQLite после "
        "проверки подписи, срока и наличия записи сеанса."
    )
    report.paragraph(
        "Приложение читает секрет из окружения и отключает кэширование страниц с формами. "
        "POST-запросы проверяют связанный с браузером CSRF-токен. Журнал расположен вне "
        "публичной статики, переводы строк экранируются, пользовательские значения в HTML "
        "обрабатываются автоэкранированием Jinja."
    )
    report.paragraph(
        "Для размещения приложения нужны HTTPS, флаг Secure, WSGI-сервер с отключённым "
        "отладчиком, закрытое хранилище секретов, ограничение частоты входа и резервные "
        "копии БД с ограниченным доступом. Непрерывную очистку без входящих запросов "
        "можно вынести в планировщик. При нескольких экземплярах нужно общее хранилище "
        "сессий и один ключ подписи для всех экземпляров."
    )


QUESTIONS = (
    (
        "Почему HTTP называют протоколом без состояния?",
        "Каждый запрос содержит данные, нужные для его обработки. Узнавание браузера между запросами обеспечивает приложение через cookie.",
    ),
    (
        "Чем аутентификация отличается от авторизации?",
        "/login устанавливает личность по имени и паролю. Middleware проверяет право этой учётной записи открыть /tempr и /compare.",
    ),
    (
        "Где хранятся данные сессии при двух подходах?",
        "Подписанная клиентская сессия Flask находится в cookie браузера. В серверной реализации учётные данные сеанса находятся в SQLite, браузер хранит cookie с идентификатором.",
    ),
    (
        "Чем подпись отличается от шифрования?",
        "Шифрование ограничивает чтение содержимого. Подпись удостоверяет целостность и знание ключа подписавшей стороной. Полезную нагрузку Flask можно прочитать, а сервер принимает изменения только с корректной подписью.",
    ),
    (
        "Зачем нужен SECRET_KEY?",
        "Flask использует ключ для подписи и её проверки. Утечка позволяет подписывать произвольное содержимое, поэтому требуется сменить ключ. Серверная реализация дополнительно требует живую запись сессии в БД.",
    ),
    (
        "Что происходит при краже cookie и при выходе?",
        "До истечения срока копия действующей cookie даёт доступ от имени пользователя. В базовой схеме Flask выход удаляет cookie в текущем браузере, копия остаётся действительной. В итоговой схеме выход отзывает запись в БД, после чего копия теряет доступ.",
    ),
    (
        "Зачем нужны HttpOnly, Secure и SameSite?",
        "HttpOnly скрывает cookie от JavaScript страницы, Secure ограничивает её передачу защищённым соединением, SameSite ограничивает отправку при межсайтовых запросах.",
    ),
    (
        "Почему для паролей применён PBKDF2, а не простой SHA-256?",
        "Открытый пароль даёт немедленный доступ при утечке БД. Быстрый SHA-256 удешевляет перебор вариантов. PBKDF2 замедляет каждую проверку за счёт многократных итераций.",
    ),
    (
        "Что такое соль и где она находится в хеше?",
        "Это случайное значение для каждой записи. Оно даёт разные хеши одинаковых паролей и мешает использовать общую таблицу готовых хешей. Werkzeug хранит соль между первым и вторым символами $ в строке хеша.",
    ),
    (
        "Почему условие в Jinja не защищает маршрут?",
        "Условие меняет меню, а прямой HTTP-запрос обрабатывается по правилам маршрутизации. Доступ проверяет серверный хук перед вызовом обработчика.",
    ),
    (
        "Что происходит после возвращения None или redirect() из before_request?",
        "После None Flask продолжает обработку запроса. Возвращённый redirect превращается в ответ, и обработчик маршрута пропускается.",
    ),
    (
        "Зачем используются белый список и исключение для /static/?",
        "Новые страницы по умолчанию требуют действующую сессию. Исключение даёт гостю CSS для страниц входа и регистрации.",
    ),
)


def main() -> None:
    report = Report()
    report.cover()
    implementation(report)
    verification(report)
    report.heading("5. Контрольные вопросы")
    for index, (question, answer) in enumerate(QUESTIONS, start=1):
        report.heading(f"{index}. {question}", 2)
        report.paragraph(answer)
    report.heading("6. Вывод")
    report.paragraph(
        "В SecureDev реализованы регистрация с email, вход, выход и защита обоих "
        "расчётных маршрутов. Серверные сессии хранятся в SQLite, действуют один час "
        "и отзываются при выходе. Результаты расчётов и проверки в браузере "
        "соответствуют заданию."
    )
    report.paragraph(
        "Источник задания — методические материалы «Middleware для авторизации "
        "пользователей (Сессии, Cookies, SQLAlchemy)» и расчётная формула ЛР2."
    )
    report.save()


if __name__ == "__main__":
    main()
