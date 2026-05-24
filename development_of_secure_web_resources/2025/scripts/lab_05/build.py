"""Отчёт по лаб. 5 — Браузерные события (7 заданий)."""

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

LAB_DIR = ROOT / "5"
SHOTS = ROOT / "docs" / "screenshots" / "lab_05"
SNIPS = ROOT / "docs" / "snippets" / "lab_05"


def read_js(name: str) -> str:
    return (LAB_DIR / "js" / name).read_text(encoding="utf-8")


def main() -> None:
    meta = LabMeta(
        number=5,
        title="Браузерные события и интерактивные веб-приложения",
    )
    doc = make_doc()
    add_title_page(doc, meta)
    add_page_break(doc)

    add_heading(doc, "Тема и цель работы")
    add_para(
        doc,
        "Тема: модель событий DOM — фазы capturing/target/bubbling, "
        "методы addEventListener/removeEventListener, объект Event "
        "(target, currentTarget, stopPropagation, preventDefault), "
        "делегирование событий; основные группы событий: мышиные "
        "(click, dblclick, contextmenu, mouseenter/mouseleave/"
        "mousemove), клавиатурные (keydown), формы (submit, blur, "
        "input), таймеры (setTimeout, setInterval), Drag & Drop API.",
    )
    add_para(
        doc,
        "Цель работы: изучить механизмы обработки событий в "
        "веб-браузере; освоить базовые методы работы с событиями "
        "DOM; применить их для создания интерактивных веб-"
        "приложений — от hover-эффектов до полнофункциональных "
        "форм с валидацией, контекстных меню и Drag & Drop "
        "карточек между списками.",
    )

    add_heading(doc, "Условие задания", level=2)
    add_bullets(
        doc,
        [
            "Задание 1. Hover-эффекты на навигационных ссылках с "
            "плавным увеличением и сменой фона при наведении.",
            "Задание 2. Модальное окно регистрации с собственной "
            "валидацией email (RFC 5321/6531) и пароля (длина, "
            "регистр, спецсимволы); закрытие крестиком, кнопкой, "
            "по Escape и клику по затемнённому фону.",
            "Задание 3. Таймер обратного отсчёта с кнопками "
            "«Запустить», «Пауза», «Сброс»; блокировка input во "
            "время отсчёта.",
            "Задание 4. Галерея фигур с увеличенным превью, "
            "следующим за курсором (mouseenter/mouseleave/"
            "mousemove + автозеркалирование у краёв окна).",
            "Задание 5. Интерактивная таблица товаров: inline-"
            "редактирование «Количество» (click + contenteditable), "
            "редактирование «Цены» через модальное окно (dblclick), "
            "контекстное меню по правому клику, Drag & Drop "
            "перестановки строк.",
            "Задание 6. Всплывающее окно помощи через "
            "setTimeout(5000) после DOMContentLoaded; форма с "
            "preventDefault и автозакрытием после отправки.",
            "Задание 7. Списки студентов с Drag & Drop между "
            "ними; ограничение «без псевдоклассов и "
            "псевдоэлементов» в CSS — все эффекты через JS.",
        ],
    )

    # === Теория ===
    add_page_break(doc)
    add_heading(doc, "Краткая теория")

    add_heading(doc, "Модель событий DOM", level=2)
    add_para(
        doc,
        "Событие в DOM проходит три фазы: capturing (от window вниз "
        "к цели), target (достигает event.target), bubbling (всплытие "
        "обратно к window). Обработчики по умолчанию срабатывают на "
        "фазах target и bubbling. Для перехвата в фазе capturing "
        "передаётся опция { capture: true }.",
    )
    add_listing(
        doc,
        "element.addEventListener('click', handler, options);\n"
        "// options.capture = true   → перехват в фазе погружения\n"
        "// event.target            → реальный элемент-источник\n"
        "// event.currentTarget     → элемент, на котором висит handler\n"
        "// event.stopPropagation() → остановить всплытие\n"
        "// event.preventDefault()  → отменить действие по умолчанию",
        caption="Листинг 1 — методы и свойства Event",
    )

    add_heading(doc, "Делегирование событий", level=2)
    add_para(
        doc,
        "Делегирование — техника, при которой один обработчик висит "
        "на родительском контейнере и определяет источник через "
        "event.target.closest(). Это экономит память (один обработчик "
        "вместо N), позволяет работать с динамически добавляемыми "
        "элементами и упрощает unbind. Применяется в заданиях 5 "
        "(таблица товаров — handler на tbody) и 7 (списки — "
        "handler на контейнере группы).",
    )
    add_listing(
        doc,
        "table.addEventListener('click', e => {\n"
        "    const cell = e.target.closest('[data-field=\"qty\"]');\n"
        "    if (!cell) return;\n"
        "    // обработка клика по нужной ячейке\n"
        "});",
        caption="Листинг 2 — делегирование клика",
    )

    add_heading(doc, "Группы событий, использованные в работе", level=2)
    add_table_simple(
        doc,
        [
            ["Группа", "События"],
            ["Мышь", "click, dblclick, contextmenu, mouseenter, mouseleave, mousemove"],
            ["Клавиатура", "keydown (для Escape, Enter)"],
            ["Формы", "submit, blur, input, change"],
            ["Drag & Drop", "dragstart, dragenter, dragover, dragleave, drop, dragend"],
            ["Таймеры", "setTimeout, setInterval, clearTimeout, clearInterval"],
            ["Жизненный цикл", "DOMContentLoaded, load"],
        ],
        caption="Таблица 1 — группы событий",
    )

    add_heading(doc, "Drag & Drop API", level=2)
    add_para(
        doc,
        "Последовательность событий при перетаскивании: dragstart "
        "(на источнике) → dragenter/dragover/dragleave (на "
        "потенциальных целях) → drop (на цели) → dragend (на "
        "источнике). Чтобы drop сработал, в dragover обязательно "
        "вызвать event.preventDefault(): браузер по умолчанию "
        "запрещает дроп. Передача данных — через "
        "event.dataTransfer.setData / getData. Применяется в "
        "заданиях 5 (перестановка строк) и 7 (перенос карточек "
        "между списками).",
    )

    # === Index ===
    add_page_break(doc)
    add_heading(doc, "Точка входа")
    add_image(doc, SHOTS / "00_index.png", caption="Рисунок 1 — содержание лабораторной (index.html)")

    # === ПО ЗАДАНИЯМ ===
    add_page_break(doc)
    add_heading(doc, "Задания №1, 2, 3. Навигация, модальная регистрация, таймер")
    add_para(
        doc,
        "Задания 1, 2 и 3 объединены на одной странице "
        "01-nav-modal-timer.html, поскольку логически связаны "
        "(шапка с навигацией ведёт к модалке регистрации). Задание 1 "
        "— hover-эффекты на навигации (плавное увеличение "
        "transform: scale(1.2) и смена фона при :hover, реализованы "
        "CSS-transition, без JavaScript). Задание 2 — модальная "
        "форма регистрации с валидацией: email по упрощённому "
        "правилу RFC 5321 (длина ≤ 254, локальная часть ≤ 64, "
        "TLD 2…63, ровно один @, без двойных точек), пароль ≥ 12 "
        "символов с обязательными буквами разного регистра, "
        "цифрой и спецсимволом из !@#$%^&*. Закрытие — крестиком, "
        "кнопкой «Закрыть», по Escape (keydown), кликом по "
        "затемнённому фону. Задание 3 — таймер обратного отсчёта: "
        "setInterval(1000), блокировка input на время работы, "
        "сообщение «Время вышло!» по нулю.",
    )
    add_image(doc, SHOTS / "01a_nav_default.png", caption="Рисунок 2 — задания 1–3: исходное состояние")
    add_image(doc, SHOTS / "01b_modal_open.png", caption="Рисунок 3 — задание 2: модальное окно регистрации")
    add_image(doc, SHOTS / "01c_modal_errors.png", caption="Рисунок 4 — задание 2: ошибки валидации формы")
    add_image(doc, SHOTS / "01d_timer_running.png", caption="Рисунок 5 — задание 3: таймер обратного отсчёта")
    add_image(doc, SNIPS / "01_nav_modal_timer_a.png", caption="Листинг 3 — JS заданий 1–3 (часть 1 из 3): валидация email и пароля")
    add_image(doc, SNIPS / "01_nav_modal_timer_b.png", caption="Листинг 4 — JS заданий 1–3 (часть 2 из 3): модальное окно")
    add_image(doc, SNIPS / "01_nav_modal_timer_c.png", caption="Листинг 5 — JS заданий 1–3 (часть 3 из 3): таймер обратного отсчёта")

    add_page_break(doc)
    add_heading(doc, "Задание №4. Галерея с превью у курсора")
    add_para(
        doc,
        "На странице расположены SVG-фигуры. При mouseenter на "
        "фигуру JavaScript клонирует её содержимое в скрытый блок "
        "превью и показывает его рядом с курсором. При mousemove "
        "блок превью движется за курсором; при приближении к "
        "правому/нижнему краю окна автоматически «зеркалируется» "
        "на противоположную сторону, чтобы не выходить за пределы "
        "viewport. При mouseleave превью исчезает. Использованы "
        "три события мыши без single click.",
    )
    add_image(doc, SHOTS / "04a_gallery.png", caption="Рисунок 6 — задание 4: галерея фигур (исходное состояние)")
    add_image(doc, SNIPS / "04_gallery.png", caption="Листинг 6 — JS задания 4 (галерея с превью)")

    add_page_break(doc)
    add_heading(doc, "Задание №5. Интерактивная таблица товаров")
    add_para(
        doc,
        "Таблица содержит товары с колонками «Название», «Цена», "
        "«Количество», «Сумма». Реализована широкая палитра "
        "интерактивности: (а) одиночный клик по «Количество» — "
        "inline-редактирование через contenteditable, при blur "
        "или Enter — пересчёт суммы; (б) двойной клик по «Цена за "
        "единицу» — модальное окно с числовым полем; (в) правый "
        "клик по строке (contextmenu) — контекстное меню «Удалить "
        "/ Изменить название / Добавить комментарий», "
        "позиционируется у курсора, закрывается кликом снаружи "
        "или Escape; (г) Drag & Drop строк — перестановка через "
        "dragstart/dragover/drop/dragend. Все обработчики "
        "навешены на tbody через делегирование событий.",
    )
    add_image(doc, SHOTS / "05a_products_table.png", caption="Рисунок 7 — задание 5: исходный вид таблицы")
    add_image(doc, SHOTS / "05b_products_context.png", caption="Рисунок 8 — задание 5: контекстное меню по правому клику")
    add_image(doc, SNIPS / "05_products_table_a.png", caption="Листинг 7 — JS задания 5 (часть 1 из 3): inline-редактирование")
    add_image(doc, SNIPS / "05_products_table_b.png", caption="Листинг 8 — JS задания 5 (часть 2 из 3): модальное окно и контекстное меню")
    add_image(doc, SNIPS / "05_products_table_c.png", caption="Листинг 9 — JS задания 5 (часть 3 из 3): Drag & Drop строк")

    add_page_break(doc)
    add_heading(doc, "Задание №6. Всплывающее окно помощи")
    add_para(
        doc,
        "Окно появляется автоматически через setTimeout(5000) "
        "после DOMContentLoaded. Содержит поле «Ваш вопрос» "
        "(textarea) и кнопку «Отправить». При отправке: "
        "event.preventDefault() отменяет реальную отправку "
        "формы (которая обновила бы страницу), показывается "
        "«Спасибо!», поле очищается, окно автоматически "
        "закрывается через 1.5 секунды (setTimeout). Закрытие "
        "также возможно крестиком, кликом по фону, по нажатию "
        "Escape (keydown). На скриншоте — попап через 5 секунд "
        "после загрузки страницы.",
    )
    add_image(doc, SHOTS / "06_help_popup.png", caption="Рисунок 9 — задание 6: всплывающее окно помощи")
    add_image(doc, SNIPS / "06_help_popup.png", caption="Листинг 10 — JS задания 6 (всплывающее окно помощи)")

    add_page_break(doc)
    add_heading(doc, "Задание №7. Drag & Drop списков студентов")
    add_para(
        doc,
        "Два списка: «Группа ВИ-31» (с полем «Добавить») и "
        "«Задолжники» (с плейсхолдером «Перетяни сюда»). "
        "Карточки автоматически сортируются по алфавиту "
        "(localeCompare с русской локалью) при каждом изменении. "
        "Правый клик по карточке — меню «Удалить / Закрыть» "
        "справа от курсора (с авто-сдвигом, если не помещается "
        "в окно). Drag & Drop между списками — при успешном "
        "дропе анимация is-success, при дропе вне зоны (dragend "
        "без drop) — анимация is-error (shake + красная "
        "подсветка). Счётчики «Всего N» в шапках обновляются "
        "автоматически. Лимит — 35 карточек суммарно.",
    )
    add_para(
        doc,
        "Важное ограничение: по условию задания 7 в CSS "
        "запрещены псевдоклассы (:hover, :active, :focus) и "
        "псевдоэлементы (::before, ::after). Все эффекты "
        "наведения, подсветки drop-зоны, ошибки и успеха "
        "реализованы через JS: на mouseenter/mouseleave, "
        "dragenter/dragleave/dragend JavaScript добавляет/"
        "снимает обычные классы .is-hover, .is-dragover, "
        ".is-success, .is-error. Сами эти классы — обычные "
        "селекторы, не псевдоклассы.",
    )
    add_image(doc, SHOTS / "07_students_dnd.png", caption="Рисунок 10 — задание 7: два списка студентов")
    add_image(doc, SNIPS / "07_students_dnd_a.png", caption="Листинг 11 — JS задания 7 (часть 1 из 4): инициализация и рендер")
    add_image(doc, SNIPS / "07_students_dnd_b.png", caption="Листинг 12 — JS задания 7 (часть 2 из 4): добавление и сортировка")
    add_image(doc, SNIPS / "07_students_dnd_c.png", caption="Листинг 13 — JS задания 7 (часть 3 из 4): контекстное меню")
    add_image(doc, SNIPS / "07_students_dnd_d.png", caption="Листинг 14 — JS задания 7 (часть 4 из 4): drag & drop логика")

    # === Проверка ===
    add_page_break(doc)
    add_heading(doc, "Проверка корректности страниц")
    add_para(
        doc,
        "Все 6 страниц проверены через локальный HTTP-сервер; "
        "ответ 200 OK на каждый запрос. Интерактивное поведение "
        "(модалка, контекстное меню, всплывающий попап) "
        "проверено через headless-Playwright — программные "
        "клики и dispatchEvent с последующими скриншотами.",
    )
    add_listing(
        doc,
        "python3 -m http.server 8769 --bind 127.0.0.1 &\n"
        "for f in index 01-nav-modal-timer 04-gallery \\\n"
        "         05-products-table 06-help-popup 07-students-dnd; do\n"
        "    curl -s -o /dev/null -w \"%{http_code} $f.html\\n\" \\\n"
        "         \"http://127.0.0.1:8769/$f.html\"\n"
        "done",
        caption="Листинг 15 — скрипт проверки",
    )
    add_para(
        doc,
        "Дополнительно проверено, что в css/07-students-dnd.css "
        "нет запрещённых псевдоклассов и псевдоэлементов "
        "(grep по списку «:hover, :focus, :active, ::before, "
        "::after» ничего не находит в реальных правилах — "
        "только в комментариях-пояснениях).",
    )

    # === Контрольные вопросы ===
    add_page_break(doc)
    add_heading(doc, "Контрольные вопросы")
    QA = [
        (
            "Какие фазы проходит событие в модели DOM и зачем это знать?",
            "Событие проходит три фазы: 1) capturing — от window "
            "вниз через всех родителей к event.target; 2) target — "
            "достигает целевого элемента; 3) bubbling — всплывает "
            "обратно к window через всех родителей. По умолчанию "
            "addEventListener подписывается на target и bubbling; "
            "{ capture: true } подписывает на capturing. Знание фаз "
            "важно для: 1) делегирования — обработчик на родителе "
            "ловит события всех детей именно благодаря bubbling; "
            "2) перехвата раньше дочерних обработчиков "
            "(capturing); 3) понимания, что stopPropagation() в "
            "одной фазе не отменяет другую.",
        ),
        (
            "В чём разница между event.target и event.currentTarget?",
            "event.target — реальный элемент, на котором "
            "произошло событие (источник). При делегировании это "
            "конкретная дочерняя кнопка/ячейка. "
            "event.currentTarget — элемент, на котором висит "
            "текущий обработчик (родитель при делегировании). "
            "Например, при click на <button> внутри <ul> с "
            "обработчиком на <ul>: event.target === button, "
            "event.currentTarget === ul. Полезно использовать "
            "event.target.closest(selector) — поднимается от "
            "target до ближайшего предка, подходящего под "
            "селектор.",
        ),
        (
            "Что такое делегирование событий и какие у него преимущества?",
            "Делегирование — техника, при которой один "
            "обработчик висит на родительском контейнере и "
            "определяет конкретный источник через "
            "event.target.closest('...'). Преимущества: 1) "
            "экономия памяти — один обработчик вместо N; 2) "
            "работает с динамически добавляемыми элементами без "
            "повторной подписки; 3) проще unbind — снять один "
            "обработчик. Применяется, когда внутри контейнера "
            "много однотипных интерактивных элементов: таблицы, "
            "списки, меню. В задании 5 один обработчик на "
            "<tbody> обрабатывает клики, dblclick, contextmenu "
            "по всем строкам и ячейкам.",
        ),
        (
            "Зачем нужны preventDefault и stopPropagation, и в чём разница?",
            "preventDefault() отменяет действие по умолчанию у "
            "элемента: для <form> submit — отменить отправку "
            "формы и обновление страницы; для <a> click — "
            "отменить переход по ссылке; в dragover — "
            "разрешить drop. Не влияет на распространение "
            "события дальше. stopPropagation() — останавливает "
            "распространение события: запрещает родительским "
            "обработчикам сработать. stopImmediatePropagation() "
            "дополнительно блокирует другие обработчики на этом "
            "же элементе. Их часто используют вместе: "
            "preventDefault() для отмены поведения, "
            "stopPropagation() для предотвращения «случайного» "
            "вызова обработчиков на родителях.",
        ),
        (
            "В чём отличие setTimeout от setInterval, и как их корректно отменить?",
            "setTimeout(fn, ms) — выполняет fn один раз через "
            "ms миллисекунд. setInterval(fn, ms) — повторяет "
            "вызов fn каждые ms миллисекунд бесконечно. Обе "
            "функции возвращают идентификатор таймера. Для "
            "отмены: clearTimeout(id) или clearInterval(id). "
            "Важно: setInterval может «накапливаться», если "
            "функция выполняется дольше интервала; для длинных "
            "задач безопаснее рекурсивный setTimeout. В задании "
            "3 (таймер) используется setInterval с явным "
            "clearInterval по «Пауза» и «Сброс»; в задании 6 — "
            "setTimeout для отложенного появления попапа.",
        ),
        (
            "Какова последовательность событий Drag & Drop и зачем preventDefault в dragover?",
            "Последовательность: 1) dragstart — на источнике, "
            "при начале перетаскивания; здесь обычно вызывают "
            "event.dataTransfer.setData('text/plain', value); "
            "2) dragenter — при входе в потенциальную цель; "
            "3) dragover — постоянно при движении над целью "
            "(каждые ~ 350мс); 4) dragleave — при покидании "
            "цели; 5) drop — при отпускании на цели; 6) dragend "
            "— на источнике, после успешного или неудачного "
            "drop. preventDefault() в dragover обязателен, "
            "потому что по умолчанию браузер запрещает дроп — "
            "без отмены этого поведения событие drop не "
            "сработает. Это самая частая ошибка при работе с "
            "Drag & Drop API.",
        ),
        (
            "Чем mouseenter отличается от mouseover, и почему предпочитают первый?",
            "mouseover срабатывает при наведении на элемент И "
            "при переходе курсора между его дочерними "
            "элементами (всплывает). mouseenter срабатывает "
            "только один раз при входе в элемент и не "
            "всплывает; не реагирует на перемещения внутри. "
            "Аналогично mouseout vs mouseleave. На практике "
            "mouseenter/mouseleave удобнее для эффектов "
            "наведения с дочерними элементами — например, в "
            "задании 4 (галерея) при наведении на фигуру с "
            "вложенным SVG: mouseover срабатывал бы каждый раз "
            "при переходе с SVG на родителя и обратно, а "
            "mouseenter — один раз на вход.",
        ),
    ]
    for i, (q, a) in enumerate(QA, start=1):
        add_qa(doc, i, q, a)

    # === Выводы ===
    add_page_break(doc)
    add_heading(doc, "Выводы")
    add_para(
        doc,
        "В работе закреплены ключевые типы DOM-событий: мышиные "
        "(click, dblclick, contextmenu, mouseenter/mouseleave/"
        "mousemove), клавиатурные (keydown для Escape и Enter), "
        "Drag & Drop (dragstart/dragover/drop/dragend), события "
        "формы (submit, blur, input) и таймерные (setInterval, "
        "setTimeout) в связке с DOMContentLoaded. Делегирование "
        "позволило обойтись минимальным числом обработчиков в "
        "сложных интерфейсах (задания 5 и 7).",
    )
    add_para(
        doc,
        "Для задания 7 продемонстрировано, как полностью заменить "
        "CSS-псевдоклассы JavaScript-эффектами через классы "
        "состояний (.is-hover, .is-dragover, .is-success, "
        ".is-error). Это полезный паттерн для случаев, когда нужно "
        "управлять состоянием не «навёлся ли курсор», а «активна "
        "ли drop-зона прямо сейчас» — псевдоклассы такой "
        "семантики не дают, JS-классы — дают.",
    )

    # === Полные листинги JS ===
    add_page_break(doc)
    add_heading(doc, "Полные текстовые листинги JavaScript")
    for jsname, cap in [
        ("01-nav-modal-timer.js", "Листинг 16 — js/01-nav-modal-timer.js"),
        ("04-gallery.js", "Листинг 17 — js/04-gallery.js"),
        ("05-products-table.js", "Листинг 18 — js/05-products-table.js"),
        ("06-help-popup.js", "Листинг 19 — js/06-help-popup.js"),
        ("07-students-dnd.js", "Листинг 20 — js/07-students-dnd.js"),
    ]:
        add_listing(doc, read_js(jsname), caption=cap)

    out = ROOT / "docs" / "reports" / "lab_05" / "Ковалев Д.П. ВКБ43 5 лаба.docx"
    save(doc, out)
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
