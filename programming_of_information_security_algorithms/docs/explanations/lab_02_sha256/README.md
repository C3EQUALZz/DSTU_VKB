# Лаб 2 — SHA-2-256

**Crate:** `crates/lab_02_sha256`
**Статус:** ✅ готова — **24 теста** (16 unit/property/векторы NIST в `domain`, 3 в `infrastructure`, 7 интеграционных CLI + 1 doctest); clippy clean; **результат побайтово совпадает с системным `shasum -a 256`** и формат файла читается им через `shasum -c`

## Что покрыто

| Уровень | Источник | Тесты |
|---------|----------|-------|
| Domain | NIST §B.1 (`abc`), `""`, §B.2 (`abcdbcdec...nopq` 56 байт), 64 'a', 1M 'a' (single-shot и streaming через 1024-байтные чанки) | 5 + 2 граничных (55/56 байт) + 2 hex round-trip |
| Property | streaming↔one-shot при случайном разбиении на куски, длина 32 байта, hex round-trip | 3 propertest'а |
| Infrastructure | save/load .sha256 round-trip, совместимость с coreutils-форматом, пустой файл → ошибка | 3 |
| CLI integration | хеш `abc`, запись в shasum-формате (2 пробела), `verify` совпадение → exit 0, изменение файла → exit ≠ 0 + `MISMATCH`, парсинг coreutils-файла, 5 MiB файл стримится корректно, `--help` | 7 |

Тестовые векторы сверены с **системным `shasum -a 256`** на macOS — четыре совпадают побайтово (включая 1M 'a').

## Условие

> Реализовать для произвольного текстового файла расчёт значения хеш на основании алгоритма SHA-2-256.
> Полученное значение хеш записать в отдельный файл. В реализации алгоритма **не использовать сторонние библиотеки, выполняющие вычисление хеш-функций**.
> Реализовать проверку на совпадение значения хеш для произвольного файла рассчитанного в приложении и прочитанного из ранее сохранённого файла.

Источник: `docs/conditions/Laboratornye_po_kursu_Programmirovanie_algoritmov_zaschity_informatsii.docx`.

## Реализация (план)

Полностью своя реализация по [FIPS 180-4](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf), без `sha2`, `ring`, `digest`.

- `domain::sha256::Sha256` — инкрементальный хешер: `new`, `update(&mut self, &[u8])`, `finalize(self) -> [u8; 32]`.
- Внутри: 64 константы $K$ из FIPS 180-4, 8 начальных значений $H_0$, функции `Ch`, `Maj`, `Σ0`, `Σ1`, `σ0`, `σ1`, padding `0x80 || zeros || u64::to_be_bytes(len_bits)`.
- `application::hash_file` — стримит файл блоками по 64 КБ через `update`. Никогда не читает весь файл в память.
- `application::verify_hash` — сравнивает свежий хеш с прочитанным из файла-эталона. Возвращает `Verdict::Match | Mismatch`.
- `infrastructure::hash_io` — формат файла хеша: одна строка hex lowercase, как у coreutils `sha256sum`, чтобы хеш можно было проверить и сторонним инструментом для уверенности студента: `shasum -a 256 -c file.sha256`.
- `presentation::cli` — `hash <file> [--out <file.sha256>]`, `verify <file> --against <file.sha256>`.

## Как запустить

```bash
# Посчитать хеш и записать
just lab-02 hash README.md --out artifacts/lab_02/readme.sha256

# Проверить (приложение читает .sha256 и сравнивает с пересчитанным значением)
just lab-02 verify README.md --against artifacts/lab_02/readme.sha256

# Внешняя сверка (для уверенности преподавателя)
shasum -a 256 README.md  # должно совпасть с содержимым .sha256
```

## Как протестировать

```bash
cargo test -p lab_02_sha256
```

Тестовые векторы NIST (известные):

| Вход            | Ожидаемый SHA-256                                                  |
|-----------------|--------------------------------------------------------------------|
| `""` (пусто)    | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `"abc"`         | `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` |
| `"abcdbcdec..."` (FIPS 180-4 Annex B.2) | `248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1` |
| 10⁶ × `'a'`     | `cd c7 6e 5c 99 14 fb 92 81 a1 c7 e2 84 d7 3e 67 f1 80 9a 48 a4 97 20 0e 04 6d 39 cc c7 11 2c d0` |

Плюс property-based: `sha256(a || b)` стримом и за один проход — равны.
