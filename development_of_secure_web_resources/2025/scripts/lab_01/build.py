"""Отчёт по лаб. 1 — Знакомство с HTML (11 заданий)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from report_builder import (  # noqa: E402
    LabMeta,
    add_bullets,
    add_heading,
    add_image,
    add_listing,
    add_page_break,
    add_para,
    add_qa,
    add_table_simple,
    add_title_page,
    make_doc,
    save,
)

LAB_DIR = ROOT / "1"
SHOTS = ROOT / "docs" / "screenshots" / "lab_01"
SNIPS = ROOT / "docs" / "snippets" / "lab_01"


def read_html(name: str) -> str:
    return (LAB_DIR / name).read_text(encoding="utf-8")


def main() -> None:
    meta = LabMeta(
        number=1,
        title="Знакомство с HTML. Создание простых WEB-страниц",
    )
    doc = make_doc()
    add_title_page(doc, meta)
    add_page_break(doc)

    # === Тема и цель ===
    add_heading(doc, "Тема и цель работы")
    add_para(
        doc,
        "Тема: знакомство с языком разметки гипертекста HTML 5 — базовая "
        "структура документа, основные теги форматирования текста, "
        "списки, ссылки, изображения, таблицы, формы и поля ввода, "
        "семантическая разметка, встраивание медиа и iframe.",
    )
    add_para(
        doc,
        "Цель работы: освоить структуру HTML-документа и набор основных "
        "тегов (h1–h6, p, b/strong, i/em, u, ol/ul/li, a, img, table, "
        "form, input, audio/video, header/nav/main/article/aside/footer, "
        "iframe); научиться создавать корректные документы HTML 5 с "
        "указанием кодировки и языка, оформлять текст, списки, ссылки, "
        "изображения, таблицы и формы; познакомиться с семантической "
        "разметкой и встраиванием внешних ресурсов через iframe.",
    )

    # === Условие задания ===
    add_heading(doc, "Условие задания", level=2)
    add_para(
        doc,
        "Согласно методическим указаниям к лабораторной работе №1, "
        "требуется выполнить 11 индивидуальных заданий, каждое из "
        "которых демонстрирует определённую группу HTML-тегов:",
    )
    add_bullets(
        doc,
        [
            "Задание 1. Создать простую WEB-страницу с заголовком, "
            "текстом и горизонтальной линией.",
            "Задание 2. Продемонстрировать теги форматирования текста "
            "(жирный, курсив, подчёркнутый, верхний/нижний индексы, "
            "выделение и др.).",
            "Задание 3. Реализовать различные виды списков "
            "(маркированные, нумерованные, вложенные, с типами маркеров).",
            "Задание 4. Создать ссылки разных видов: на внешний сайт, "
            "с открытием в новой вкладке, на якорь, на скачивание файла.",
            "Задание 5. Разместить изображения с атрибутами src/alt/"
            "width/height/title и реализовать изображение-ссылку.",
            "Задание 6. Построить таблицу с заголовком (caption), "
            "разделением на thead/tbody, объединением ячеек "
            "(colspan/rowspan).",
            "Задание 7. Продемонстрировать тег <input> со всеми "
            "значениями атрибута type (text, password, email, number, "
            "date, color, range, checkbox, radio, file, submit и др.).",
            "Задание 8. Создать форму с использованием fieldset/legend, "
            "label, разнотипных полей ввода, textarea, select, кнопок "
            "submit/reset.",
            "Задание 9. Построить страницу с семантической разметкой: "
            "header, nav, main, article, aside, footer.",
            "Задание 10. Встроить аудио и видео через теги <audio>, "
            "<video> и <iframe> (YouTube, Vimeo).",
            "Задание 11. Встроить интерактивную карту через <iframe> "
            "(Google Maps embed).",
        ],
    )
    add_para(
        doc,
        "В качестве точки входа должен быть создан index.html со "
        "ссылками на все 11 страниц.",
    )

    # === Краткая теория ===
    add_page_break(doc)
    add_heading(doc, "Краткая теория")
    add_heading(doc, "Базовая структура HTML 5-документа", level=2)
    add_para(
        doc,
        "Минимально валидный документ HTML 5 содержит инструкцию "
        "DOCTYPE, корневой элемент <html> с атрибутом языка, секцию "
        "<head> с обязательным <title> и метатегом кодировки, и "
        "видимое содержимое в <body>:",
    )
    add_listing(
        doc,
        "<!DOCTYPE html>\n"
        "<html lang=\"ru\">\n"
        "<head>\n"
        "    <meta charset=\"UTF-8\">\n"
        "    <title>Заголовок вкладки</title>\n"
        "</head>\n"
        "<body>\n"
        "    <h1>Заголовок страницы</h1>\n"
        "    <p>Параграф текста.</p>\n"
        "</body>\n"
        "</html>",
        caption="Листинг 1 — каркас HTML 5-документа",
    )
    add_table_simple(
        doc,
        [
            ["Тег / атрибут", "Назначение"],
            ["<!DOCTYPE html>", "Объявление версии разметки (HTML 5)."],
            ["<html lang=\"ru\">", "Корневой элемент. lang помогает SEO и screen-readers."],
            ["<head>", "Метаинформация: кодировка, заголовок вкладки, ссылки на CSS."],
            ["<title>", "Обязательный тег внутри <head>: текст вкладки браузера."],
            ["<meta charset>", "Кодировка документа (UTF-8)."],
            ["<meta name=\"viewport\">", "Адаптация под мобильные устройства."],
            ["<body>", "Видимое содержимое страницы."],
        ],
        caption="Таблица 1 — обязательные элементы каркаса",
    )

    add_heading(doc, "Группы тегов, использованные в работе", level=2)
    add_table_simple(
        doc,
        [
            ["Группа", "Теги"],
            ["Заголовки", "h1, h2, h3, h4, h5, h6"],
            ["Блочное форматирование", "p, hr, br, blockquote, pre"],
            ["Строчное форматирование", "b/strong, i/em, u, small, mark, del/ins, sub/sup"],
            ["Списки", "ul, ol, li, dl/dt/dd"],
            ["Ссылки / медиа", "a, img, audio, video, source"],
            ["Таблицы", "table, caption, thead, tbody, tr, th, td (colspan, rowspan)"],
            ["Формы и ввод", "form, fieldset, legend, label, input, textarea, select, option, button"],
            ["Семантика HTML 5", "header, nav, main, article, aside, footer"],
            ["Встраивание", "iframe (YouTube, Vimeo, Google Maps)"],
        ],
        caption="Таблица 2 — теги, использованные в 11 заданиях",
    )

    # === Структура работы (index) ===
    add_page_break(doc)
    add_heading(doc, "Структура проекта и точка входа")
    add_para(
        doc,
        "Все 11 страниц собраны в единое содержание index.html — со "
        "ссылками на каждое задание. Структура каталога 1/ "
        "сгруппирована по номерам файлов:",
    )
    add_listing(
        doc,
        "1/\n"
        "├── ЛР1.pdf                # оригинал задания\n"
        "├── README.md\n"
        "├── index.html             # содержание со ссылками\n"
        "├── 01-simple-page.html\n"
        "├── 02-text-formatting.html\n"
        "├── 03-lists.html\n"
        "├── 04-links.html\n"
        "├── 05-images.html\n"
        "├── 06-tables.html\n"
        "├── 07-input-types.html\n"
        "├── 08-forms.html\n"
        "├── 09-semantic.html\n"
        "├── 10-audio-video.html\n"
        "├── 11-iframe.html\n"
        "└── assets/\n"
        "    ├── chrome.svg\n"
        "    └── example.pdf",
        caption="Листинг 2 — состав каталога 1/",
    )
    add_image(doc, SHOTS / "00_index.png", caption="Рисунок 1 — точка входа (index.html)")

    # === ПО ЗАДАНИЯМ ===
    tasks = [
        {
            "n": 1,
            "title": "Простая WEB-страница",
            "summary": (
                "Минимальная страница с заголовком первого уровня, "
                "горизонтальным разделителем (<hr>) и двумя параграфами. "
                "Демонстрирует базовый каркас HTML-документа: DOCTYPE, "
                "<html lang=\"ru\">, <head><title></head>, <body>."
            ),
            "tags": "h1, p, hr, title, meta charset",
            "shot": "01_simple_page.png",
            "snip": "01_simple_page.png",
        },
        {
            "n": 2,
            "title": "Форматирование текста",
            "summary": (
                "Страница демонстрирует строчные теги форматирования: "
                "<b>/<strong> — жирный, <i>/<em> — курсив, <u> — "
                "подчёркивание, <small> — мелкий текст, <mark> — "
                "выделение фона, <del>/<ins> — зачёркнутый/вставленный, "
                "<sub>/<sup> — нижний/верхний индексы. Каждый тег "
                "сопровождается подписью."
            ),
            "tags": "b, strong, i, em, u, small, mark, del, ins, sub, sup",
            "shot": "02_text_formatting.png",
            "snip": "02_text_formatting.png",
        },
        {
            "n": 3,
            "title": "Списки",
            "summary": (
                "Три вида списков: маркированный <ul>, нумерованный "
                "<ol> с атрибутом type, вложенные списки. На странице "
                "показаны различные стили маркеров (disc/circle/square, "
                "decimal/upper-roman/lower-alpha)."
            ),
            "tags": "ul, ol, li, type",
            "shot": "03_lists.png",
            "snip": "03_lists.png",
        },
        {
            "n": 4,
            "title": "Ссылки",
            "summary": (
                "Демонстрация всех видов ссылок: внешний переход на "
                "сайт, открытие в новой вкладке (target=\"_blank\" + "
                "rel=\"noopener\"), переход к якорю (#id) внутри "
                "страницы, ссылка-скачивание (download), ссылка на "
                "почту (mailto:) и телефон (tel:)."
            ),
            "tags": "a href, target=\"_blank\", #anchor, download, mailto, tel",
            "shot": "04_links.png",
            "snip": "04_links.png",
        },
        {
            "n": 5,
            "title": "Изображения",
            "summary": (
                "Размещены изображения с обязательным атрибутом alt "
                "(для доступности и SEO), заданными width/height (для "
                "корректного резервирования места при загрузке), "
                "подсказкой title. Реализован пример изображения-"
                "ссылки — <a><img></a>."
            ),
            "tags": "img src/alt/width/height/title, изображение-ссылка",
            "shot": "05_images.png",
            "snip": "05_images.png",
        },
        {
            "n": 6,
            "title": "Таблицы",
            "summary": (
                "Таблица с заголовком <caption>, разделением на "
                "<thead>/<tbody>, объединением ячеек по горизонтали "
                "(colspan) и вертикали (rowspan). Использованы "
                "теги-заголовки строк (<th>) и ячейки данных (<td>)."
            ),
            "tags": "table, caption, thead, tbody, tr, th, td, colspan, rowspan",
            "shot": "06_tables.png",
            "snip": "06_tables.png",
        },
        {
            "n": 7,
            "title": "Тег input — все типы",
            "summary": (
                "Полная демонстрационная таблица из 23 строк — по "
                "одному <input> для каждого значения атрибута type "
                "(text, password, email, url, tel, search, number, "
                "range, date, time, datetime-local, month, week, "
                "color, file, checkbox, radio, button, submit, reset, "
                "image, hidden, datetime — устаревший). Для каждого "
                "указано назначение и пример отображения в браузере."
            ),
            "tags": "input type=...",
            "shot": "07_input_types.png",
            "snip": "07_input_types.png",
        },
        {
            "n": 8,
            "title": "Формы",
            "summary": (
                "Учебная форма регистрации, сгруппированная в "
                "<fieldset> с подписями <legend>. Используются: "
                "однострочные поля <input>, многострочное <textarea>, "
                "выпадающий список <select>, чекбоксы, радиокнопки, "
                "ползунок range, поле даты, поле пароля, кнопки "
                "submit/reset. Все поля сопровождаются <label "
                "for=...> — корректная связка для accessibility."
            ),
            "tags": "form, fieldset, legend, label, input, textarea, select, option, button",
            "shot": "08_forms.png",
            "snip_parts": ["08_forms_a.png", "08_forms_b.png"],
        },
        {
            "n": 9,
            "title": "Семантическая разметка",
            "summary": (
                "Страница построена на семантических тегах HTML 5: "
                "<header> с логотипом, <nav> с навигационным меню, "
                "<main> с основным контентом — <article> (статья) и "
                "<aside> (боковая колонка), <footer> с контактами и "
                "копирайтом. Такая разметка улучшает доступность и "
                "понимание структуры страницы поисковыми системами."
            ),
            "tags": "header, nav, main, article, aside, footer",
            "shot": "09_semantic.png",
            "snip_parts": ["09_semantic_a.png", "09_semantic_b.png"],
        },
        {
            "n": 10,
            "title": "Аудио и видео",
            "summary": (
                "Демонстрация мультимедийных тегов: <audio "
                "controls> с несколькими <source> для разных "
                "форматов (mp3, ogg), <video controls> с poster и "
                "fallback-сообщением. Также добавлены <iframe> на "
                "видеохостинги YouTube и Vimeo — это типовой способ "
                "встраивания видео без локальных файлов."
            ),
            "tags": "audio, video, source, iframe (YouTube, Vimeo)",
            "shot": "10_audio_video.png",
            "snip": "10_audio_video.png",
        },
        {
            "n": 11,
            "title": "Встраивание Google Maps",
            "summary": (
                "Интерактивная карта Google Maps встроена через "
                "<iframe src=\"https://maps.google.com/maps?q=...&"
                "output=embed\">. Этот публичный embed-URL не "
                "требует API-ключа и работает напрямую с локального "
                "сервера и file://."
            ),
            "tags": "iframe + Google Maps embed",
            "shot": "11_iframe.png",
            "snip": "11_iframe.png",
        },
    ]

    for t in tasks:
        add_page_break(doc)
        add_heading(doc, f"Задание №{t['n']}. {t['title']}")
        add_para(doc, t["summary"])
        add_para(doc, f"Использованные теги: {t['tags']}.")
        add_image(
            doc,
            SHOTS / t["shot"],
            caption=f"Рисунок {t['n'] + 1} — внешний вид страницы (задание {t['n']})",
        )
        if "snip_parts" in t:
            for idx, part in enumerate(t["snip_parts"], start=1):
                add_image(
                    doc,
                    SNIPS / part,
                    caption=(
                        f"Листинг {t['n'] + 2} — исходный HTML задания "
                        f"{t['n']} (часть {idx} из {len(t['snip_parts'])})"
                    ),
                )
        else:
            add_image(
                doc,
                SNIPS / t["snip"],
                caption=f"Листинг {t['n'] + 2} — исходный HTML задания {t['n']}",
            )

    # === Проверка корректности ===
    add_page_break(doc)
    add_heading(doc, "Проверка корректности страниц")
    add_para(
        doc,
        "Для проверки доступности всех страниц был запущен локальный "
        "HTTP-сервер Python, после чего каждая из 12 страниц (index + "
        "11 заданий) запрошена через curl:",
    )
    add_listing(
        doc,
        "python3 -m http.server 8765 --bind 127.0.0.1 &\n"
        "for f in index 01-simple-page 02-text-formatting 03-lists \\\n"
        "         04-links 05-images 06-tables 07-input-types \\\n"
        "         08-forms 09-semantic 10-audio-video 11-iframe; do\n"
        "    curl -s -o /dev/null -w \"%{http_code} $f.html\\n\" \\\n"
        "         \"http://127.0.0.1:8765/$f.html\"\n"
        "done",
        caption="Листинг 14 — скрипт проверки",
    )
    add_para(
        doc,
        "Все 12 страниц возвращают код 200 OK. Дополнительно для "
        "каждой страницы сделан полностраничный screenshot через "
        "headless-браузер (рисунки 2–12 выше).",
    )

    # === Контрольные вопросы ===
    add_page_break(doc)
    add_heading(doc, "Контрольные вопросы")
    QA = [
        (
            "Какова обязательная структура HTML 5-документа?",
            "Документ начинается с инструкции <!DOCTYPE html>, далее "
            "корневой элемент <html lang=\"...\"> с указанием языка. "
            "Внутри — <head> с метатегом кодировки (<meta charset="
            "\"UTF-8\">), обязательным <title> и опциональным "
            "<meta name=\"viewport\"> для адаптива. Видимое "
            "содержимое размещается в <body>. Без DOCTYPE браузер "
            "переключается в quirks-mode, что ломает CSS-правила.",
        ),
        (
            "В чём смысловое отличие <strong>/<em> от <b>/<i>?",
            "<b> и <i> — чисто визуальные теги (bold/italic), они "
            "ничего не сообщают о смысле текста. <strong> и <em> — "
            "семантические: <strong> выделяет фрагмент по важности, "
            "<em> ставит логическое ударение. Screen-readers могут "
            "произносить такие фрагменты с особой интонацией. В "
            "HTML 5 рекомендуется отдавать предпочтение семантическим "
            "тегам, а чисто визуальное оформление выносить в CSS.",
        ),
        (
            "Зачем нужен атрибут alt у <img> и можно ли его не указывать?",
            "Атрибут alt — обязательный по стандарту HTML 5. Он "
            "выполняет три функции: 1) текст-замена при недоступности "
            "изображения (медленная сеть, ошибка загрузки); 2) "
            "озвучивание screen-readers для незрячих пользователей "
            "(доступность); 3) индексация поисковыми системами (SEO). "
            "Если изображение чисто декоративное, корректнее указать "
            "пустой alt=\"\" — это сигнал, что текст не требуется.",
        ),
        (
            "Что такое семантическая разметка и зачем она нужна?",
            "Семантическая разметка — использование тегов, отражающих "
            "смысл блока (header, nav, main, article, aside, footer, "
            "section, figure) вместо обезличенного <div class=\"...\">. "
            "Преимущества: 1) понятность кода для разработчиков; "
            "2) корректная работа screen-readers (browse by landmarks); "
            "3) лучшее ранжирование поисковыми системами (Google и "
            "Яндекс распознают тип контента); 4) автоматические "
            "режимы чтения у браузеров (Reading View Safari).",
        ),
        (
            "Чем colspan отличается от rowspan, и где они применяются?",
            "colspan=\"N\" объединяет ячейку с N последующими по "
            "горизонтали (внутри одной строки), rowspan=\"N\" — с N "
            "последующими по вертикали (через несколько строк). "
            "Используются для создания сложных шапок таблиц "
            "(заголовок над двумя колонками — colspan=\"2\") или "
            "для слияния повторяющихся значений в столбце "
            "(rowspan=\"3\" — одна общая ячейка на 3 строки). При "
            "использовании colspan/rowspan следующая ячейка в "
            "соответствующих строках/столбцах пропускается.",
        ),
        (
            "Почему iframe считается потенциально опасным элементом?",
            "Iframe загружает страницу из другого источника внутрь "
            "текущей и может стать вектором атак: clickjacking "
            "(невидимый iframe поверх кнопки), tracking (сторонние "
            "куки), XSS через postMessage. Для защиты применяются: "
            "атрибут sandbox (ограничения по умолчанию: запрет JS, "
            "форм, навигации), CSP-заголовок frame-src/frame-ancestors, "
            "заголовок X-Frame-Options ответа встраиваемой страницы. "
            "Для Google Maps и YouTube iframe считается приемлемым, "
            "так как сами эти источники доверены.",
        ),
    ]
    for i, (q, a) in enumerate(QA, start=1):
        add_qa(doc, i, q, a)

    # === Выводы ===
    add_page_break(doc)
    add_heading(doc, "Выводы")
    add_para(
        doc,
        "В рамках лабораторной работы созданы 11 самостоятельных "
        "HTML-страниц, каждая из которых демонстрирует одну тематику "
        "из методических указаний: базовый каркас документа, "
        "форматирование текста, списки, ссылки, изображения, таблицы, "
        "поля ввода всех типов, формы, семантическую разметку HTML 5, "
        "встраивание аудио/видео и интерактивных карт через iframe.",
    )
    add_para(
        doc,
        "Все 12 страниц (включая точку входа index.html) — валидные "
        "документы HTML 5 с указанной кодировкой UTF-8, языком ru и "
        "viewport-метатегом для корректной работы на мобильных "
        "устройствах. Проверка локальным HTTP-сервером подтверждает: "
        "все 12 запросов возвращают код 200 OK. Освоены основные "
        "группы тегов согласно таблице 2 и приобретены навыки, "
        "необходимые для дальнейшего изучения CSS и адаптивной "
        "вёрстки.",
    )

    # === Полные листинги ===
    add_page_break(doc)
    add_heading(doc, "Полные текстовые листинги исходного кода")
    add_para(
        doc,
        "Ниже приведены полные исходники всех 11 страниц в текстовой "
        "форме — для удобства копирования преподавателем.",
    )
    for n, fname, caption_num in [
        ("01", "01-simple-page.html", 15),
        ("02", "02-text-formatting.html", 16),
        ("03", "03-lists.html", 17),
        ("04", "04-links.html", 18),
        ("05", "05-images.html", 19),
        ("06", "06-tables.html", 20),
        ("07", "07-input-types.html", 21),
        ("08", "08-forms.html", 22),
        ("09", "09-semantic.html", 23),
        ("10", "10-audio-video.html", 24),
        ("11", "11-iframe.html", 25),
    ]:
        add_listing(
            doc,
            read_html(fname),
            caption=f"Листинг {caption_num} — {fname}",
        )

    out = ROOT / "docs" / "reports" / "lab_01" / "Ковалев Д.П. ВКБ43 1 лаба.docx"
    save(doc, out)
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
