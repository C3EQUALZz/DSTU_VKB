"""Отчёт по лаб 2 — знакомство с pytest, classify_triangle с поиском дефектов."""

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

LAB_DIR = ROOT / "2"
SCREENS = ROOT / "docs" / "screenshots" / "lab_02"


def read_source(rel: str) -> str:
    return (LAB_DIR / rel).read_text(encoding="utf-8")


def main() -> None:
    meta = LabMeta(
        number=2,
        title="Знакомство с pytest. Проектирование тестов и поиск логических ошибок в коде",
    )
    doc = make_doc()
    add_title_page(doc, meta)
    add_page_break(doc)

    add_heading(doc, "Тема и цель работы")
    add_para(
        doc,
        "Тема: знакомство с библиотекой pytest, проектирование тестов и "
        "поиск логических ошибок в функции классификации треугольника.",
    )
    add_para(
        doc,
        "Цель работы: научиться выявлять логические дефекты в исходном коде, "
        "проектировать тест-кейсы по эквивалентным классам и параметризованным "
        "источникам данных, установить и использовать pytest через uv, добиться "
        "покрытия всех ветвей и граничных случаев исправленной функции.",
    )

    add_heading(doc, "Условие задания", level=2)
    add_para(
        doc,
        "Дана функция определения типа треугольника по трём сторонам. Исходная "
        "реализация:",
    )
    add_listing(
        doc,
        'def classify_triangle(a, b, c):\n'
        '    """\n'
        '    Классифицирует треугольник по трём сторонам.\n'
        '    Возвращает:\n'
        '        - "Equilateral"  : равносторонний\n'
        '        - "Isosceles"    : равнобедренный (но не равносторонний)\n'
        '        - "Scalene"      : разносторонний\n'
        '        - "InvalidInput" : недопустимый ввод (<= 0 или не int)\n'
        '    """\n'
        '    if not all(isinstance(side, int) for side in (a, b, c)):\n'
        '        return "InvalidInput"\n'
        '    if any(side <= 0 for side in (a, b, c)):\n'
        '        return "InvalidInput"\n'
        '    if a == b == c:\n'
        '        return "Равносторонний"\n'
        '    elif a == b or b == c or a == c:\n'
        '        return "Равнобедренный"\n'
        '    else:\n'
        '        return "Разносторонний"\n\n'
        'if __name__ == "__main__":\n'
        '    print(classify_triangle(7, 7, 14))',
        caption="Листинг 1 — исходный код функции (по заданию)",
    )
    add_para(
        doc,
        "Задачи: (1) определить, какие проверки необходимо добавить, чтобы "
        "функция корректно обрабатывала все возможные варианты входных данных "
        "(подсказка из задания: не каждый набор значений соответствует "
        "треугольнику); (2) реализовать функцию с учётом необходимых "
        "исправлений; (3) установить pytest и составить полный набор "
        "тест-кейсов.",
    )

    # === Задание 1 — три дефекта ===
    add_page_break(doc)
    add_heading(doc, "Задание 1. Какие дефекты есть и что нужно добавить")
    add_para(
        doc,
        "В исходной реализации обнаруживается три логических дефекта разной "
        "степени критичности.",
    )

    add_heading(doc, "Дефект 1 — отсутствует проверка неравенства треугольника", level=2)
    add_para(
        doc,
        "Геометрически треугольник существует только тогда, когда сумма длин "
        "любых двух сторон строго больше длины третьей стороны:",
    )
    add_listing(doc, "a + b > c   и   a + c > b   и   b + c > a")
    add_para(
        doc,
        "Прямо в задании приведён канонический пример нарушения: "
        "classify_triangle(7, 7, 14) возвращает «Равнобедренный», хотя 7 + 7 = 14 "
        "(точки лежат на одной прямой — вырожденный треугольник). Также невалидны "
        "(1, 2, 10), (5, 5, 10), (100, 1, 1) и любые другие наборы, для которых "
        "хотя бы одно неравенство нарушено — функция выдаёт ложно-валидный тип "
        "вместо InvalidInput. Что добавить:",
    )
    add_listing(doc, "if a + b <= c or a + c <= b or b + c <= a:\n    return \"InvalidInput\"")
    add_para(
        doc,
        "Знак «≤» важен: равенство (a + b == c) даёт вырожденный треугольник с "
        "нулевой площадью, который тоже нельзя классифицировать как обычный.",
    )

    add_heading(doc, "Дефект 2 — рассогласование docstring и реальных return-значений", level=2)
    add_table_simple(
        doc,
        [
            ["Тип", "По docstring", "Фактически возвращается"],
            ["Равносторонний", "Equilateral", "Равносторонний"],
            ["Равнобедренный", "Isosceles", "Равнобедренный"],
            ["Разносторонний", "Scalene", "Разносторонний"],
        ],
        caption="Таблица 1 — двойственность спецификации",
    )
    add_para(
        doc,
        "В исправленной версии реализация приведена к docstring (английские "
        "строки) — так контракт остаётся тем же, что был задокументирован.",
    )

    add_heading(doc, "Дефект 3 — bool пропускается как валидный int", level=2)
    add_para(
        doc,
        "В Python bool — подкласс int, поэтому isinstance(True, int) == True. "
        "Из-за этого classify_triangle(True, True, True) без претензий возвращает "
        "«Равносторонний» (стороны со значением 1, 1, 1). С точки зрения "
        "семантики «длина стороны треугольника» это некорректный ввод. "
        "Что добавить — явная фильтрация bool до проверки isinstance(..., int):",
    )
    add_listing(
        doc,
        "for side in (a, b, c):\n"
        "    if isinstance(side, bool) or not isinstance(side, int):\n"
        "        return \"InvalidInput\"",
    )

    add_heading(doc, "Сводная таблица дефектов", level=2)
    add_table_simple(
        doc,
        [
            ["№", "Дефект", "Демонстрация", "Класс ошибки"],
            ["1", "Нет неравенства треугольника", "(7,7,14) → «Равнобедренный»", "Missing case"],
            ["2", "Расхождение docstring/реализации", "(5,5,5) → «Равносторонний» вместо «Equilateral»", "Spec/impl mismatch"],
            ["3", "bool проходит как int", "(True,True,True) → «Равносторонний»", "Слабая проверка типа"],
        ],
        caption="Таблица 2 — три дефекта оригинальной функции",
    )

    # === Демонстрация ===
    add_page_break(doc)
    add_heading(doc, "Демонстрация дефектов и исправлений")
    add_para(
        doc,
        "Ниже параллельный запуск legacy- и fixed-версий для пяти показательных "
        "входов. Видно, как (7,7,14), (1,2,10) и (True,True,True) выдают разные "
        "результаты, а для корректных треугольников (5,5,5) и (3,4,5) отличается "
        "только язык метки.",
    )
    add_image(doc, SCREENS / "04_demo_compare.png", caption="Рисунок 1 — сравнение legacy vs fixed на ключевых входах")
    add_image(doc, SCREENS / "05_legacy_py.png", caption="Рисунок 2 — исходник второй_laboratory/legacy.py (с тремя fault)")
    add_image(doc, SCREENS / "06_triangle_py.png", caption="Рисунок 3 — исходник второй_laboratory/triangle.py (исправленная версия)")

    # === Задание 3 — pytest ===
    add_page_break(doc)
    add_heading(doc, "Задание 3. Набор тест-кейсов в pytest")
    add_para(
        doc,
        "Все тесты — в каталоге tests/unit/. Полный набор состоит из 69 тест-кейсов, "
        "разбитых на 2 файла и 11 классов. Тесты построены через "
        "@pytest.mark.parametrize — это даёт компактный код и подробный per-case "
        "отчёт.",
    )
    add_table_simple(
        doc,
        [
            ["Файл / класс", "Покрытие"],
            ["test_triangle.py :: TestEquilateral", "(s, s, s) для разных s — от 1 до 10⁶"],
            ["test_triangle.py :: TestIsosceles", "Две равные стороны во всех 3 позициях (a==b, b==c, a==c)"],
            ["test_triangle.py :: TestScalene", "Пифагоровы тройки и обычные разносторонние"],
            ["test_triangle.py :: TestInvalidType", "Строки, float, None, list, object, bool в 3 положениях"],
            ["test_triangle.py :: TestNonPositive", "Нули и отрицательные числа в каждой позиции"],
            ["test_triangle.py :: TestTriangleInequality", "Вырожденные (a+b==c) и невозможные (a+b<c) во всех 3 положениях"],
            ["test_triangle.py :: TestArgumentOrderInvariance", "Результат не зависит от порядка аргументов (все 6 перестановок)"],
            ["test_triangle.py :: TestBoundary", "Минимальный (1,1,1), очень большие 10⁹, smoke-таблица"],
            ["test_legacy_fault.py :: TestLegacyDegenerateTriangleBug", "Фиксирует, что legacy неверно классифицирует (7,7,14) и (1,2,10)"],
            ["test_legacy_fault.py :: TestLegacyDocstringMismatch", "Фиксирует расхождение возвращаемых меток legacy с docstring"],
            ["test_legacy_fault.py :: TestLegacyBoolBug", "Фиксирует, что legacy пропускает bool, а fixed отвергает"],
        ],
        caption="Таблица 3 — структура тестового набора (11 классов, 69 тестов)",
    )

    add_heading(doc, "Принцип работы legacy-тестов", level=2)
    add_para(
        doc,
        "Эти тесты НЕ являются регрессией функционала — это «золотой стандарт» "
        "дефекта. Ожидаемое значение в assert — это фактическое (неверное) поведение "
        "оригинальной функции; рядом в тесте сравнивается с правильным "
        "поведением исправленной версии. Каждый дефект из таблицы 2 превращается "
        "в пару тестов «есть в legacy / исправлено в triangle».",
    )

    # === Прогон тестов ===
    add_page_break(doc)
    add_heading(doc, "Прогон тестов")
    add_para(
        doc,
        "Базовая команда uv run pytest выдаёт сжатый отчёт с итоговым числом "
        "пройденных тестов:",
    )
    add_image(doc, SCREENS / "01_pytest_summary.png", caption="Рисунок 4 — успешный прогон uv run pytest (69 passed)")

    add_para(
        doc,
        "С флагом -v и переопределением addopts (для перебивки «-q» из pyproject.toml) "
        "виден per-case отчёт по каждому параметризованному кейсу. Пример — все "
        "11 тестов TestTriangleInequality:",
    )
    add_image(doc, SCREENS / "02_pytest_inequality.png", caption="Рисунок 5 — подробный прогон TestTriangleInequality")

    add_para(
        doc,
        "Прогон legacy-fault тестов отдельно подтверждает, что все три дефекта "
        "зафиксированы и что фикс ведёт себя ожидаемо иначе:",
    )
    add_image(doc, SCREENS / "03_pytest_legacy_fault.png", caption="Рисунок 6 — подробный прогон test_legacy_fault.py")

    # === Тесты как код ===
    add_page_break(doc)
    add_heading(doc, "Листинги тестового кода")
    add_image(doc, SCREENS / "07_test_triangle_py.png", caption="Рисунок 7 — test_triangle.py (8 классов, 60 тестов)")
    add_image(doc, SCREENS / "08_test_legacy_fault_py.png", caption="Рисунок 8 — test_legacy_fault.py (3 класса, 9 тестов)")

    # === Контрольные вопросы ===
    add_page_break(doc)
    add_heading(doc, "Контрольные вопросы")
    QA = [
        (
            "Что такое pytest и в чём его преимущества перед unittest?",
            "Pytest — современный фреймворк функционального и unit-тестирования "
            "для Python. Преимущества: тесты — обычные функции (а не методы "
            "классов TestCase); один assert вместо assertEqual/assertTrue (с "
            "автоматическим introspection ошибочного выражения); богатая "
            "параметризация через @parametrize; фикстуры с DI через имя аргумента "
            "(чище setUp/tearDown); огромный плагин-экосистема (cov, xdist, "
            "asyncio, html); подробный отчёт с цветом и группировкой.",
        ),
        (
            "Как pytest узнаёт, что функция/класс/файл — это тест?",
            "По соглашениям об именах (автоматическое discovery): файлы test_*.py "
            "или *_test.py, классы, начинающиеся с Test (без __init__), функции "
            "и методы, начинающиеся с test_. Корневая директория поиска задаётся "
            "опцией testpaths в pyproject.toml; путь поиска можно изменить через "
            "pyproject/conftest. Также можно явно указывать тесты по узлу: "
            "pytest path/to/file.py::ClassName::test_method.",
        ),
        (
            "Зачем нужна параметризация (@parametrize) и чем она лучше цикла внутри теста?",
            "Параметризация запускает один и тот же метод теста для каждого набора "
            "входов как ОТДЕЛЬНЫЙ тест-кейс — со своим именем, своим статусом "
            "pass/fail и отдельной строкой в отчёте. Это даёт: (а) видимость "
            "какой именно ввод сломал тест (а не «упало в цикле — где?»); "
            "(б) корректную статистику покрытия; (в) возможность параллельного "
            "выполнения; (г) компактный код для табличного тестирования (BVT, "
            "ECT, smoke-таблицы).",
        ),
        (
            "Почему важно отдельно отвергать bool, если bool — это int?",
            "Семантически длина стороны треугольника — это положительное целое "
            "число, а bool — это маркер истинности (True/False), который в "
            "Python унаследован от int только из исторических соображений (PEP 3107). "
            "Принимать True как сторону 1, а False как 0 — значит молча "
            "интерпретировать неправильный по контракту ввод. Это типовой "
            "источник скрытых багов; в pyright/mypy эта проблема ловится статически, "
            "но в runtime — только явной проверкой isinstance(side, bool) ДО "
            "проверки isinstance(side, int).",
        ),
        (
            "Что такое неравенство треугольника и почему его нужно проверять строгим знаком?",
            "Неравенство треугольника: для существования треугольника необходимо "
            "и достаточно, чтобы сумма любых двух сторон была строго больше "
            "третьей: a + b > c, a + c > b, b + c > a. Случай равенства (a + b == c) "
            "даёт «вырожденный треугольник» — три точки на одной прямой, площадь "
            "равна нулю. Такой объект формально не треугольник, поэтому проверять "
            "нужно именно «> с возвратом InvalidInput при ≤».",
        ),
    ]
    for i, (q, a) in enumerate(QA, start=1):
        add_qa(doc, i, q, a)

    # === Выводы ===
    add_page_break(doc)
    add_heading(doc, "Выводы")
    add_para(
        doc,
        "Главный пропущенный случай в коде из задания — неравенство треугольника. "
        "Без его проверки функция принимает на вход вырожденные и попросту "
        "несуществующие треугольники и возвращает ложно-валидный тип. "
        "Демонстрация прямо из условия задачи — classify_triangle(7, 7, 14) "
        "возвращает «Равнобедренный».",
    )
    add_para(
        doc,
        "Помимо главного дефекта в коде есть ещё две менее очевидные проблемы: "
        "расхождение docstring и фактических возвращаемых значений, а также "
        "слишком слабая проверка типа — bool пропускается как int. Все три дефекта "
        "устранены в исправленной версии second_laboratory.triangle.classify_triangle.",
    )
    add_para(
        doc,
        "Pytest через uv устанавливается одной командой uv sync и позволяет "
        "компактно описать большой набор кейсов через параметризацию. Финальный "
        "набор — 69 тестов в 11 классах: 8 классов покрывают позитивные и "
        "негативные сценарии исправленной функции, 3 класса фиксируют поведение "
        "legacy-функции на сценариях, где она ошибается. Все 69 тестов проходят "
        "успешно за 0.02 с.",
    )

    # === Полный листинг ===
    add_page_break(doc)
    add_heading(doc, "Полный листинг исходного кода")
    for caption, rel in [
        ("Листинг 2 — src/second_laboratory/legacy.py", "src/second_laboratory/legacy.py"),
        ("Листинг 3 — src/second_laboratory/triangle.py", "src/second_laboratory/triangle.py"),
        ("Листинг 4 — src/second_laboratory/__init__.py", "src/second_laboratory/__init__.py"),
        ("Листинг 5 — tests/unit/test_triangle.py", "tests/unit/test_triangle.py"),
        ("Листинг 6 — tests/unit/test_legacy_fault.py", "tests/unit/test_legacy_fault.py"),
    ]:
        add_listing(doc, read_source(rel), caption=caption)

    out = ROOT / "docs" / "reports" / "lab_02" / "Ковалев Д.П. ВКБ43 2 лаба.docx"
    save(doc, out)
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
