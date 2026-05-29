# КДБ8 — Метод Куттера-Джордана-Боссена

Стеганография в неподвижных изображениях через модуляцию синего канала
пропорционально яркости пикселя. Метод эксплуатирует пониженную
чувствительность зрения к синей составляющей.

## Алгоритм

**Встраивание (бит → пиксель):**

1. Псевдослучайно выбираются пиксели-носители (общий seed у отправителя
   и получателя).
2. Для каждого выбранного пикселя считается яркость по BT.601:
   `Y = 0.299·R + 0.587·G + 0.114·B`.
3. Синий канал изменяется на `±λ·Y`: бит «1» → `B' = B + λ·Y`,
   бит «0» → `B' = B − λ·Y`. Значения насыщаются в диапазоне 0–255.

**Извлечение:**

1. Тем же seed восстанавливается порядок пикселей-носителей.
2. Для каждого пикселя считается среднее значение синего канала по
   крестообразной окрестности (4 соседа на radius = 1).
3. Бит = 1, если синий пикселя больше среднего соседей; иначе бит = 0.

Сообщение хранится с 32-битным префиксом длины в байтах.

## Запуск

```bash
uv sync --extra dev

# встроить
./.venv/bin/steganography kutter-jordan-bossen embed \
    -s "КДБ работает!" -l 0.2 --seed 7 \
    -c resources/bmp_samples/sample_smooth_128.bmp \
    -o /tmp/kjb.bmp

# извлечь
./.venv/bin/steganography kutter-jordan-bossen extract \
    -l 0.2 --seed 7 -c /tmp/kjb.bmp
```

Опции:

| Опция | Значение по умолчанию | Описание |
|------|----------------------|----------|
| `-l/--lambda-factor` | `0.1` | Сила модуляции синего, доля от яркости |
| `--seed` | `42` | Seed PRNG выбора пикселей |

**Замечание о применимости:** метод работает корректно на относительно
гладких изображениях (фотографии, градиенты), где соседние пиксели имеют
близкие значения синего. На сильно зашумлённых изображениях извлечение
может давать ошибки — это ограничение алгоритма.

## Сборка docx-отчёта

```bash
./.venv/bin/python scripts/kutter_jordan_bossen/build.py
```

Результат: `docs/reports/2025/8/КДБ8.docx`.

## Тесты

```bash
./.venv/bin/python -m pytest \
    tests/unit/domain/kutter_jordan_bossen \
    tests/integration/kutter_jordan_bossen
```

## Архитектура

- `domain/common/bmp/` — общее с ПР6/ПР7.
- `domain/kutter_jordan_bossen/services/`:
  - `luminance_calculator.py` — формула BT.601.
  - `pixel_selector.py` — PRNG-выбор пикселей-носителей.
  - `kjb_embedder.py` — модуляция синего канала на `±λ·Y`.
  - `kjb_extractor.py` — извлечение по сравнению с соседями.
- `domain/kutter_jordan_bossen/value_objects/` — `KjbParameters`, `KjbStats`.
- `application/commands/kutter_jordan_bossen/{embed,extract}.py` — async Command Handlers.
- `presentation/cli/handlers/kutter_jordan_bossen.py` — click-команды
  `embed`/`extract` через dishka.
