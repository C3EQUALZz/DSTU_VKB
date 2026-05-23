# Лаб 6 — Пороговые схемы Миньотта и Асмут-Блума

## Что внутри

- `crates/lab_06_crt_sharing/src/domain/crt.rs` — Китайская теорема об остатках, модулярная инверсия.
- `crates/lab_06_crt_sharing/src/domain/mignotte.rs` — схема Миньотта (k, n).
- `crates/lab_06_crt_sharing/src/domain/asmuth_bloom.rs` — схема Асмут-Блума.
- `crates/lab_06_crt_sharing/src/domain/encoding.rs` — кодировка буквы как малого секрета.

## Запуск

```bash
cargo run --release -p lab_06_crt_sharing -- variant --variant 1 --k 3 --n 5 --r 7
cargo run --release -p lab_06_crt_sharing -- all
```

## Тесты

```bash
cargo test -p lab_06_crt_sharing
```

Проверяются:
- Пример Миньотта из методички (S=250, basis=[5,7,11,13,17], восстановление по {1,3,5}).
- Пример Асмут-Блума из методички (S=250, q=257, r=15, восстановление по {269, 271, 281}).
- Roundtrip для всех 20 слов варианта.

## Отчёты

`docs/reports/lab_06_crt_sharing/var_NN/` — генератор `python3 scripts/lab_06_crt_sharing/build.py`.
