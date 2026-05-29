# ПР6 — LSB-стеганография в BMP с шифрованием Виженера

Программа встраивает текстовое сообщение в 24-битный BMP-контейнер,
шифруя его модифицированным шифром Виженера и оборачивая метками
начала/конца, как описано в методичке (вариант Mathcad-реализации).

## Запуск

```bash
uv sync --extra dev

# встроить
./.venv/bin/steganography lsb-bmp-vigenere embed \
    -s "Стеганография защищает данные." \
    -k "MyKey-2025" \
    -c resources/bmp_samples/sample_64.bmp \
    -o /tmp/stego.bmp

# извлечь
./.venv/bin/steganography lsb-bmp-vigenere extract \
    -k "MyKey-2025" -c /tmp/stego.bmp
```

## Сборка docx-отчёта

```bash
./.venv/bin/python scripts/lsb_bmp_vigenere/build.py
```

Результат: `docs/reports/2025/6/ПР6.docx`.

## Тесты

```bash
./.venv/bin/python -m pytest \
    tests/unit/domain/lsb_bmp_vigenere tests/integration/lsb_bmp_vigenere
```

## Архитектура

- `domain/common/bmp/` — общее с ПР7: `Pixel`, `BmpImage`, `BmpReader`, `BmpWriter`.
- `domain/lsb_bmp_vigenere/services/`:
  - `vigenere_cipher.py` — модифицированный Виженер по байтам (mod 256).
  - `marker_packager.py` — обёртка start/end-марками.
  - `lsb_embedder.py` / `lsb_extractor.py` — запись/чтение бит сообщения в LSB каналов R-G-B.
  - `secret_embedder.py` / `secret_extractor.py` — высокоуровневые операции «зашифровать+встроить» / «извлечь+расшифровать».
- `infrastructure/bmp/` — реализации `BmpReader`/`BmpWriter` через Pillow.
- `application/commands/lsb_bmp_vigenere/{embed,extract}.py` — async Command Handlers.
- `presentation/cli/handlers/lsb_bmp_vigenere.py` — click-команды
  `embed`/`extract` с инжектом через dishka.
