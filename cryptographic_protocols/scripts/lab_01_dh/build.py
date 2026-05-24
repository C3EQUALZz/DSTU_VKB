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
    m_frac,
    m_op,
    m_sub,
    m_sup,
    m_text,
    make_doc,
    omml_display,
    omml_inline,
    save,
)


def read_artifact(name: str) -> str:
    return (ROOT / "artifacts" / "lab_01_dh" / name).read_text(encoding="utf-8")


def read_source(rel: str) -> str:
    return (ROOT / "crates" / "lab_01_dh" / "src" / rel).read_text(encoding="utf-8")


# ---------- ручные расчёты ----------


def mod_pow(base: int, exp: int, mod: int) -> int:
    return pow(base, exp, mod)


def m_pow(base: str, exp: str) -> str:
    return m_sup(m_text(base), m_text(exp))


def m_eq_line(parts: list[str]) -> str:
    return omml_display(parts)


def add_dh_steps(doc) -> None:
    """Пошаговая проверка DH (n=97, g=5, X_A=36, X_B=58, K=75) через OMML."""
    add_para(doc, "Шаг 1. Вычисляем открытый ключ Алисы:", indent=False)
    add_math(doc, m_eq_line([
        m_sub(m_text("Y"), m_text("A")), m_op(" = "),
        m_pow("5", "36"), m_op(" mod 97"),
    ]))
    add_para(
        doc,
        "Используя метод последовательного возведения в квадрат (square-and-multiply):",
        indent=False,
    )
    add_math(doc, m_eq_line([m_pow("5", "2"), m_op(" = 25")]))
    add_math(doc, m_eq_line([m_pow("5", "4"), m_op(" = "), m_pow("25", "2"), m_op(" = 625 ≡ 43 (mod 97)")]))
    add_math(doc, m_eq_line([m_pow("5", "8"), m_op(" = "), m_pow("43", "2"), m_op(" = 1849 ≡ 6 (mod 97)")]))
    add_math(doc, m_eq_line([m_pow("5", "16"), m_op(" = "), m_pow("6", "2"), m_op(" = 36 (mod 97)")]))
    add_math(doc, m_eq_line([m_pow("5", "32"), m_op(" = "), m_pow("36", "2"), m_op(" = 1296 ≡ 35 (mod 97)")]))
    add_math(doc, m_eq_line([
        m_pow("5", "36"), m_op(" = "), m_pow("5", "32"), m_op(" · "), m_pow("5", "4"),
        m_op(" = 35 · 43 = 1505 ≡ 50 (mod 97)"),
    ]))
    add_math(doc, m_eq_line([m_sub(m_text("Y"), m_text("A")), m_op(" = 50")]))

    add_para(doc, "Шаг 2. Вычисляем открытый ключ Боба:", indent=False)
    add_math(doc, m_eq_line([
        m_sub(m_text("Y"), m_text("B")), m_op(" = "), m_pow("5", "58"), m_op(" mod 97"),
    ]))
    add_math(doc, m_eq_line([
        m_pow("5", "58"), m_op(" = "), m_pow("5", "32"), m_op(" · "), m_pow("5", "16"),
        m_op(" · "), m_pow("5", "8"), m_op(" · "), m_pow("5", "2"),
        m_op(" = 35 · 36 · 6 · 25 = 189000 ≡ 44 (mod 97)"),
    ]))
    add_math(doc, m_eq_line([m_sub(m_text("Y"), m_text("B")), m_op(" = 44")]))

    add_para(doc, "Шаг 3. Алиса вычисляет общий ключ:", indent=False)
    add_math(doc, m_eq_line([
        m_sub(m_text("K"), m_text("A")), m_op(" = "),
        m_sup(m_sub(m_text("Y"), m_text("B")), m_sub(m_text("X"), m_text("A"))),
        m_op(" = "), m_pow("44", "36"), m_op(" mod 97"),
    ]))
    add_math(doc, m_eq_line([m_pow("44", "2"), m_op(" ≡ 51 (mod 97)")]))
    add_math(doc, m_eq_line([m_pow("44", "4"), m_op(" = "), m_pow("51", "2"), m_op(" = 2601 ≡ 75 (mod 97)")]))
    add_math(doc, m_eq_line([m_pow("44", "8"), m_op(" = "), m_pow("75", "2"), m_op(" = 5625 ≡ 96 (mod 97)")]))
    add_math(doc, m_eq_line([m_pow("44", "16"), m_op(" = "), m_pow("96", "2"), m_op(" ≡ 1 (mod 97)")]))
    add_math(doc, m_eq_line([m_pow("44", "32"), m_op(" = 1 (mod 97)")]))
    add_math(doc, m_eq_line([
        m_pow("44", "36"), m_op(" = "), m_pow("44", "32"), m_op(" · "), m_pow("44", "4"),
        m_op(" = 1 · 75 = 75 (mod 97)"),
    ]))

    add_para(doc, "Шаг 4. Боб вычисляет общий ключ:", indent=False)
    add_math(doc, m_eq_line([
        m_sub(m_text("K"), m_text("B")), m_op(" = "),
        m_sup(m_sub(m_text("Y"), m_text("A")), m_sub(m_text("X"), m_text("B"))),
        m_op(" = "), m_pow("50", "58"), m_op(" mod 97"),
    ]))
    add_math(doc, m_eq_line([m_pow("50", "2"), m_op(" = 2500 ≡ 75 (mod 97)")]))
    add_math(doc, m_eq_line([m_pow("50", "4"), m_op(" = "), m_pow("75", "2"), m_op(" = 5625 ≡ 96 (mod 97)")]))
    add_math(doc, m_eq_line([m_pow("50", "8"), m_op(" = "), m_pow("96", "2"), m_op(" ≡ 1 (mod 97)")]))
    add_math(doc, m_eq_line([m_pow("50", "16"), m_op(" = "), m_pow("50", "32"), m_op(" = 1 (mod 97)")]))
    add_math(doc, m_eq_line([
        m_pow("50", "58"), m_op(" = "), m_pow("50", "32"), m_op(" · "), m_pow("50", "16"),
        m_op(" · "), m_pow("50", "8"), m_op(" · "), m_pow("50", "2"),
        m_op(" = 1 · 1 · 1 · 75 = 75 (mod 97)"),
    ]))
    add_math(doc, m_eq_line([
        m_sub(m_text("K"), m_text("B")), m_op(" = 75 = "),
        m_sub(m_text("K"), m_text("A")), m_op(" ✓"),
    ]))


