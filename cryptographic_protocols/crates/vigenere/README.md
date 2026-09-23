# Шифр Виженера

Один Rust crate для трёх схем построения ключа:

- `standard` повторяет исходный ключ;
- `progressive` увеличивает сдвиг после каждого полного блока ключа;
- `autokey` после исходного ключа использует буквы открытого текста.

Алфавиты: `en` (26 латинских букв), `ru-yo` (33 русские буквы с отдельной Ё), `ru-no-yo` (32 русские буквы и `_` для пробела; Ё приводится к Е). Знаки вне алфавита копируются без расходования ключа. Буквы другого алфавита отклоняются. Для `ru-no-yo` результат приводится к верхнему регистру, поскольку знак `_` не хранит регистр зашифрованной буквы.

```bash
cargo run -p vigenere -- encrypt --scheme progressive --alphabet en --key MODE --text CRYPTOGRAPHY
cargo run -p vigenere -- decrypt --scheme progressive --alphabet en --key MODE --text OFBTGDKWOFME
cargo run -p vigenere -- encrypt --scheme standard --alphabet ru-yo --key КЛЮЧ --text КРИПТОГРАФИЯ
cargo run -p vigenere -- encrypt --scheme autokey --alphabet ru-yo --key КЛЮЧ --text КРИПТОГРАФИЯ
```

`break` восстанавливает наиболее вероятный начальный ключ и открытый текст по шифротексту. Он доступен для всех трёх схем и алфавитов:

```bash
cargo run -p vigenere -- break ШИФРОТЕКСТ --scheme standard --alphabet ru-no-yo --min-key 2 --max-key 8
```

Оценка в результате — среднее логарифмическое правдоподобие по встроенной модели букв и биграмм; больше означает более вероятный текст. Криптоанализ статистический: короткий или нетипичный текст может дать неверный ключ. Английская модель получена из [Alice's Adventures in Wonderland, Project Gutenberg #11](https://www.gutenberg.org/ebooks/11), русские модели — из `artifacts/lab_04_vigenere/corpus_ru.txt`. Модели воспроизводятся скриптом `scripts/vigenere/generate_language_model.py`.

Отчёт 2026 года: `docs/reports/2026/vigenere/Ковалев Д.П. ВКБ43 1 лаба.docx`. Генератор: `python3 scripts/vigenere/build.py`.
