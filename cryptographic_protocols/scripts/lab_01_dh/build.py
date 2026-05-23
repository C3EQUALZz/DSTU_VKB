"""Сборка отчёта по лаб 1 — обмен ключами по схеме Диффи-Хеллмана."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from report_builder import (  # noqa: E402
    LabMeta,
    add_heading,
    add_label,
    add_listing,
    add_para,
    add_title_page,
    make_doc,
    save,
)


def read_artifact(name: str) -> str:
    return (ROOT / "artifacts" / "lab_01_dh" / name).read_text(encoding="utf-8")


def read_source(rel: str) -> str:
    return (ROOT / "crates" / "lab_01_dh" / "src" / rel).read_text(encoding="utf-8")


def main() -> None:
    meta = LabMeta(number=1, title="Обмен ключами по схеме Диффи-Хеллмана")
    doc = make_doc()
    add_title_page(doc, meta)
    doc.add_page_break()

    add_heading(doc, "Тема и цель работы")
    add_para(
        doc,
        "Тема: обмен ключами по схеме Диффи-Хеллмана с собственной реализацией "
        "генерации больших простых чисел и поиска первообразных корней.",
    )
    add_para(
        doc,
        "Цель работы: освоить методы генерации больших простых чисел (тест Рабина-Миллера), "
        "методы построения первообразных корней по модулю n и реализовать обмен ключами "
        "по схеме Диффи-Хеллмана на числах, превышающих 2^64.",
    )

    add_heading(doc, "Краткие теоретические сведения", level=2)
    add_para(
        doc,
        "Тест Рабина-Миллера — вероятностный алгоритм проверки числа на простоту. "
        "Для проверяемого нечётного p раскладываем p − 1 = 2^b · m, где m нечётно. "
        "Для случайного 2 ≤ a < p − 1 вычисляем z = a^m mod p. "
        "Если z = 1 или z = p − 1 — кандидат на простоту. Иначе возводим z в квадрат до "
        "(b − 1) раз; если получим p − 1 — кандидат, если 1 при j > 0 — число составное. "
        "После t раундов вероятность принять составное за простое не превышает (1/4)^t.",
    )
    add_para(
        doc,
        "Первообразный корень g по простому модулю n — число, чьи степени порождают все "
        "ненулевые вычеты по модулю n. Согласно свойству 5 (методичка), для проверки "
        "достаточно убедиться, что a^((n−1)/q_i) ≢ 1 (mod n) для каждого простого делителя "
        "q_i числа n − 1.",
    )
    add_para(
        doc,
        "Схема Диффи-Хеллмана. Стороны A и B договариваются о публичных n и g. "
        "Каждая выбирает секрет X и вычисляет Y = g^X mod n. Обменявшись Y, "
        "получают общий ключ K = Y_other^X mod n. Безопасность опирается на "
        "сложность дискретного логарифмирования.",
    )

    doc.add_page_break()
    add_heading(doc, "Программная реализация")
    add_para(
        doc,
        "Решение оформлено как Cargo-workspace на Rust 2024 edition в crate "
        "lab_01_dh. Архитектура соответствует Clean Architecture: домен содержит "
        "алгоритмы (Рабин-Миллер, генерация простых, первообразные корни, DH), "
        "прикладной слой — сценарии, презентация — clap-CLI. Источник случайности "
        "(ChaCha20 RNG) инжектируется через trait RandomSource — для воспроизводимых "
        "запусков используется параметр --seed.",
    )
    add_para(
        doc,
        "Все вычисления над целыми произвольной длины выполняются через num-bigint. "
        "Алгоритм Рабина-Миллера реализован вручную в crates/lab_01_dh/src/domain/prime.rs.",
    )

    add_heading(doc, "Запуск и проверка работы программы", level=2)

    add_para(
        doc,
        "1. Генерация большого простого числа. Команда задаёт количество бит и число раундов "
        "Рабина-Миллера; программа выводит итоговое число, количество итераций и затраченное "
        "время.",
    )
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

    add_para(
        doc,
        "2. Перечисление всех простых в заданном диапазоне с суммарным временем работы.",
    )
    add_listing(
        doc,
        "$ cargo run --release -p lab_01_dh -- range-primes --from 1000 --to 1100\n"
        + read_artifact("03_range_primes.txt"),
        caption="Листинг 3 — простые числа в диапазоне [1000; 1100)",
    )

    add_para(
        doc,
        "3. Поиск первых 100 первообразных корней по простому модулю. Программа выводит "
        "также суммарное время поиска.",
    )
    roots = read_artifact("04_roots_1009.txt").splitlines()
    head = "\n".join(roots[:6])
    tail = "\n".join(roots[-3:])
    add_listing(
        doc,
        "$ cargo run --release -p lab_01_dh -- roots --n 1009 --count 100\n"
        + head
        + "\n... (полный вывод в artifacts/lab_01_dh/04_roots_1009.txt) ...\n"
        + tail,
        caption="Листинг 4 — первообразные корни по модулю 1009 (сокращённо)",
    )

    add_para(
        doc,
        "4. Моделирование обмена ключами по схеме Диффи-Хеллмана. Сначала — пример из "
        "методички (n = 97, g = 5, X_A = 36, X_B = 58, ожидаемый общий ключ K = 75):",
    )
    add_listing(
        doc,
        "$ cargo run --release -p lab_01_dh -- --seed 42 dh --n 97 --g 5 --xa 36 --xb 58\n"
        + read_artifact("05_dh_methodichka.txt"),
        caption="Листинг 5 — обмен ключами, тестовый пример из методички",
    )
    add_para(
        doc,
        "Далее — запуск с автоматически сгенерированным простым (для краткости используется "
        "малое n = 1009, в боевом режиме --bits 128 даёт n > 2^127):",
    )
    add_listing(
        doc,
        "$ cargo run --release -p lab_01_dh -- --seed 7 dh --n 1009 --g 11\n"
        + read_artifact("06_dh_1009.txt"),
        caption="Листинг 6 — обмен ключами на n = 1009 со случайными X_A, X_B",
    )

    doc.add_page_break()
    add_heading(doc, "Листинг исходного кода (ключевые модули)")

    add_label(doc, "Листинг 7 — тест Рабина-Миллера и генерация простого (src/domain/prime.rs)")
    add_listing(doc, read_source("domain/prime.rs"))

    add_label(
        doc,
        "Листинг 8 — построение первообразных корней (src/domain/primitive_root.rs)",
    )
    add_listing(doc, read_source("domain/primitive_root.rs"))

    add_label(doc, "Листинг 9 — обмен ключами Диффи-Хеллмана (src/domain/dh.rs)")
    add_listing(doc, read_source("domain/dh.rs"))

    add_label(doc, "Листинг 10 — usecases прикладного слоя (src/application/usecases.rs)")
    add_listing(doc, read_source("application/usecases.rs"))

    doc.add_page_break()
    add_heading(doc, "Выводы")
    add_para(
        doc,
        "В ходе работы реализованы три ключевых компонента криптографического протокола: "
        "вероятностный тест простоты Рабина-Миллера, поиск первообразных корней по простому "
        "модулю и сам обмен ключами по схеме Диффи-Хеллмана. Все алгоритмы работают на "
        "числах произвольной длины (использован крейт num-bigint), что подтверждается "
        "генерацией 128- и 256-битных простых за единицы миллисекунд.",
    )
    add_para(
        doc,
        "Корректность реализации подтверждается тестами на эталонных примерах: для p = 41 "
        "найденный набор первообразных корней начинается с 6, что совпадает с методическим "
        "указанием; для протокола Диффи-Хеллмана при n = 97, g = 5, X_A = 36, X_B = 58 общий "
        "ключ равен 75 — также как в учебнике. Корректность Рабина-Миллера дополнительно "
        "проверена на множестве известных простых и составных чисел.",
    )
    add_para(
        doc,
        "Архитектурно решение соответствует Clean Architecture: доменный слой не зависит от "
        "инфраструктуры, источник случайности абстрагирован trait-объектом, что обеспечивает "
        "детерминизм при тестировании и гибкость при замене RNG в боевой эксплуатации.",
    )

    out = ROOT / "docs" / "reports" / "lab_01_dh" / "Ковалев Д.П. ВКБ43 1 лаба.docx"
    save(doc, out)
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