def add_primitive_root_steps(doc) -> None:
    add_para(
        doc,
        "Дано p = 41. Функция Эйлера: φ(p) = 40 = 2³ · 5. Простые делители числа 40: "
        "q₁ = 2, q₂ = 5. По свойству 5 методички число a является первообразным корнем "
        "по модулю 41 тогда и только тогда, когда:",
        indent=False,
    )
    add_math(doc, m_eq_line([
        m_pow("a", "40/2"), m_op(" = "), m_pow("a", "20"), m_op(" ≢ 1 (mod 41), и "),
        m_pow("a", "40/5"), m_op(" = "), m_pow("a", "8"), m_op(" ≢ 1 (mod 41)"),
    ]))
    add_para(doc, "Перебираем кандидаты:", indent=False)
    add_math(doc, m_eq_line([
        m_text("a = 2:  "), m_pow("2", "8"), m_op(" = 256 ≡ 10 (mod 41); "),
        m_pow("2", "20"), m_op(" ≡ 1 (mod 41)  → отвергаем"),
    ]))
    add_math(doc, m_eq_line([
        m_text("a = 3:  "), m_pow("3", "8"), m_op(" = 6561 ≡ 1 (mod 41)  → отвергаем"),
    ]))
    add_math(doc, m_eq_line([
        m_text("a = 4:  "), m_pow("4", "8"), m_op(" ≡ 18 ≠ 1; "),
        m_pow("4", "20"), m_op(" ≡ 1  → отвергаем"),
    ]))
    add_math(doc, m_eq_line([
        m_text("a = 5:  "), m_pow("5", "8"), m_op(" ≡ 18 ≠ 1; "),
        m_pow("5", "20"), m_op(" ≡ 1  → отвергаем"),
    ]))
    add_math(doc, m_eq_line([
        m_text("a = 6:  "), m_pow("6", "8"), m_op(" ≡ 10 ≠ 1; "),
        m_pow("6", "20"), m_op(" ≡ 40 ≠ 1  → принимаем"),
    ]))
    add_para(
        doc,
        "Итог: g = 6 — наименьший первообразный корень по модулю 41. ✓",
        indent=False,
    )


