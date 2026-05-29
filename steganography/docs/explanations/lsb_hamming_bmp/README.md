# ПР7 — Стеганография изображений: LSB-R / LSB-M / Хемминг (15,11)

Три метода встраивания текстового сообщения в 24-битный BMP-контейнер:

1. **LSB-Replacement** — классическая замена младшего бита канала битом сообщения. Параметр `--step` задаёт шаг (1 = каждый канал, 4 = каждый четвёртый, и т. д.).
2. **LSB-Matching** — мягкий вариант: при несовпадении LSB значение канала меняется на ±1 (статистически менее заметно для гистограммного стегоанализа).
3. **Hamming (15,11)** — стег-код: в блок из 15 LSB вкладывается 4 бита сообщения с искажением максимум одного канала.

Сообщение хранится с 32-битным префиксом длины (в битах), что позволяет точно знать, сколько байт читать при извлечении.

## Запуск

```bash
uv sync --extra dev

# LSB-R
./.venv/bin/steganography lsb-hamming-bmp embed -s "Тест" -m lsb-r \
    -c resources/bmp_samples/sample_64.bmp -o /tmp/lsbr.bmp
./.venv/bin/steganography lsb-hamming-bmp extract -m lsb-r -c /tmp/lsbr.bmp

# LSB-M (мягкая модификация)
./.venv/bin/steganography lsb-hamming-bmp embed -s "Тест" -m lsb-m \
    -c resources/bmp_samples/sample_64.bmp -o /tmp/lsbm.bmp

# Хемминг (15,11) — низкий уровень искажений
./.venv/bin/steganography lsb-hamming-bmp embed -s "Тест" -m hamming-15-11 \
    -c resources/bmp_samples/sample_64.bmp -o /tmp/ham.bmp
```

Поддерживаемые опции:

| Опция | Значения |
|-------|----------|
| `-m/--method` | `lsb-r`, `lsb-m`, `hamming-15-11` |
| `--step` | положительное целое, шаг по каналам (для LSB-R/M; для Хемминг игнорируется) |

## Сборка docx-отчёта

```bash
./.venv/bin/python scripts/lsb_hamming_bmp/build.py
```

Результат: `docs/reports/2025/7/ПР7.docx`.

## Тесты

```bash
./.venv/bin/python -m pytest \
    tests/unit/domain/lsb_hamming_bmp tests/integration/lsb_hamming_bmp
```

## Архитектура

- `domain/common/bmp/` — общее с ПР6.
- `domain/lsb_hamming_bmp/services/`:
  - `channel_stream.py` — BmpImage ↔ list[int] каналов.
  - `lsb_replacement_method.py` — LSB-R с задаваемым шагом.
  - `lsb_matching_method.py` — LSB-M с детерминированным RNG.
  - `hamming_15_11_method.py` — синдромный код Хемминга (15,11).
- `domain/lsb_hamming_bmp/value_objects/`:
  - `embedding_method.py` — Enum `lsb-r` / `lsb-m` / `hamming-15-11`.
  - `embedding_stats.py` — payload_bits, capacity_bits, changed_channels, rate, distortion.
- `application/commands/lsb_hamming_bmp/{embed,extract}.py` — Command Handlers, выбирающие метод по enum.
- `presentation/cli/handlers/lsb_hamming_bmp.py` — `embed`/`extract` через dishka.
