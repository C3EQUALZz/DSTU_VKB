# Лаб 1 — Обмен ключами по схеме Диффи-Хеллмана

Реализация курса «Криптографические протоколы».

## Что внутри

- `crates/lab_01_dh/src/domain/prime.rs` — тест Рабина-Миллера, генерация простых.
- `crates/lab_01_dh/src/domain/primitive_root.rs` — поиск первообразных корней.
- `crates/lab_01_dh/src/domain/dh.rs` — обмен ключами.
- `crates/lab_01_dh/src/application/usecases.rs` — сценарии с замером времени.
- `crates/lab_01_dh/src/presentation/cli.rs` — clap-CLI.

## Запуск

```bash
# 1. Сгенерировать 128-битное простое:
cargo run --release -p lab_01_dh -- --seed 42 gen-prime --bits 128 --rounds 32

# 2. Найти простые в диапазоне:
cargo run --release -p lab_01_dh -- range-primes --from 1000 --to 1100

# 3. Первые 100 первообразных корней по mod 1009:
cargo run --release -p lab_01_dh -- roots --n 1009 --count 100

# 4. Обмен Диффи-Хеллмана (пример из методички):
cargo run --release -p lab_01_dh -- --seed 42 dh --n 97 --g 5 --xa 36 --xb 58

# 5. Обмен со случайным n заданной разрядности:
cargo run --release -p lab_01_dh -- --seed 7 dh --bits 128 --rounds 32
```

Глобальные флаги:

- `--seed <u64>` — фиксирует ChaCha20 RNG для воспроизводимости;
- `RUST_LOG=debug` — подробные логи (раунды Миллера-Рабина и пр.).

## Тесты

```bash
cargo test -p lab_01_dh
```

Покрытие включает:

- Эталонный пример из методички (n=97, K=75).
- Проверку Рабина-Миллера на наборе известных простых/составных.
- Поиск первообразных корней по mod 41 (ожидаемый ряд 6, 7, 11, 12, ...).
- Round-trip генерации простого с минимальной разрядностью 65 бит.

## Отчёт

Сгенерирован в `docs/reports/lab_01_dh/Ковалев Д.П. ВКБ43 1 лаба.docx`
через `python3 scripts/lab_01_dh/build.py`.