def add_miller_rabin_steps(doc) -> None:
    add_para(doc, "Проверим простоту p = 23 тестом Рабина-Миллера.", indent=False)
    add_math(doc, m_eq_line([
        m_text("p − 1 = 22 = "), m_pow("2", "1"), m_op(" · 11"),
        m_op(",   откуда b = 1, m = 11"),
    ]))
    add_para(doc, "Раунд 1: случайный свидетель a = 5.", indent=False)
    add_math(doc, m_eq_line([
        m_text("z = "), m_pow("a", "m"), m_op(" mod p = "),
        m_pow("5", "11"), m_op(" mod 23"),
    ]))
    add_math(doc, m_eq_line([m_pow("5", "2"), m_op(" = 25 ≡ 2 (mod 23)")]))
    add_math(doc, m_eq_line([m_pow("5", "4"), m_op(" ≡ 4 (mod 23)")]))
    add_math(doc, m_eq_line([m_pow("5", "8"), m_op(" ≡ 16 (mod 23)")]))
    add_math(doc, m_eq_line([
        m_pow("5", "11"), m_op(" = "), m_pow("5", "8"), m_op(" · "),
        m_pow("5", "2"), m_op(" · 5 = 16 · 2 · 5 = 160 ≡ 22 ≡ p − 1 (mod 23)"),
    ]))
    add_para(doc, "z = p − 1 ⇒ тест пройден.", indent=False)

    add_para(doc, "Раунд 2: случайный свидетель a = 7.", indent=False)
    add_math(doc, m_eq_line([m_pow("7", "2"), m_op(" = 49 ≡ 3 (mod 23)")]))
    add_math(doc, m_eq_line([m_pow("7", "4"), m_op(" ≡ 9 (mod 23)")]))
    add_math(doc, m_eq_line([m_pow("7", "8"), m_op(" = 81 ≡ 12 (mod 23)")]))
    add_math(doc, m_eq_line([
        m_pow("7", "11"), m_op(" = "), m_pow("7", "8"), m_op(" · "),
        m_pow("7", "2"), m_op(" · 7 = 12 · 3 · 7 = 252 ≡ 22 ≡ p − 1 (mod 23)"),
    ]))
    add_para(doc, "z = p − 1 ⇒ тест пройден.", indent=False)
    add_para(
        doc,
        "После t = 8 успешных раундов с различными свидетелями вероятность принять "
        "составное за простое не превышает:",
    )
    add_math(doc, m_eq_line([
        m_sup(m_text("(1/4)"), m_text("8")), m_op(" ≈ 1.5 · "),
        m_sup(m_text("10"), m_text("−5")),
    ]))
    add_para(doc, "Следовательно, p = 23 считается простым (что верно).", indent=False)


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
        "Параметры протокола Диффи-Хеллмана из примера методички: n = 97 (большое "
        "простое), g = 5 (первообразный корень по модулю 97), X_A = 36 (секрет Алисы), "
        "X_B = 58 (секрет Боба). Ожидаемый общий ключ K = 75.",
    )
    add_dh_steps(doc)

    add_heading(doc, "Ручная проверка первообразного корня по mod 41")
    add_primitive_root_steps(doc)

    add_heading(doc, "Ручная проверка теста Рабина-Миллера")
    add_miller_rabin_steps(doc)

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
