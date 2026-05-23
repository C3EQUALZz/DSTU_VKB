# Лаб 2 — Пороговые схемы Шамира и Блэкли

## Что внутри

- `crates/lab_02_secret_sharing/src/domain/modular.rs` — модулярная арифметика над Z_p.
- `crates/lab_02_secret_sharing/src/domain/shamir.rs` — Шамир: интерполяция Лагранжа и восстановление полинома методом Гаусса.
- `crates/lab_02_secret_sharing/src/domain/blakley.rs` — Блэкли: пересечение трёх плоскостей.
- `crates/lab_02_secret_sharing/src/presentation/variants.rs` — данные 28 вариантов из методички.

## Запуск

```bash
# Решить упражнение 2 для варианта 7:
cargo run --release -p lab_02_secret_sharing -- shamir --variant 7

# Решить упражнение 3 для варианта 12:
cargo run --release -p lab_02_secret_sharing -- blakley --variant 12

# Прогон всех 28 вариантов:
cargo run --release -p lab_02_secret_sharing -- all
```

## Тесты

```bash
cargo test -p lab_02_secret_sharing
```

Проверяются:
- Пример 3 методички (Шамир, p=11, секрет=7, доля Дейва (2, 0)).
- Примеры 1 и 2 методички (Блэкли).
- 28 вариантов корректно загружаются.

## Отчёты

В `docs/reports/lab_02_secret_sharing/var_NN/` — один docx на вариант,
сгенерированы через `python3 scripts/lab_02_secret_sharing/build.py`.
