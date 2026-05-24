"""Отчёт по лаб 1 — поиск fault в Java + Normal Boundary Value Testing."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from report_builder import (  # noqa: E402
    LabMeta,
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

LAB_DIR = ROOT / "1" / "firstLaboratory"
SCREENS = ROOT / "docs" / "screenshots" / "lab_01"


def read_source(rel: str) -> str:
    return (LAB_DIR / "src" / rel).read_text(encoding="utf-8")


def main() -> None:
    meta = LabMeta(
        number=1,
        title="Поиск fault в коде, исправление ошибки и разработка тест-кейсов",
    )
    doc = make_doc()
    add_title_page(doc, meta)
    add_page_break(doc)

    # === Тема и цель ===
    add_heading(doc, "Тема и цель работы")
    add_para(
        doc,
        "Тема: поиск fault в исходном коде на языке Java, исправление дефекта "
        "и разработка тест-кейсов для покрытия как «скрывающих» баг входов, "
        "так и тех, что приводят к видимому отказу (failure).",
    )
    add_para(
        doc,
        "Цель работы: освоить терминологию модели «fault → error → failure» "
        "(Goodenough/Hoare, ISTQB), научиться локализовать дефекты по чтению "
        "исходного кода, спроектировать набор test cases по методу Normal "
        "Boundary Value Testing (4·n + 1 кейсов) и реализовать "
        "автоматизированный прогон на JUnit 5 через Maven Surefire.",
    )

    # === Условие задания ===
    add_heading(doc, "Условие задания", level=2)
    add_para(doc, "Задание №1. Дан Java-метод подсчёта нечётных или положительных элементов массива:")
    add_listing(
        doc,
        "public static int oddOrPos(int[] x) {\n"
        "    int count = 0;\n"
        "    for (int i = 0; i < x.length; i++) {\n"
        "        if (x[i] % 2 == 1 || x[i] > 0) {\n"
        "            count++;\n"
        "        }\n"
        "    }\n"
        "    return count;\n"
        "}",
        caption="Листинг 1 — исходный метод с fault (по заданию №1)",
    )
    add_para(
        doc,
        "Требуется: (а) определить, где именно располагается fault, и предложить "
        "исправление; (б) описать test cases, которые не выполняют fault — то есть "
        "не приводят к видимому отличию от корректной реализации.",
    )
    add_para(
        doc,
        "Задание №2. Спроектировать тест-кейсы методом Normal Boundary Value "
        "Testing для следующей спецификации:",
    )
    add_listing(
        doc,
        "This method finds the area of a regular quadrilateral.\n"
        "Parameters:\n"
        "  side1 is the length of the one side.\n"
        "  side2 is the length of the second side.\n"
        "Returns: it returns the area of the shape.\n"
        "@pre 0 <= side1 <= 100\n"
        "@pre 0 <= side2 <= 100",
        caption="Листинг 2 — спецификация метода area (по заданию №2)",
    )

    # === Терминология ===
    add_page_break(doc)
    add_heading(doc, "Используемая терминология")
    add_para(
        doc,
        "Согласно классической модели Goodenough/Hoare и определениям ISTQB "
        "различают три понятия:",
    )
    add_table_simple(
        doc,
        [
            ["Термин", "Значение"],
            ["Fault (дефект)", "Статический недостаток в коде — неверная конструкция, выражение, условие."],
            ["Error (ошибка)", "Несоответствующее правильному внутреннее состояние программы, возникающее при выполнении дефектного участка."],
            ["Failure (отказ)", "Внешне наблюдаемое неправильное поведение программы — несоответствие фактического результата ожидаемому."],
        ],
        caption="Таблица 1 — fault / error / failure",
    )
    add_para(
        doc,
        "Тест-кейс «выполняет fault» означает, что входные данные приводят к "
        "исполнению дефектной строки. При этом он не обязательно превращает "
        "fault в failure — для этого ошибка («error») должна распространиться "
        "до выхода функции и проявиться в наблюдаемом результате (модель "
        "RIPR: Reachability — Infection — Propagation — Revealability).",
    )

    # === Задание №1 ===
    add_page_break(doc)
    add_heading(doc, "Задание №1. Локализация и исправление fault")
    add_para(doc, "Дефектной является строка с условием:")
    add_listing(doc, "if (x[i] % 2 == 1 || x[i] > 0) {")
    add_para(
        doc,
        "Точка fault — левая часть дизъюнкции «x[i] % 2 == 1». Цель проверки — "
        "определить нечётность. Но в Java оператор % для отрицательных "
        "операндов возвращает отрицательный остаток (JLS §15.17.3):",
    )
    add_listing(doc, "(a / b) * b + (a % b) == a")
    add_para(doc, "Из этого следует таблица значений:")
    add_table_simple(
        doc,
        [
            ["x[i]", "x[i] % 2", "x[i] % 2 == 1"],
            ["3", "1", "true"],
            ["-3", "-1", "false ← ошибка"],
            ["-1", "-1", "false ← ошибка"],
            ["-7", "-1", "false ← ошибка"],
        ],
        caption="Таблица 2 — поведение оператора % для отрицательных чисел",
    )
    add_para(
        doc,
        "Метод пропускает все отрицательные нечётные элементы, хотя по контракту "
        "JavaDoc должен их учитывать («count of odd or positive elements in x»).",
    )
    add_para(doc, "Минимальное и идиоматичное исправление — проверка на «не равен нулю»:")
    add_listing(doc, "if (x[i] % 2 != 0 || x[i] > 0) {")
    add_para(
        doc,
        "Условие «x[i] % 2 != 0» истинно для любого нечётного целого независимо "
        "от знака, что и требуется. Альтернативы — Math.abs(x[i] % 2) == 1, "
        "Math.floorMod(x[i], 2) == 1 или битовая проверка (x[i] & 1) == 1.",
    )

    add_heading(doc, "Демонстрация fault на реальных данных", level=2)
    add_para(
        doc,
        "В классе Main собрано пять характерных массивов с параллельным "
        "вызовом багованной и исправленной версии. Видно, что для отрицательных "
        "нечётных входов результаты расходятся:",
    )
    add_image(doc, SCREENS / "02_main_demo.png", caption="Рисунок 1 — вывод программы Main")

    add_heading(doc, "Задание №1(б). Тест-кейсы, НЕ выполняющие fault", level=2)
    add_para(
        doc,
        "Тест-кейс не выполняет fault, если на нём результат багованной "
        "реализации совпадает с эталонной. Возможны пять характерных ситуаций:",
    )
    add_table_simple(
        doc,
        [
            ["№", "Вход x", "oddOrPos", "fixed", "Почему fault скрыт"],
            ["1", "{}", "0", "0", "Цикл не выполняется ни одной итерации."],
            ["2", "{0, 1, 2, 3, 4, 5}", "5", "5", "Для положительных нечётных «% == 1» работает верно; для чётных срабатывает «>0»."],
            ["3", "{1, 3, 5, 7}", "4", "4", "Положительные нечётные «прикрывает» ветка «x[i] > 0»."],
            ["4", "{-2, -4, -6, -8}", "0", "0", "Дефектное условие достигнуто (reachability есть), но даёт корректный false на каждом элементе (нет infection)."],
            ["5", "{0, 0, 0}", "0", "0", "Аналогично кейсу 4: оба подусловия ложны."],
        ],
        caption="Таблица 3 — пять тест-кейсов, не выполняющих fault",
    )
    add_para(
        doc,
        "Обобщение: fault не превращается в failure тогда и только тогда, когда "
        "массив не содержит отрицательных нечётных элементов. Иначе говоря, "
        "чтобы тест выполнил fault и привёл к видимому отказу, входной массив "
        "должен содержать хотя бы одно число вида 2k − 1, k ≤ 0 (например −1, "
        "−3, −5).",
    )

    add_heading(doc, "Тест-кейсы, ВЫПОЛНЯЮЩИЕ fault (для проверки фикса)", level=2)
    add_table_simple(
        doc,
        [
            ["№", "Вход x", "Ожидание", "oddOrPos (баг)", "Разница"],
            ["1", "{-3}", "1", "0", "−1"],
            ["2", "{-1, -3, -5, -7}", "4", "0", "−4"],
            ["3", "{-3, -1, 0, 1, 2, 3}", "5", "3", "−2"],
            ["4", "{Integer.MIN_VALUE + 1}", "1", "0", "−1"],
        ],
        caption="Таблица 4 — четыре тест-кейса, демонстрирующих failure",
    )
    add_para(
        doc,
        "Эти кейсы реализованы во вложенном классе FaultTriggered тестового "
        "файла OddOrPosTest.java. Каждый кейс одновременно служит регрессионным "
        "тестом для исправленной версии oddOrPosFixed.",
    )

    # === Задание №2 ===
    add_page_break(doc)
    add_heading(doc, "Задание №2. Normal Boundary Value Testing для area")
    add_para(
        doc,
        "Boundary Value Analysis (BVA) — методика чёрного ящика, выбирающая "
        "тестовые значения на «краях» области допустимых входов, где "
        "исторически сосредоточена бо́льшая часть ошибок (off-by-one, неверные "
        "сравнения < vs ≤, неверная инициализация). Различают четыре формы BVA:",
    )
    add_table_simple(
        doc,
        [
            ["Форма", "Значения переменной", "Число кейсов (n переменных)"],
            ["Normal BVT", "min, min⁺, nom, max⁻, max (только in-range)", "4·n + 1"],
            ["Robust BVT", "Normal + min⁻, max⁺ (out-of-range)", "6·n + 1"],
            ["Worst-case BVT", "декартово произведение 5 значений каждой переменной", "5ⁿ"],
            ["Robust Worst-case BVT", "то же, но 7 значений", "7ⁿ"],
        ],
        caption="Таблица 5 — основные формы BVA",
    )
    add_para(
        doc,
        "В Normal BVT действует принцип «single fault assumption»: предполагается, "
        "что отказ вызывает изменение одной переменной за раз. Поэтому в каждом "
        "кейсе одна переменная варьируется через все 5 граничных значений, а "
        "остальные фиксируются на nominal-значении.",
    )

    add_heading(doc, "Граничные точки для area", level=2)
    add_para(doc, "Для каждой из двух переменных side1, side2 ∈ [0, 100] выбираем 5 значений:")
    add_table_simple(
        doc,
        [
            ["Метка", "Значение"],
            ["min", "0"],
            ["min⁺", "1"],
            ["nom", "50"],
            ["max⁻", "99"],
            ["max", "100"],
        ],
        caption="Таблица 6 — граничные точки",
    )
    add_para(doc, "Число тест-кейсов: 4 · n + 1 = 4 · 2 + 1 = 9.")

    add_heading(doc, "Полный набор Normal BVT тест-кейсов", level=2)
    add_table_simple(
        doc,
        [
            ["TC #", "side1", "метка side1", "side2", "метка side2", "Ожидание area"],
            ["TC-1", "0", "min", "50", "nom", "0"],
            ["TC-2", "1", "min⁺", "50", "nom", "50"],
            ["TC-3", "50", "nom", "50", "nom", "2500"],
            ["TC-4", "99", "max⁻", "50", "nom", "4950"],
            ["TC-5", "100", "max", "50", "nom", "5000"],
            ["TC-6", "50", "nom", "0", "min", "0"],
            ["TC-7", "50", "nom", "1", "min⁺", "50"],
            ["TC-8", "50", "nom", "99", "max⁻", "4950"],
            ["TC-9", "50", "nom", "100", "max", "5000"],
        ],
        caption="Таблица 7 — 9 NBVT-кейсов для метода area",
    )
    add_para(
        doc,
        "Графически набор образует «крест» из двух пробегов по 5 точек, "
        "пересекающихся в центральной точке (TC-3, side1 = side2 = 50). "
        "Все 9 кейсов реализованы одним параметризованным тестом "
        "QuadrilateralTest$NormalBoundaryValue через @ParameterizedTest + @CsvSource.",
    )

    add_heading(doc, "Дополнительные кейсы вне Normal BVT", level=2)
    add_para(
        doc,
        "Хотя Normal BVT строго ограничен только in-range значениями, для полноты "
        "контракта добавлены 4 кейса на нарушение пред-условий (элементы Robust BVT). "
        "Они проверяют, что метод корректно бросает IllegalArgumentException.",
    )
    add_table_simple(
        doc,
        [
            ["Кейс", "side1", "side2", "Ожидаемое поведение"],
            ["RC-1", "-1", "50", "IllegalArgumentException"],
            ["RC-2", "101", "50", "IllegalArgumentException"],
            ["RC-3", "50", "-1", "IllegalArgumentException"],
            ["RC-4", "50", "101", "IllegalArgumentException"],
        ],
        caption="Таблица 8 — 4 robust-кейса на нарушение пред-условий",
    )

    # === Программная проверка ===
    add_page_break(doc)
    add_heading(doc, "Программная проверка")
    add_para(
        doc,
        "Проект собран Maven 3.x, тесты написаны на JUnit 5 (Jupiter). Полный "
        "прогон через «mvn test» выполняет 22 теста (5 + 4 на oddOrPos, 9 + 4 "
        "на area) и завершается успешно:",
    )
    add_image(doc, SCREENS / "01_mvn_test_full.png", caption="Рисунок 2 — успешный прогон mvn test (22 теста)")

    # === Листинги через freeze ===
    add_page_break(doc)
    add_heading(doc, "Листинги исходного кода (с подсветкой)")
    add_para(
        doc,
        "Ниже приведены исходные файлы основного кода и тестов в виде "
        "оформленных снимков с подсветкой синтаксиса Java.",
    )
    add_image(doc, SCREENS / "03_OddOrPos_java.png", caption="Рисунок 3 — OddOrPos.java (бажная + исправленная версия)")
    add_image(doc, SCREENS / "04_Quadrilateral_java.png", caption="Рисунок 4 — Quadrilateral.java (метод area + проверка пред-условий)")
    add_image(doc, SCREENS / "05_OddOrPosTest_java.png", caption="Рисунок 5 — OddOrPosTest.java (тесты задания №1)")
    add_image(doc, SCREENS / "06_QuadrilateralTest_java.png", caption="Рисунок 6 — QuadrilateralTest.java (Normal BVT)")

    # === Контрольные вопросы ===
    add_page_break(doc)
    add_heading(doc, "Контрольные вопросы")
    QA = [
        (
            "В чём разница между fault, error и failure?",
            "Fault — статический дефект в коде (неверная конструкция/условие/выражение). "
            "Error — некорректное промежуточное состояние программы, возникающее "
            "при исполнении дефектного места. Failure — внешне наблюдаемый отказ, "
            "когда результат программы не совпадает с ожидаемым. Цепочка RIPR "
            "(Reachability → Infection → Propagation → Revealability) требует, "
            "чтобы для каждой стадии выполнялось своё условие; нарушение хотя бы "
            "одного звена «маскирует» fault.",
        ),
        (
            "Почему «x % 2 == 1» некорректно проверяет нечётность в Java?",
            "В Java оператор % сохраняет знак делимого: согласно JLS §15.17.3, "
            "(a/b)·b + (a%b) == a. Поэтому (-3) % 2 == -1, (-1) % 2 == -1 и т.д. — "
            "ни одно отрицательное нечётное число не равно остатку 1. Корректная "
            "идиома — «x % 2 != 0» или Math.floorMod(x, 2) == 1 (последний всегда "
            "возвращает неотрицательный остаток).",
        ),
        (
            "Зачем нужен метод Normal Boundary Value Testing и почему именно 4n+1 кейсов?",
            "BVA эксплуатирует эмпирическое наблюдение, что ошибки сосредоточены "
            "на границах областей. Normal BVT под single-fault-assumption "
            "варьирует каждую переменную по 5 значениям {min, min⁺, nom, max⁻, max}, "
            "а остальные фиксирует на nominal. Для n переменных получаем 5 значений "
            "× n переменных = 5n, но центральная точка (nom, …, nom) общая для всех "
            "крестов, поэтому 5n − (n − 1) = 4n + 1.",
        ),
        (
            "В чём отличие Normal BVT от Robust BVT и Worst-case BVT?",
            "Normal — только in-range значения, 4n+1 кейсов. Robust — добавляет "
            "min⁻ и max⁺ (out-of-range), 6n+1 кейсов, тестирует обработку нарушенных "
            "пред-условий. Worst-case — декартово произведение всех 5 значений каждой "
            "переменной, 5ⁿ кейсов, отказывается от single-fault-assumption. Robust "
            "Worst-case — декартово произведение из 7 значений (с out-of-range), 7ⁿ.",
        ),
        (
            "Что такое «параметризованный тест» в JUnit 5 и зачем он нужен?",
            "Это конструкция @ParameterizedTest + источник данных (@ValueSource, "
            "@CsvSource, @MethodSource), которая выполняет один и тот же метод теста "
            "для каждого набора параметров. Применительно к BVT-таблицам это даёт "
            "компактный код (один метод вместо 9), наглядный per-case отчёт surefire "
            "(каждый запуск — отдельная строка с описанием) и упрощает сопровождение: "
            "новый граничный кейс добавляется одной строкой CSV.",
        ),
    ]
    for i, (q, a) in enumerate(QA, start=1):
        add_qa(doc, i, q, a)

    # === Выводы ===
    add_page_break(doc)
    add_heading(doc, "Выводы")
    add_para(
        doc,
        "По заданию №1: дефект «x[i] % 2 == 1» локализован в условии цикла; "
        "причина — некорректное предположение о знаке остатка от деления в Java "
        "для отрицательных чисел. Минимальный фикс — замена «== 1» на «!= 0», "
        "восстанавливающая семантику нечётности для любого знака. Выделены пять "
        "тест-кейсов, не выполняющих fault (пустой массив, только неотрицательные, "
        "только положительные нечётные, только отрицательные чётные, только нули) — "
        "общий критерий «отсутствие отрицательных нечётных». Параллельно реализованы "
        "четыре тест-кейса, выполняющих fault и приводящих к failure, в том числе "
        "граничный Integer.MIN_VALUE + 1.",
    )
    add_para(
        doc,
        "По заданию №2: для метода area построен полный набор Normal BVT — 9 кейсов "
        "по формуле 4·n + 1 (n = 2). Граничные точки 0, 1, 50, 99, 100 покрывают "
        "минимум, минимум-плюс, номинальное, максимум-минус и максимум области "
        "значений [0, 100]. Дополнительно реализованы 4 robust-кейса на нарушение "
        "пред-условий, проверяющие правильное возбуждение IllegalArgumentException.",
    )
    add_para(
        doc,
        "Все 22 теста (5 FaultNotTriggered + 4 FaultTriggered + 9 NormalBoundaryValue "
        "+ 4 PreconditionViolations) проходят успешно при запуске mvn test. Отчёт "
        "Surefire подтверждает: Tests run: 22, Failures: 0, Errors: 0, Skipped: 0.",
    )

    # === Полный листинг исходного кода (текст) ===
    add_page_break(doc)
    add_heading(doc, "Полный листинг исходного кода")
    add_para(
        doc,
        "Ниже приведены полные исходники проекта в текстовой форме (для удобства "
        "копирования и проверки преподавателем).",
    )
    for caption, rel in [
        ("Листинг 3 — src/main/java/org/cequalz/OddOrPos.java", "main/java/org/cequalz/OddOrPos.java"),
        ("Листинг 4 — src/main/java/org/cequalz/Quadrilateral.java", "main/java/org/cequalz/Quadrilateral.java"),
        ("Листинг 5 — src/main/java/org/cequalz/Main.java", "main/java/org/cequalz/Main.java"),
        ("Листинг 6 — src/test/java/org/cequalz/OddOrPosTest.java", "test/java/org/cequalz/OddOrPosTest.java"),
        ("Листинг 7 — src/test/java/org/cequalz/QuadrilateralTest.java", "test/java/org/cequalz/QuadrilateralTest.java"),
    ]:
        add_listing(doc, read_source(rel), caption=caption)

    out = ROOT / "docs" / "reports" / "lab_01" / "Ковалев Д.П. ВКБ43 1 лаба.docx"
    save(doc, out)
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
