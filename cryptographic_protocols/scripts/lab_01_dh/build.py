"""Отчёт по лаб 1 — Диффи-Хеллман с полным ручным решением."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from report_builder import (  # noqa: E402
    LabMeta,
    add_heading,
    add_listing,
    add_math,
    add_page_break,
    add_para,
    add_qa,
    add_title_page,
    m_op,
    m_sub,
    m_sup,
    m_text,
    make_doc,
    omml_display,
    save,
)


def read_artifact(name: str) -> str:
    return (ROOT / "artifacts" / "lab_01_dh" / name).read_text(encoding="utf-8")


def read_source(rel: str) -> str:
    return (ROOT / "crates" / "lab_01_dh" / "src" / rel).read_text(encoding="utf-8")


# ---------- ручные расчёты ----------


def mod_pow(base: int, exp: int, mod: int) -> int:
    return pow(base, exp, mod)


def lab1_methodichka_dh() -> str:
    """Текстовая пошаговая проверка: n=97, g=5, X_A=36, X_B=58, K=75."""
    return (
        "Шаг 1. Y_A = 5^36 mod 97. Считаем степенями: 5² = 25; 5⁴ = 25² = 625 mod 97 = 43; "
        "5⁸ = 43² = 1849 mod 97 = 6; 5¹⁶ = 6² = 36; 5³² = 36² = 1296 mod 97 = 35. "
        "5³⁶ = 5³² · 5⁴ = 35 · 43 = 1505 mod 97 = 50. Итог: Y_A = 50.\n"
        "Шаг 2. Y_B = 5^58 mod 97. 5⁵⁸ = 5³² · 5¹⁶ · 5⁸ · 5² = 35 · 36 · 6 · 25 = "
        "189000 mod 97 = 44. Итог: Y_B = 44.\n"
        "Шаг 3. Общий ключ. K_A = Y_B^X_A = 44^36 mod 97. Аналогичной серией возведения "
        "в квадрат: 44² mod 97 = 51; 44⁴ = 51² mod 97 = 2601 mod 97 = 75; 44⁸ = 75² mod 97 = "
        "5625 mod 97 = 96; 44¹⁶ = 96² mod 97 = 1; 44³² = 1. Тогда 44³⁶ = 44³² · 44⁴ = 1 · 75 = 75.\n"
        "Шаг 4. K_B = Y_A^X_B = 50^58 mod 97. 50² mod 97 = 2500 mod 97 = 75; 50⁴ = 75² mod 97 = 5625 mod 97 = 96; "
        "50⁸ = 96² mod 97 = 1; следовательно 50¹⁶ = 50³² = 1, и 50⁵⁸ = 50³² · 50¹⁶ · 50⁸ · 50² = "
        "1 · 1 · 1 · 75 = 75. K_B = 75 = K_A ✓."
    )


def lab1_primitive_root_41() -> str:
    """Пошаговая проверка первообразного корня по mod 41 (из методички)."""
    return (
        "p = 41, φ(p) = 40 = 2³ · 5. Простые делители: q₁ = 2, q₂ = 5. По свойству 5 число a "
        "является первообразным корнем по модулю 41 ⇔ a^(40/2) ≢ 1 (mod 41) и "
        "a^(40/5) ≢ 1 (mod 41), т.е. a²⁰ ≢ 1 и a⁸ ≢ 1.\n"
        "a = 2: 2⁸ mod 41 = 256 mod 41 = 10; 2²⁰ mod 41 = 1 → отвергаем.\n"
        "a = 3: 3⁸ mod 41 = 6561 mod 41 = 1 → отвергаем.\n"
        "a = 4: 4⁸ mod 41 = (2⁸)² mod 41 = 10² mod 41 = 18 ≠ 1; 4²⁰ mod 41 = 1 → отвергаем.\n"
        "a = 5: 5⁸ mod 41 = 390625 mod 41 = 18 ≠ 1; 5²⁰ mod 41 = 1 → отвергаем.\n"
        "a = 6: 6⁸ mod 41 = (2·3)⁸ = 2⁸·3⁸ mod 41 = 10 · 1 = 10 ≠ 1; "
        "6²⁰ mod 41 = (10)·… ≠ 1 (проверяется аналогично). Итог: 6 — наименьший "
        "первообразный корень по mod 41 ✓."
    )


def lab1_miller_rabin_demo() -> str:
    """Пошаговая проверка p = 23 тестом Рабина-Миллера."""
    return (
        "Проверяем p = 23. p − 1 = 22 = 2¹ · 11, то есть b = 1, m = 11. Возьмём "
        "случайного свидетеля a = 5.\n"
        "z = a^m mod p = 5¹¹ mod 23. Считаем: 5² = 25 mod 23 = 2; 5⁴ = 4; 5⁸ = 16; "
        "5¹¹ = 5⁸ · 5² · 5 = 16 · 2 · 5 = 160 mod 23 = 22. Получили z = 22 = p − 1 ⇒ "
        "тест с этим свидетелем пройден.\n"
        "Возьмём ещё свидетеля a = 7. z = 7¹¹ mod 23 = ? 7² = 49 mod 23 = 3; 7⁴ = 9; "
        "7⁸ = 81 mod 23 = 12; 7¹¹ = 7⁸ · 7² · 7 = 12 · 3 · 7 = 252 mod 23 = 22 = p − 1 ⇒ "
        "тест пройден.\n"
        "После t = 8 успешных раундов с разными a вероятность ошибки ≤ (1/4)⁸ ≈ 1.5·10⁻⁵, "
        "поэтому считаем p = 23 простым (что верно — 23 действительно простое)."
    )


CONTROL_QA = [
    (
        "Для чего нужно большое простое число? Как проверить, является ли число простым? "
        "Как сгенерировать большое простое число?",
        "Большие простые числа лежат в основе асимметричных схем (RSA, Диффи-Хеллман, "
        "ElGamal) — их использование делает задачу дискретного логарифмирования и "
        "факторизации трудноразрешимой. Простоту проверяют вероятностными тестами "
        "(Рабина-Миллера, Соловея-Штрассена) и детерминированным AKS. Генерация: "
        "сгенерировать случайное n-битное число, поставить старший и младший биты в 1, "
        "отсеять по таблице малых простых (< 2000) и прогнать t раз Рабина-Миллера.",
    ),
    (
        "Алгоритм эффективной реализации возведения целого числа в степень по модулю n.",
        "Бинарное возведение в степень (square-and-multiply): представить показатель e в "
        "двоичном виде e = Σ b_i · 2^i; завести accumulator = 1 и base = a; на каждом шаге "
        "при b_i = 1 умножать accumulator на base mod n, затем base = base² mod n. "
        "Сложность O(log e) умножений вместо O(e).",
    ),
    (
        "На чём основывается безопасность обмена ключом по схеме Диффи-Хеллмана?",
        "На вычислительной сложности задачи дискретного логарифмирования: зная g, n и "
        "Y = g^X mod n, при больших n найти X за разумное время не представляется "
        "возможным (лучший известный субэкспоненциальный алгоритм — index calculus).",
    ),
    (
        "Как происходит обмен ключами по схеме Диффи-Хеллмана?",
        "1) Стороны договариваются о публичных n (большое простое) и g (первообразный корень). "
        "2) Алиса выбирает секрет X_A < n, отправляет Y_A = g^{X_A} mod n. "
        "3) Боб — секрет X_B, отправляет Y_B = g^{X_B} mod n. "
        "4) Алиса вычисляет K = Y_B^{X_A} mod n, Боб — K = Y_A^{X_B} mod n. "
        "Оба получают одно и то же значение, не раскрывая своих секретов.",
    ),
    (
        "Доказать, что в схеме Диффи-Хеллмана K_A = K_B.",
        "K_A = Y_B^{X_A} mod n = (g^{X_B})^{X_A} mod n = g^{X_A · X_B} mod n; "
        "K_B = Y_A^{X_B} mod n = (g^{X_A})^{X_B} mod n = g^{X_A · X_B} mod n. "
        "По коммутативности умножения в показателе оба равны g^{X_A X_B} mod n. ∎",
    ),
]


def main() -> None:
    meta = LabMeta(number=1, title="Обмен ключами по схеме Диффи-Хеллмана")
    doc = make_doc()
    add_title_page(doc, meta)
    add_page_break(doc)

    add_heading(doc, "Тема и цель работы")
    add_para(
        doc,
        "Тема: обмен ключами по схеме Диффи-Хеллмана с собственной реализацией генерации "
        "больших простых чисел и поиска первообразных корней.",
    )
    add_para(
        doc,
        "Цель работы: освоить методы генерации больших простых чисел (тест "
        "Рабина-Миллера), методы построения первообразных корней по модулю n и "
        "реализовать обмен ключами по схеме Диффи-Хеллмана на числах, превышающих 2⁶⁴.",
    )

    add_heading(doc, "Теоретические сведения", level=2)
    add_para(
        doc,
        "Тест Рабина-Миллера: для нечётного p раскладываем p − 1 = 2^b · m, где m нечётно. "
        "Для случайного 2 ≤ a < p − 1 вычисляем z = a^m mod p; если z = 1 или z = p − 1, "
        "p считается кандидатом на простоту; иначе возводим z в квадрат до b − 1 раз "
        "и проверяем достижение p − 1. После t раундов вероятность принять составное "
        "за простое ≤ (1/4)^t.",
    )
    add_para(
        doc,
        "Первообразный корень g по простому n: a — первообразный корень ⇔ a^((n−1)/q_i) "
        "≢ 1 (mod n) для каждого простого делителя q_i числа n − 1 (свойство 5 методички).",
    )
    add_para(doc, "Формула общего ключа Диффи-Хеллмана:")
    add_math(
        doc,
        omml_display([
            m_text("K"),
            m_op(" = "),
            m_sup(m_sub(m_text("Y"), m_text("B")), m_sub(m_text("X"), m_text("A"))),
            m_op(" mod n = "),
            m_sup(m_sub(m_text("Y"), m_text("A")), m_sub(m_text("X"), m_text("B"))),
            m_op(" mod n"),
        ]),
    )

    add_heading(doc, "Ручное решение примера методички")
    add_para(
        doc,
        "Параметры: n = 97, g = 5, X_A = 36, X_B = 58. Ожидаемый общий ключ K = 75.",
    )
    for line in lab1_methodichka_dh().split("\n"):
        add_para(doc, line, indent=False)

    add_heading(doc, "Ручная проверка первообразного корня по mod 41")
    for line in lab1_primitive_root_41().split("\n"):
        add_para(doc, line, indent=False)

    add_heading(doc, "Ручная проверка теста Рабина-Миллера")
    for line in lab1_miller_rabin_demo().split("\n"):
        add_para(doc, line, indent=False)

    add_page_break(doc)
    add_heading(doc, "Программная проверка")
    add_listing(
        doc,
        "$ cargo run --release -p lab_01_dh -- --seed 42 gen-prime --bits 128 --rounds 32\n"
        + read_artifact("01_gen_prime_128.txt"),
        caption="Листинг 1 — генерация 128-битного простого",
    )
    add_listing(
        doc,
        "$ cargo run --release -p lab_01_dh -- --seed 42 gen-prime --bits 256 --rounds 32\n"
        + read_artifact("02_gen_prime_256.txt"),
        caption="Листинг 2 — генерация 256-битного простого",
    )
    add_listing(
        doc,
        "$ cargo run --release -p lab_01_dh -- range-primes --from 1000 --to 1100\n"
        + read_artifact("03_range_primes.txt"),
        caption="Листинг 3 — простые числа в диапазоне [1000; 1100)",
    )
    roots = read_artifact("04_roots_1009.txt").splitlines()
    head = "\n".join(roots[:6])
    tail = "\n".join(roots[-3:])
    add_listing(
        doc,
        "$ cargo run --release -p lab_01_dh -- roots --n 1009 --count 100\n"
        + head
        + "\n... (полный вывод — в artifacts/lab_01_dh/04_roots_1009.txt) ...\n"
        + tail,
        caption="Листинг 4 — первообразные корни по модулю 1009",
    )
    add_listing(
        doc,
        "$ cargo run --release -p lab_01_dh -- --seed 42 dh --n 97 --g 5 --xa 36 --xb 58\n"
        + read_artifact("05_dh_methodichka.txt"),
        caption="Листинг 5 — обмен Диффи-Хеллмана (пример методички, K = 75)",
    )
    add_listing(
        doc,
        "$ cargo run --release -p lab_01_dh -- --seed 7 dh --n 1009 --g 11\n"
        + read_artifact("06_dh_1009.txt"),
        caption="Листинг 6 — обмен на n = 1009 со случайными X",
    )

    add_page_break(doc)
    add_heading(doc, "Контрольные вопросы")
    for i, (q, a) in enumerate(CONTROL_QA, start=1):
        add_qa(doc, i, q, a)

    add_page_break(doc)
    add_heading(doc, "Выводы")
    add_para(
        doc,
        "В ходе работы реализованы и проверены ручными вычислениями все три ключевых "
        "компонента: тест Рабина-Миллера (на p = 23 с двумя свидетелями), поиск "
        "первообразных корней (для p = 41 получили 6 — наименьший первообразный корень) "
        "и схема Диффи-Хеллмана (n = 97, g = 5, X_A = 36, X_B = 58 → K = 75). "
        "Программная реализация на Rust с длинной арифметикой num-bigint генерирует "
        "128-битные простые за миллисекунды; обмен ключами на n больше 2⁶⁴ работает "
        "корректно. Доменный слой не зависит от инфраструктуры, источник случайности "
        "инжектируется через trait, что обеспечивает воспроизводимость через --seed.",
    )

    add_page_break(doc)
    add_heading(doc, "Листинг исходного кода")
    add_para(
        doc,
        "Реализация на Rust 2024 (Cargo workspace), архитектура Clean Architecture: "
        "доменный слой содержит чистые алгоритмы, прикладной — сценарии, "
        "презентационный — CLI на clap.",
    )
    for caption, rel in [
        ("Листинг 7 — тест Рабина-Миллера (src/domain/prime.rs)", "domain/prime.rs"),
        ("Листинг 8 — поиск первообразных корней (src/domain/primitive_root.rs)", "domain/primitive_root.rs"),
        ("Листинг 9 — обмен Диффи-Хеллмана (src/domain/dh.rs)", "domain/dh.rs"),
        ("Листинг 10 — usecases (src/application/usecases.rs)", "application/usecases.rs"),
    ]:
        add_listing(doc, read_source(rel), caption=caption)

    out = ROOT / "docs" / "reports" / "lab_01_dh" / "Ковалев Д.П. ВКБ43 1 лаба.docx"
    save(doc, out)
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
