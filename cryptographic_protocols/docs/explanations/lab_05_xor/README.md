# Лаб 5 — XOR-шифрование

## Что внутри

- `crates/lab_05_xor/src/domain/xor.rs` — функция `xor_stream` (инволюция).
- `crates/lab_05_xor/src/presentation/cli.rs` — clap-CLI.

## Запуск

```bash
# Демо: стих Блока, ключ K=70
cargo run --release -p lab_05_xor -- demo

# Зашифровать произвольную строку
cargo run --release -p lab_05_xor -- encrypt "привет" --key 73

# Расшифровать байты по десятичным кодам
cargo run --release -p lab_05_xor -- decrypt "139 168 ..." --key 73
```

## Тесты

```bash
cargo test -p lab_05_xor
```

Покрытие: инволютивность, многобайтовый ключ, эталонный байт из методички.

## Отчёт

`docs/reports/lab_05_xor/Ковалев Д.П. ВКБ43 5 лаба.docx`
— `python3 scripts/lab_05_xor/build.py`.
