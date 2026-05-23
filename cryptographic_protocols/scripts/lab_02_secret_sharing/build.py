"""Генерация отчётов лаб 2 для всех 28 вариантов с ручным решением.

Для каждого варианта подставляются конкретные доли Шамира и пары (a, b) Блэкли
из таблицы методички; все промежуточные значения (L_j(0), коэффициенты полинома,
c_i, Q) вычисляются на лету в Python и сравниваются с программной реализацией.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "lab_02_secret_sharing"))

from math_helpers import (  # noqa: E402
    blakley_c,
    gauss_blakley,
    gauss_blakley_first_valid,
    gauss_blakley_with_steps,
    gauss_vandermonde_with_steps,
    lagrange_zero,
    reconstruct_polynomial,
)
from report_builder import (  # noqa: E402
    LabMeta,
    add_heading,
    add_listing,
    add_math,
    add_page_break,
    add_para,
    add_qa,
    add_title_page,
    m_frac,
    m_op,
    m_sub,
    m_sup,
    m_text,
    make_doc,
    omml_display,
    save,
)
from variants_data import (  # noqa: E402
    BLAKLEY_LEFT_Q,
    BLAKLEY_RIGHT_Q,
    SHAMIR_LEFT,
    SHAMIR_RIGHT,
    blakley_left_pairs,
    blakley_right_pairs,
)

BIN = ROOT / "target" / "release" / "lab_02_secret_sharing"
CRATE_SRC = ROOT / "crates" / "lab_02_secret_sharing" / "src"


def run_cli(*args: str) -> str:
    env = os.environ.copy()
    env["RUST_LOG"] = "error"
    res = subprocess.run(
        [str(BIN), *args], capture_output=True, text=True, check=True, env=env
    )
    return res.stdout


def read_source(rel: str) -> str:
    return (CRATE_SRC / rel).read_text(encoding="utf-8")


# ----------------- математические вставки для шагов решения -----------------


def m_a_sub(idx: str) -> str:
    return m_sub(m_text("a"), m_text(idx))


def _format_neg(x: int) -> str:
    return f"({x})" if x < 0 else str(x)


# ----------------- блоки отчёта -----------------


def add_lagrange_steps(doc, shares: list[tuple[int, int]], p: int) -> int:
    """Пошаговое восстановление f(0) по интерполяции Лагранжа. Возвращает f(0)."""
    f0, details = lagrange_zero(shares, p)
    for j, xj, yj, num_raw, num_mod, den_raw, den_mod, inv_den, lj0 in details:
        add_para(
            doc,
            f"Шаг {j + 1}. Для (x_{j + 1}, y_{j + 1}) = ({xj}, {yj}):",
            indent=False,
        )
        num_factors = " · ".join(_format_neg(-xk) for k, (xk, _) in enumerate(shares) if k != j)
        den_factors = " · ".join(
            f"({xj}−{xk})" for k, (xk, _) in enumerate(shares) if k != j
        )
        add_math(
            doc,
            omml_display([
                m_sub(m_text("L"), m_text(str(j + 1))),
                m_op("(0) = "),
                m_frac(m_op(num_factors), m_op(den_factors)),
                m_op(f" ≡ "),
                m_frac(m_op(str(num_mod)), m_op(str(den_mod))),
                m_op(f" (mod {p})"),
            ]),
        )
        add_para(
            doc,
            f"Обратный элемент {den_mod}⁻¹ mod {p} = {inv_den}. "
            f"Тогда L_{j + 1}(0) ≡ {num_mod} · {inv_den} ≡ {(num_mod * inv_den) % p} (mod {p}); "
            f"итог: L_{j + 1}(0) = {lj0}.",
            indent=False,
        )
    # Сборка f(0).
    summands = " + ".join(f"{yj}·{d[8]}" for d, (xj, yj) in zip(details, shares))
    total_raw = sum(yj * d[8] for d, (xj, yj) in zip(details, shares))
    add_para(doc, "Сборка секрета f(0):", indent=False)
    add_math(
        doc,
        omml_display([
            m_text("f"),
            m_op(f"(0) = {summands} = {total_raw} ≡ {f0} (mod {p})"),
        ]),
    )
    return f0


def add_polynomial_block(doc, shares: list[tuple[int, int]], p: int) -> list[int]:
    """Восстановление полинома через систему Вандермонда + пошаговый Гаусс."""
    m = len(shares)
    coeffs, steps = gauss_vandermonde_with_steps(shares, p)
    add_para(
        doc,
        f"Восстановим полином f(x) = a₀ + a₁x + … + a_{{{m - 1}}}x^{{{m - 1}}} через "
        f"систему Вандермонда (m = {m} уравнений в Z_{p}):",
    )
    for x, y in shares:
        parts: list[str] = []
        for k in range(m):
            xk = pow(x, k, p)
            if k == 0:
                parts.append(m_a_sub(str(k)))
            else:
                parts.extend([m_op(f" + {xk} · "), m_a_sub(str(k))])
        parts.append(m_op(f" ≡ {y % p} (mod {p})"))
        add_math(doc, omml_display(parts))

    add_para(doc, "Решение методом Гаусса-Жордана в Z_{} (последовательно):".format(p))
    for step in steps:
        add_listing(doc, step)

    poly_terms = []
    for k, a in enumerate(coeffs):
        if k == 0:
            poly_terms.append(str(a))
        elif k == 1:
            poly_terms.append(f"{a}x")
        else:
            poly_terms.append(f"{a}x^{k}")
    add_para(
        doc,
        f"После приведения к ступенчатому виду получаем коэффициенты "
        f"(a₀, …, a_{{{m - 1}}}) = ({', '.join(str(c) for c in coeffs)}). Итоговый полином:",
    )
    add_math(
        doc,
        omml_display([
            m_text("f"),
            m_op(f"(x) = {' + '.join(reversed(poly_terms))} (mod {p})"),
        ]),
    )
    return coeffs


def add_dave_share(doc, coeffs: list[int], p: int, dave_x: int = 2) -> int:
    val = sum(c * pow(dave_x, k, p) for k, c in enumerate(coeffs)) % p
    terms = " + ".join(
        f"{c}·{pow(dave_x, k, p)}" if k > 0 else str(c) for k, c in enumerate(coeffs)
    )
    add_para(doc, f"Доля Дейва — f({dave_x}):", indent=False)
    add_math(
        doc,
        omml_display([
            m_text("f"),
            m_op(f"({dave_x}) = {terms} ≡ {val} (mod {p})"),
        ]),
    )
    add_para(doc, f"Итог: доля Дейва — ({dave_x}, {val}).", indent=False)
    return val


def add_blakley_section(
    doc,
    p: int,
    q: tuple[int, int, int],
    pairs: list[tuple[int, int]],
) -> None:
    names = ["A", "B", "D", "C"]
    add_para(
        doc,
        f"Создаём по 4 доли — плоскости z = a·x + b·y + c, где c = z₀ − a·x₀ − b·y₀ "
        f"(mod {p}) = {q[2]} − {q[0]}·a − {q[1]}·b (mod {p}).",
    )
    planes: list[tuple[int, int, int]] = []
    for name, (a, b) in zip(names, pairs):
        c_raw = q[2] - q[0] * a - q[1] * b
        c = blakley_c(a, b, q, p)
        add_para(
            doc,
            f"Доля {name}: a = {a}, b = {b}. "
            f"c = {q[2]} − {q[0]}·{a} − {q[1]}·{b} = {c_raw} ≡ {c} (mod {p}). "
            f"Плоскость: z = {a}x + {b}y + {c}.",
            indent=False,
        )
        planes.append((a, b, c))

    # Подбираем тройку, на которой Гаусс не вырождается.
    qq, combo = gauss_blakley_first_valid(planes, p)
    trio_names = ", ".join(names[i] for i in combo)
    add_para(
        doc,
        f"Для восстановления Q возьмём тройку {{{trio_names}}}. Система уравнений "
        f"вида ax + by − z ≡ −c (mod {p}):",
    )
    trio = [planes[i] for i in combo]
    for i in combo:
        a, b, c = planes[i]
        add_math(
            doc,
            omml_display([
                m_op(f"{a} x + {b} y − z ≡ {(-c) % p} (mod {p})"),
            ]),
        )
    qq2, steps = gauss_blakley_with_steps(trio, p)
    add_para(doc, "Пошаговое решение методом Гаусса-Жордана в Z_{}:".format(p))
    for step in steps:
        add_listing(doc, step)
    add_para(
        doc,
        f"Из последней матрицы читаем результат: (x, y, z) = "
        f"({qq[0]}, {qq[1]}, {qq[2]}) = Q ✓.",
    )


# ----------------- упражнение 1 (Блэкли пример 1) — одинаковое для всех -----------------


EX1_TEXT = (
    "Из примера 1 методички известны 4 доли в Z₇³, пересекающиеся в Q = (5, 1, 2):\n"
    "• Алиса: z = 5x + 2y + 3;\n"
    "• Боб: z = 2x + 5y + 1;\n"
    "• Кэрол: z = 2x + y + 5;\n"
    "• Дейв: z = 4x + 2y + 1."
)
EX1_TRIPLES = [
    ("а", "Боб, Дейв, Кэрол", [(2, 5, 1), (4, 2, 1), (2, 1, 5)]),
    ("б", "Алиса, Боб, Кэрол", [(5, 2, 3), (2, 5, 1), (2, 1, 5)]),
    ("в", "Боб, Дейв, Кэрол", [(2, 5, 1), (4, 2, 1), (2, 1, 5)]),
]


def add_exercise1(doc) -> None:
    add_heading(doc, "Упражнение 1 — Блэкли (пример 1 методички), p = 7")
    for line in EX1_TEXT.split("\n"):
        add_para(doc, line, indent=False)
    for tag, names, planes in EX1_TRIPLES:
        (x, y, z), steps = gauss_blakley_with_steps(planes, 7)
        add_para(doc, f"Случай {tag}) {names}. Система ax + by − z ≡ −c (mod 7):", indent=False)
        for a, b, c in planes:
            add_math(doc, omml_display([m_op(f"{a} x + {b} y − z ≡ {(-c) % 7} (mod 7)")]))
        add_para(doc, "Решение методом Гаусса-Жордана:")
        for step in steps:
            add_listing(doc, step)
        add_para(
            doc,
            f"Из приведённой матрицы получаем (x, y, z) = ({x}, {y}, {z}). "
            f"Секрет x₀ = {x}.",
            indent=False,
        )
    add_para(
        doc,
        "Во всех трёх случаях x₀ = 5, что подтверждает свойство схемы Блэкли: любая "
        "легальная тройка восстанавливает один и тот же секрет.",
    )


# ----------------- контрольные вопросы -----------------


CONTROL_QA = [
    (
        "К какому типу протоколов согласно классификации по отношению к "
        "вспомогательным участникам относится протокол разделения секрета Шамира?",
        "К протоколам с арбитром (дилером): доверенный участник-дилер генерирует "
        "полином f(x), раздаёт доли (x_j, f(x_j)) другим участникам и затем выходит "
        "из системы. Восстановление секрета участниками идёт уже без него.",
    ),
    (
        "Какие математические факты лежат в основе схем Шамира и Блэкли?",
        "Схема Шамира — единственность полинома степени m − 1, проходящего через m "
        "различных точек (интерполяция Лагранжа в Z_p). Схема Блэкли — однозначность "
        "пересечения трёх плоскостей общего положения в Z_p³ (линейная алгебра в Z_p).",
    ),
    (
        "Полином какой степени нужен для (3, n)-схемы Шамира для трёх партий, "
        "когда минимально требуется 3, 2 и 4 человека из них?",
        "Для каждой партии — свой полином: степени 2, 1 и 3 (m − 1 на партию). "
        "Итоговый секрет — произведение свободных членов всех трёх полиномов.",
    ),
    (
        "Параметры (m, n)-схемы для 3 генералов и 7 полковников: «2 генерала + 1 "
        "полковник», «1 генерал + 3 полковника» или «5 полковников».",
        "Каждый генерал получает 3 доли, каждый полковник — 1 долю. Порог m = 5. "
        "Тогда любая из указанных комбинаций даёт ≥ 5 долей. Общее n = 3·3 + 7·1 = 16.",
    ),
    (
        "Какие возможности для Евы и Мэллори в этих схемах?",
        "Ева — пассивный наблюдатель: имея < m долей, она не получает информации о "
        "секрете. Мэллори — активный: имея m − 1 честных долей, может подобрать "
        "собственную, которая удовлетворит сборщика; схемы без аутентификации долей "
        "от этого не защищают.",
    ),
    (
        "Возможно ли динамически добавлять участников?",
        "Да: для Шамира — выдать новому участнику (x', f(x')) для свободной x'; для "
        "Блэкли — построить новую плоскость, проходящую через Q. Без дилера расширение "
        "сложнее и требует proactive secret sharing.",
    ),
    (
        "Если Кэрол вместо легальной доли (6, 1) назовёт (7, 3) или (3, 8) — "
        "восстановится ли секрет?",
        "Нет: интерполяция Лагранжа выдаст какое-то значение, но не настоящий секрет. "
        "Доля (3, 8) хуже — точка x = 3 совпадает с x Боба и алгоритм вообще не "
        "применим (деление на ноль в знаменателе).",
    ),
    (
        "От каких видов мошенничества защищена схема Шамира?",
        "От злоумышленника, знающего < m долей (информационная стойкость). От подмены "
        "долей легальными участниками, выдачи дилером неверных долей и использования "
        "дилером секрета — НЕ защищена; для этого нужны verifiable secret sharing-схемы.",
    ),
    (
        "Максимальное число участников схемы Шамира над Z_181?",
        "n ≤ p − 1 = 180, т.к. x_j должны быть попарно различными из {1, …, p − 1}.",
    ),
    (
        "Максимальное число участников схемы Блэкли над Z_11?",
        "Каждая доля — плоскость, задаётся парой (a, b) ∈ Z₁₁². Максимум n = 11² = 121.",
    ),
]


def add_control_questions(doc) -> None:
    add_heading(doc, "Контрольные вопросы")
    for i, (q, a) in enumerate(CONTROL_QA, start=1):
        add_qa(doc, i, q, a)


# ----------------- основной отчёт -----------------


def build_variant(variant: int) -> None:
    shamir_left = SHAMIR_LEFT[variant - 1]
    shamir_right = SHAMIR_RIGHT[variant - 1]
    bl_left = blakley_left_pairs(variant)
    bl_right = blakley_right_pairs(variant)

    meta = LabMeta(
        number=2,
        title="Пороговые схемы разделения секрета Шамира и Блэкли",
        variant=variant,
    )
    doc = make_doc()
    add_title_page(doc, meta)
    add_page_break(doc)

    # Тема, цель.
    add_heading(doc, "Тема и цель работы")
    add_para(
        doc,
        "Тема: пороговые схемы разделения секрета — Шамира (на основе интерполяции "
        "Лагранжа в Z_p) и Блэкли (на основе пересечения плоскостей).",
    )
    add_para(
        doc,
        "Цель работы: освоить методы порогового разделения секрета между n "
        "участниками, чтобы для восстановления требовалось не менее m долей. "
        "Реализовать упражнения 1, 2, 3 методички для индивидуального варианта.",
    )

    # Теория.
    add_heading(doc, "Теоретические сведения", level=2)
    add_para(
        doc,
        "Схема Шамира. Секрет S — свободный член полинома f(x) ∈ Z_p[x] степени m − 1. "
        "Долей участника является пара (x_j, f(x_j)). По любым m долям секрет "
        "восстанавливается формулой интерполяции Лагранжа в точке x = 0:",
    )
    add_math(
        doc,
        omml_display([
            m_text("f"),
            m_op("(0) = "),
            m_op("Σ_{j=1..m} y_j · ∏_{k≠j} (−x_k) · (x_j − x_k)⁻¹  (mod p)"),
        ]),
    )
    add_para(
        doc,
        "Схема Блэкли. Секрет — координата x₀ точки Q = (x₀, y₀, z₀) ∈ Z_p³. "
        "Каждая доля — плоскость z = ax + by + c, где c = z₀ − a·x₀ − b·y₀ (mod p). "
        "Любые три плоскости общего положения пересекаются в Q, которая "
        "восстанавливается решением системы методом Гаусса.",
    )

    # Задание.
    add_heading(doc, f"Задание варианта №{variant}")
    add_para(
        doc,
        "Упражнение 1 (Блэкли, пример 1 методички). Используя исходные данные "
        "Q = (5, 1, 2), p = 7, восстановить x₀ по трём заданным тройкам долей.",
    )
    shamir_left_text = ", ".join(f"({x}, {y})" for x, y in shamir_left)
    shamir_right_text = ", ".join(f"({x}, {y})" for x, y in shamir_right)
    add_para(
        doc,
        "Упражнение 2 (Шамир). По заданным долям восстановить секрет f(0), коэффициенты "
        "полинома и долю Дейва с x = 2:",
    )
    add_para(doc, f"• левая колонка: m = 4, p = 23, доли {shamir_left_text};", indent=False)
    add_para(doc, f"• правая колонка: m = 3, p = 31, доли {shamir_right_text}.", indent=False)
    bl_left_text = ", ".join(f"{n}=({a}, {b})" for n, (a, b) in zip("ABDC", bl_left))
    bl_right_text = ", ".join(f"{n}=({a}, {b})" for n, (a, b) in zip("ABDC", bl_right))
    add_para(
        doc,
        "Упражнение 3 (Блэкли). Создать доли для участников A, B, D, C и "
        "восстановить Q по любой тройке:",
    )
    add_para(
        doc,
        f"• левая колонка: p = 17, Q = (15, 5, 4), пары {bl_left_text};",
        indent=False,
    )
    add_para(
        doc,
        f"• правая колонка: p = 31, Q = (11, 10, 25), пары {bl_right_text}.",
        indent=False,
    )

    # Упражнение 1.
    add_exercise1(doc)

    # Упражнение 2 левая.
    add_heading(doc, "Упражнение 2 (а) — Шамир, m = 4, p = 23")
    add_para(doc, "Все операции далее — по модулю 23.", indent=False)
    add_lagrange_steps(doc, shamir_left, 23)
    coeffs_l = add_polynomial_block(doc, shamir_left, 23)
    add_dave_share(doc, coeffs_l, 23, dave_x=2)

    # Упражнение 2 правая.
    add_heading(doc, "Упражнение 2 (б) — Шамир, m = 3, p = 31")
    add_para(doc, "Все операции — по модулю 31.", indent=False)
    add_lagrange_steps(doc, shamir_right, 31)
    coeffs_r = add_polynomial_block(doc, shamir_right, 31)
    add_dave_share(doc, coeffs_r, 31, dave_x=2)

    # Упражнение 3.
    add_heading(doc, "Упражнение 3 (а) — Блэкли, p = 17, Q = (15, 5, 4)")
    add_blakley_section(doc, 17, BLAKLEY_LEFT_Q, bl_left)
    add_heading(doc, "Упражнение 3 (б) — Блэкли, p = 31, Q = (11, 10, 25)")
    add_blakley_section(doc, 31, BLAKLEY_RIGHT_Q, bl_right)

    # Программная проверка.
    add_page_break(doc)
    add_heading(doc, "Программная проверка")
    add_para(doc, "Запуск программы подтверждает все ручные вычисления:")
    shamir_out = run_cli("shamir", "--variant", str(variant), "--dave-x", "2")
    add_listing(
        doc,
        f"$ cargo run --release -p lab_02_secret_sharing -- shamir --variant {variant}\n"
        + shamir_out,
        caption="Листинг 1 — упражнение 2 (Шамир)",
    )
    blakley_out = run_cli("blakley", "--variant", str(variant))
    add_listing(
        doc,
        f"$ cargo run --release -p lab_02_secret_sharing -- blakley --variant {variant}\n"
        + blakley_out,
        caption="Листинг 2 — упражнение 3 (Блэкли)",
    )

    # Контрольные вопросы.
    add_page_break(doc)
    add_control_questions(doc)

    # Выводы.
    add_page_break(doc)
    add_heading(doc, "Выводы")
    add_para(
        doc,
        "В ходе работы реализованы две пороговые схемы разделения секрета: схема "
        "Шамира на интерполяции Лагранжа в Z_p и схема Блэкли на пересечении "
        "плоскостей в Z_p³. Ручные вычисления и программная реализация дали "
        "идентичные результаты: для (4, n)-схемы Шамира с p = 23 секрет f(0) "
        f"восстанавливается корректно; аналогично для (3, n)-схемы с p = 31. "
        "Для обеих (3, n)-схем Блэкли точка Q = (15, 5, 4) при p = 17 и "
        "Q = (11, 10, 25) при p = 31 восстанавливаются точно по любой тройке долей.",
    )

    out = (
        ROOT
        / "docs"
        / "reports"
        / "lab_02_secret_sharing"
        / f"var_{variant:02d}"
        / "Ковалев Д.П. ВКБ43 2 лаба.docx"
    )
    save(doc, out)
    print(f"  saved variant {variant:>2}: {out.relative_to(ROOT)}")


def main() -> None:
    if not BIN.exists():
        raise SystemExit("binary not built: cargo build -p lab_02_secret_sharing --release")
    for v in range(1, 29):
        build_variant(v)


if __name__ == "__main__":
    main()
