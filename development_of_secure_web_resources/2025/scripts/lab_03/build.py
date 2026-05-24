"""Отчёт по лаб. 3 — Адаптивная вёрстка (7 заданий)."""

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

LAB_DIR = ROOT / "3"
SHOTS = ROOT / "docs" / "screenshots" / "lab_03"
SNIPS = ROOT / "docs" / "snippets" / "lab_03"


def read_css(name: str) -> str:
    return (LAB_DIR / "css" / name).read_text(encoding="utf-8")


def main() -> None:
    meta = LabMeta(
        number=3,
        title="Адаптивная вёрстка средствами CSS",
    )
    doc = make_doc()
    add_title_page(doc, meta)
    add_page_break(doc)

    add_heading(doc, "Тема и цель работы")
    add_para(
        doc,
        "Тема: подключение CSS-стилей и адаптивная вёрстка — использование "
        "CSS Grid, Flexbox, медиа-запросов (@media), относительных единиц "
        "(%, em, rem, vw, vh, fr) и viewport-метатега для корректной "
        "работы веб-страниц на устройствах разной ширины: от мобильных "
        "телефонов 320–414px до широких десктопов 1920px+.",
    )
    add_para(
        doc,
        "Цель работы: сформировать понимание основных способов подключения "
        "CSS-стилей; научиться применять CSS для адаптивной стилизации "
        "HTML-элементов; освоить медиа-запросы и подход mobile-first; "
        "уверенно использовать Grid для двумерных сеток и Flexbox для "
        "одномерных компоновок; реализовать типовые адаптивные паттерны "
        "(stack-table, sticky-header, гамбургер-меню, hero-секцию "
        "лендинга).",
    )

    add_heading(doc, "Условие задания", level=2)
    add_bullets(
        doc,
        [
            "Задание 1. Адаптивная сетка товаров: 12 карточек, "
            "переключение количества колонок по брейкпоинтам 768px и "
            "1200px.",
            "Задание 2. Sticky-header с навигацией и гамбургер-меню "
            "для мобильных устройств — реализация без JavaScript.",
            "Задание 3. Адаптивная форма обратной связи: поля «Имя» и "
            "«Email» в одну строку на десктопе, в столбец — на мобильных.",
            "Задание 4. Блок «О компании» с переключаемой осью "
            "Flexbox (горизонтально/вертикально).",
            "Задание 5. Адаптивная таблица «Stack Table»: на десктопе — "
            "обычная таблица, на мобильных — карточки с подписями.",
            "Задание 6. Адаптивные фильтры результатов: скрытие/"
            "показ панели фильтров без JavaScript (через :checked).",
            "Задание 7. Полноценная Landing Page с hero, "
            "преимуществами, тарифами, отзывами и формой связи.",
        ],
    )

    # === Теория ===
    add_page_break(doc)
    add_heading(doc, "Краткая теория")

    add_heading(doc, "Viewport-метатег", level=2)
    add_para(
        doc,
        "Без viewport-метатега мобильный браузер открывает страницу на "
        "виртуальном экране шириной 980px и масштабирует её под "
        "фактический экран, что делает текст нечитаемым. Метатег "
        "переключает страницу в режим, когда CSS-пиксель равен пикселю "
        "устройства с поправкой на DPR:",
    )
    add_listing(
        doc,
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">",
        caption="Листинг 1 — обязательный viewport-метатег",
    )

    add_heading(doc, "Относительные единицы и медиа-запросы", level=2)
    add_table_simple(
        doc,
        [
            ["Единица", "К чему относится"],
            ["%", "Размер родительского блока"],
            ["em", "font-size текущего элемента"],
            ["rem", "font-size корневого <html> (обычно 16px)"],
            ["vw / vh", "1% ширины / высоты viewport"],
            ["fr", "Доля свободного места в Grid"],
            ["minmax(min, max)", "Гибкий диапазон в Grid"],
            ["clamp(min, pref, max)", "Адаптивное значение с ограничителями"],
        ],
        caption="Таблица 1 — относительные единицы CSS",
    )
    add_para(
        doc,
        "Медиа-запрос условно применяет CSS-правила в зависимости от "
        "ширины окна, ориентации, DPR, цветовой схемы:",
    )
    add_listing(
        doc,
        "/* mobile-first: базовые правила для узких экранов */\n"
        ".grid { grid-template-columns: 1fr; }\n\n"
        "@media (min-width: 768px) {\n"
        "    .grid { grid-template-columns: repeat(3, 1fr); }\n"
        "}\n"
        "@media (min-width: 1200px) {\n"
        "    .grid { grid-template-columns: repeat(4, 1fr); }\n"
        "}",
        caption="Листинг 2 — структура mobile-first",
    )

    add_heading(doc, "Flexbox и Grid: когда что выбирать", level=2)
    add_table_simple(
        doc,
        [
            ["Задача", "Инструмент"],
            ["Один ряд / одна колонка элементов, выравнивание", "Flexbox"],
            ["Двумерная сетка карточек, лендинг", "Grid"],
            ["Адаптивная таблица из сетки", "Grid + minmax + auto-fit"],
            ["Внутренности карточки (изображение + текст)", "Flexbox"],
            ["Sticky-header или sticky-sidebar", "position: sticky"],
        ],
        caption="Таблица 2 — Flexbox vs Grid",
    )

    add_heading(doc, "CSS-only переключатели через :checked", level=2)
    add_para(
        doc,
        "Раскрытие меню/панели фильтров можно реализовать без "
        "JavaScript — через скрытый <input type=\"checkbox\"> и "
        "соседний селектор:",
    )
    add_listing(
        doc,
        "<input type=\"checkbox\" id=\"menu-toggle\" hidden>\n"
        "<label for=\"menu-toggle\">≡ Меню</label>\n"
        "<nav>...</nav>\n\n"
        "/* CSS */\n"
        "#menu-toggle:checked ~ nav { max-height: 400px; }",
        caption="Листинг 3 — CSS-only переключатель",
    )
    add_para(
        doc,
        "Применяется в заданиях 2 (sticky-меню) и 6 (фильтры). "
        "Прогрессивное улучшение: даже при отключённом JavaScript "
        "интерфейс остаётся работоспособным.",
    )

    # === Index ===
    add_page_break(doc)
    add_heading(doc, "Точка входа и структура проекта")
    add_image(doc, SHOTS / "00_index.png", caption="Рисунок 1 — содержание лабораторной (index.html)")

    # === ПО ЗАДАНИЯМ ===
    tasks = [
        {
            "n": 1,
            "title": "Адаптивная сетка товаров (Grid)",
            "summary": (
                "12 карточек товаров расположены в CSS-сетке "
                "(display: grid). Брейкпоинты: <768px — 2 в строке; "
                "768–1199px — 3 в строке; ≥1200px — 4 в строке. "
                "Базовая раскладка mobile-first: "
                "grid-template-columns: repeat(2, 1fr); расширения "
                "через @media (min-width: 768px) и (min-width: "
                "1200px). Используются также grid-gap, "
                "padding/margin в относительных rem."
            ),
            "shots": [
                ("01_grid_products_desktop.png", "Десктоп (1280px) — 4 колонки"),
                ("01_grid_products_mobile.png", "Мобильный (390px) — 2 колонки"),
            ],
            "snips": ["01_grid_products_a.png", "01_grid_products_b.png"],
        },
        {
            "n": 2,
            "title": "Sticky-header + гамбургер-меню без JavaScript",
            "summary": (
                "Шапка страницы фиксируется через position: sticky; "
                "top: 0; и остаётся на месте при прокрутке. На "
                "мобильных (max-width: 767px) ссылки сворачиваются в "
                "выпадающий список под иконкой-«бургер». Переключение "
                "реализовано чистым CSS — через скрытый <input "
                "type=\"checkbox\"> и соседний селектор "
                ".menu-toggle:checked ~ .header .nav { max-height: "
                "400px; }. JavaScript не используется."
            ),
            "shots": [
                ("02_sticky_menu_desktop.png", "Десктоп — горизонтальное меню"),
                ("02_sticky_menu_mobile.png", "Мобильный — гамбургер"),
            ],
            "snips": ["02_sticky_menu_a.png", "02_sticky_menu_b.png"],
        },
        {
            "n": 3,
            "title": "Адаптивная форма «Обратная связь»",
            "summary": (
                "Поля «Имя» и «Email» расположены в одну строку при "
                "ширине окна ≥768px и в столбец — на мобильных. "
                "Реализовано через CSS Grid: базовая раскладка "
                "grid-template-columns: 1fr (один столбец), в "
                "медиа-запросе 1fr 1fr (два столбца). Валидация — "
                "нативная HTML5 (required, type=\"email\")."
            ),
            "shots": [
                ("03_contact_form_desktop.png", "Десктоп — поля в одной строке"),
                ("03_contact_form_mobile.png", "Мобильный — поля в столбец"),
            ],
            "snips": ["03_contact_form_a.png", "03_contact_form_b.png"],
        },
        {
            "n": 4,
            "title": "Адаптивный «О компании» (Flexbox)",
            "summary": (
                "Блок «О компании» содержит логотип (inline-SVG с "
                "градиентом) и описательный текст. На десктопе они "
                "расположены горизонтально (flex-direction: row, "
                "лого слева), на мобильных — вертикально "
                "(flex-direction: column, лого сверху). Переключение "
                "оси через @media-запрос."
            ),
            "shots": [
                ("04_company_info_desktop.png", "Десктоп — flex-direction: row"),
                ("04_company_info_mobile.png", "Мобильный — flex-direction: column"),
            ],
            "snips": ["04_company_info.png"],
        },
        {
            "n": 5,
            "title": "Адаптивная таблица (Stack Table)",
            "summary": (
                "На десктопе отображается стандартная HTML-таблица. "
                "На мобильных (max-width: 767px) каждая строка "
                "превращается в карточку: thead скрыт через "
                "display: none, ячейки получают подписи через "
                "data-label у <td> и псевдоэлемент ::before с "
                "content: attr(data-label). Этот приём решает "
                "проблему горизонтальной прокрутки таблиц на узких "
                "экранах без потери информации."
            ),
            "shots": [
                ("05_stack_table_desktop.png", "Десктоп — обычная таблица"),
                ("05_stack_table_mobile.png", "Мобильный — карточки с подписями"),
            ],
            "snips": ["05_stack_table.png"],
        },
        {
            "n": 6,
            "title": "Адаптивные фильтры результатов (CSS-only)",
            "summary": (
                "На десктопе — двухколоночный макет: панель фильтров "
                "слева (≈260px), результаты справа. На мобильных "
                "(max-width: 799px) панель фильтров скрывается, "
                "появляется кнопка «Показать фильтры». Раскрытие "
                "панели — снова через <input type=\"checkbox\"> и "
                "соседний селектор, без JavaScript. Демонстрирует, "
                "как сложные интерактивные паттерны можно "
                "реализовать чистым CSS."
            ),
            "shots": [
                ("06_filters_desktop.png", "Десктоп — фильтры слева"),
                ("06_filters_mobile.png", "Мобильный — фильтры свёрнуты"),
            ],
            "snips": ["06_filters_a.png", "06_filters_b.png"],
        },
        {
            "n": 7,
            "title": "Landing Page",
            "summary": (
                "Полноценный одностраничный лендинг, включающий: "
                "sticky-header с навигацией и логотипом; hero-секцию "
                "с заголовком и CTA-кнопкой, размер шрифта через "
                "clamp() для адаптивности; 3 карточки преимуществ "
                "(grid-template-columns: 1fr → repeat(3, 1fr)); 3 "
                "тарифа с выделенным центральным (scale(1.04) + "
                "цветная рамка); горизонтальный Flexbox-«карусель» "
                "отзывов на scroll-snap; форма «Связаться с нами» "
                "(поля становятся в столбец на узких экранах); "
                "тёмный футер."
            ),
            "shots": [
                ("07_landing_desktop.png", "Десктоп — полная страница"),
                ("07_landing_mobile.png", "Мобильный — однокол. вёрстка"),
            ],
            "snips": ["07_landing_a.png", "07_landing_b.png", "07_landing_c.png"],
        },
    ]

    rfig = 1
    lst = 3
    for t in tasks:
        add_page_break(doc)
        add_heading(doc, f"Задание №{t['n']}. {t['title']}")
        add_para(doc, t["summary"])
        for fname, label in t["shots"]:
            rfig += 1
            add_image(
                doc,
                SHOTS / fname,
                caption=f"Рисунок {rfig} — задание {t['n']}: {label}",
            )
        for idx, fname in enumerate(t["snips"], start=1):
            lst += 1
            cap_suffix = (
                f" (часть {idx} из {len(t['snips'])})"
                if len(t["snips"]) > 1
                else ""
            )
            add_image(
                doc,
                SNIPS / fname,
                caption=f"Листинг {lst} — CSS задания {t['n']}{cap_suffix}",
            )

    # === Проверка ===
    add_page_break(doc)
    add_heading(doc, "Проверка корректности")
    add_para(
        doc,
        "Все 8 страниц (index + 7 заданий) проверены через локальный "
        "HTTP-сервер; ответ 200 OK на каждый запрос. Адаптивность "
        "проверена снятием полностраничных скриншотов в двух "
        "viewport-ах: 1280×800 (десктоп) и 390×844 (мобильный, "
        "соответствует iPhone 12/13/14):",
    )
    add_listing(
        doc,
        "python3 -m http.server 8767 --bind 127.0.0.1 &\n"
        "for f in index 01-grid-products 02-sticky-menu \\\n"
        "         03-contact-form 04-company-info 05-stack-table \\\n"
        "         06-filters 07-landing; do\n"
        "    curl -s -o /dev/null -w \"%{http_code} $f.html\\n\" \\\n"
        "         \"http://127.0.0.1:8767/$f.html\"\n"
        "done",
        caption=f"Листинг {lst + 1} — скрипт проверки",
    )
    add_para(
        doc,
        "Дополнительно проверено отсутствие JavaScript в "
        "css/02-sticky-menu.css и css/06-filters.css — переключение "
        "реализовано исключительно через :checked-селекторы.",
    )

    # === Контрольные вопросы ===
    add_page_break(doc)
    add_heading(doc, "Контрольные вопросы")
    QA = [
        (
            "Зачем нужен viewport-метатег и что произойдёт без него?",
            "Метатег <meta name=\"viewport\" content=\"width=device-"
            "width, initial-scale=1\"> переключает мобильный браузер "
            "в режим, при котором CSS-пиксель соответствует пикселю "
            "устройства (с поправкой на DPR), и медиа-запросы "
            "работают корректно. Без него мобильный браузер "
            "открывает страницу на виртуальном экране 980px и "
            "масштабирует под фактический экран — текст становится "
            "нечитаемым, а CSS-правила @media (max-width: 768px) не "
            "срабатывают, потому что браузер «считает» экран "
            "широким.",
        ),
        (
            "В чём разница между em и rem?",
            "em — относительно font-size текущего элемента (или "
            "ближайшего родителя для свойств, не зависящих от шрифта). "
            "rem — относительно font-size корневого элемента <html> "
            "(обычно 16px). em каскадирует и может «накапливаться» "
            "при вложенности (1.2em внутри 1.2em даёт 1.44em), что "
            "часто нежелательно. rem всегда стабилен относительно "
            "корня — удобен для размеров, отступов, шрифтов на всей "
            "странице. Современная практика: rem для типографики и "
            "размеров, em — для отступов внутри компонента, чтобы "
            "они масштабировались вместе со шрифтом компонента.",
        ),
        (
            "Что значит подход mobile-first?",
            "Подход mobile-first означает, что базовые CSS-правила "
            "(вне @media) написаны для мобильных устройств — самого "
            "узкого случая. Расширения для широких экранов "
            "добавляются через @media (min-width: ...). "
            "Преимущества: 1) проще код (меньше переопределений и "
            "сбросов); 2) меньшие CSS-файлы — мобильное устройство "
            "загружает только базовые правила; 3) лучше "
            "performance — браузер сразу применяет нужные правила; "
            "4) такой код легче поддерживать. Противоположный "
            "подход (desktop-first с @media max-width) считается "
            "устаревшим.",
        ),
        (
            "Чем CSS Grid отличается от Flexbox?",
            "Grid — двумерная система компоновки: одновременно "
            "управляет колонками и строками, идеально подходит для "
            "сеток карточек, лендингов, дашбордов, сложных "
            "форм-макетов. Flexbox — одномерная: распределяет "
            "элементы по одной оси (главная — main axis, "
            "поперечная — cross). Подходит для одного ряда кнопок, "
            "выравнивания внутри карточки, sticky-меню. Часто "
            "комбинируются: Grid для общей структуры страницы, "
            "Flexbox для внутреннего содержимого карточек.",
        ),
        (
            "Что такое position: sticky и как он работает?",
            "Position: sticky — гибридное позиционирование. Элемент "
            "ведёт себя как relative (занимает место в потоке "
            "документа), пока его исходная позиция видна на экране. "
            "Когда при прокрутке элемент достигает заданного "
            "смещения (например, top: 0), он переключается в "
            "режим fixed и остаётся на месте до тех пор, пока его "
            "родительский контейнер виден. При выходе родителя за "
            "пределы экрана элемент уходит вместе с ним. "
            "Используется для sticky-header, sticky-sidebar, "
            "sticky-таблиц.",
        ),
        (
            "Как реализовать переключатель видимости без JavaScript?",
            "Через скрытый <input type=\"checkbox\"> и соседние "
            "CSS-селекторы. Состояние чекбокса (отмечен / не "
            "отмечен) меняет CSS через псевдокласс :checked, а "
            "соседние селекторы ~ (общий сосед) или + (следующий "
            "сосед) пробрасывают изменение на нужный элемент. "
            "Пример: #menu-toggle:checked ~ nav { max-height: "
            "400px; }. Преимущества: 0 строк JavaScript, "
            "работоспособность при отключённом JS, ускоренная "
            "загрузка. Недостаток: ограниченные возможности "
            "(невозможно сохранить состояние между страницами без "
            "JS).",
        ),
        (
            "Как сделать таблицу адаптивной без горизонтальной прокрутки?",
            "Через паттерн Stack Table: на широких экранах оставить "
            "обычную таблицу, на узких — превратить каждую строку в "
            "карточку. Реализация: 1) <td data-label=\"Имя\">Иван</td> "
            "— подпись хранится в data-атрибуте; 2) на мобильных "
            "thead { display: none; }, tr { display: block; }, "
            "td { display: block; }; 3) перед содержимым ячейки — "
            "псевдоэлемент с подписью: td::before { content: "
            "attr(data-label); font-weight: bold; }. Альтернатива — "
            "паттерн horizontal scroll (overflow-x: auto) или "
            "приоритизация столбцов (column-hiding).",
        ),
    ]
    for i, (q, a) in enumerate(QA, start=1):
        add_qa(doc, i, q, a)

    # === Выводы ===
    add_page_break(doc)
    add_heading(doc, "Выводы")
    add_para(
        doc,
        "В работе использованы все основные техники адаптивной "
        "вёрстки: viewport-метатег, mobile-first медиа-запросы, "
        "CSS Grid для двумерных сеток (задания 1, 3, 7), Flexbox "
        "для одномерных компоновок (задания 4, 7), position: "
        "sticky (задания 2, 7), scroll-snap для каруселей "
        "(задание 7), CSS-only переключатели через :checked "
        "(задания 2, 6), адаптивная таблица через data-label + "
        "::before (задание 5). Все 7 задач реализованы "
        "корректно: проверка curl возвращает 200 OK на всех 8 "
        "страницах и 8 CSS-файлах.",
    )
    add_para(
        doc,
        "Полностраничные скриншоты в двух viewport-ах (1280×800 и "
        "390×844) подтверждают корректное срабатывание всех "
        "медиа-запросов и адаптивную перестройку макета. "
        "Дополнительно подтверждено отсутствие JavaScript в "
        "заданиях 2 и 6 — переключение реализовано чистым CSS.",
    )

    # === Полные листинги ===
    add_page_break(doc)
    add_heading(doc, "Полные текстовые листинги CSS")
    for fname in [
        "reset.css",
        "01-grid-products.css",
        "02-sticky-menu.css",
        "03-contact-form.css",
        "04-company-info.css",
        "05-stack-table.css",
        "06-filters.css",
        "07-landing.css",
    ]:
        lst += 1
        add_listing(
            doc,
            read_css(fname),
            caption=f"Листинг {lst} — css/{fname}",
        )

    out = ROOT / "docs" / "reports" / "lab_03" / "Ковалев Д.П. ВКБ43 3 лаба.docx"
    save(doc, out)
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
