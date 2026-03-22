# Лабораторная работа №3 — Анализ текстовой информации с применением ИНС

**Цель:** классификация позитивных и негативных отзывов людей по использованию автомобиля Tesla.

**Результат:** точность на проверочной выборке — **87–88%** (целевой диапазон 85–90%).

## Содержание

- [Установка и запуск](#установка-и-запуск)
- [Архитектура проекта](#архитектура-проекта)
- [Ход выполнения работы](#ход-выполнения-работы)
- [Результаты](#результаты)
- [CLI-команды](#cli-команды)

---

## Установка и запуск

```bash
# 1. Установить зависимости
uv sync
# или
pip install -e .

# 2. Полный пайплайн: скачивание + обучение
text-analyzer pipeline

# 3. Оценка обученной модели
text-analyzer evaluate

# 4. Генерация графиков для отчёта
text-analyzer visualize
```

### Требования

- Python >= 3.12
- PyTorch >= 2.10.0
- macOS (MPS), Linux (CUDA) или CPU

---

## Архитектура проекта

Проект построен по принципам **Clean Architecture** с инверсией зависимостей через **Dishka** (IoC-контейнер).

```
src/text_analyzer/
├── domain/                          # Доменный слой (чистый Python, без зависимостей)
│   ├── entities.py                  # Review — доменная сущность отзыва
│   ├── value_objects.py             # Sentiment (StrEnum), ReviewText (frozen dataclass)
│   └── errors.py                    # DomainError, EmptyReviewTextError
│
├── application/                     # Слой приложения (юзкейсы, порты)
│   ├── dto.py                       # TrainingConfig, TrainingResult, EvaluationResult
│   ├── ports/                       # Интерфейсы к инфраструктуре (Protocol)
│   │   ├── dataset_downloader.py    # Загрузка датасета
│   │   ├── dataset_loader.py        # Чтение отзывов из файлов
│   │   ├── text_preprocessor.py     # Токенизация и кодирование текста
│   │   ├── classifier.py            # Обучение и инференс модели
│   │   └── visualizer.py            # Построение графиков
│   └── commands/                    # Обработчики команд (CQRS-pattern)
│       ├── download_dataset.py      # DownloadDatasetCommandHandler
│       ├── train_model.py           # TrainModelCommandHandler
│       ├── evaluate_model.py        # EvaluateModelCommandHandler
│       └── visualize.py             # VisualizeCommandHandler
│
├── infrastructure/                  # Инфраструктурный слой (реализации портов)
│   ├── http_downloader.py           # httpx — загрузка и распаковка ZIP-архива
│   ├── file_dataset_loader.py       # Чтение .txt файлов, автодетект класса по имени
│   ├── simple_preprocessor.py       # Токенизатор: слова + bigrams + char n-grams
│   ├── pytorch_classifier.py        # TF-IDF + FeedForward NN (PyTorch)
│   └── matplotlib_visualizer.py     # Графики: loss, accuracy, confusion matrix
│
├── presentation/                    # Слой представления
│   └── cli.py                       # Click CLI + Dishka (FromDishka, @inject)
│
└── setup/                           # Сборка приложения
    └── container.py                 # Dishka: InfrastructureProvider + ApplicationProvider
```

### Принцип работы DI (Dishka)

```
presentation/cli.py
    └─ setup_dishka(container, context)
         └─ FromDishka[TrainModelCommandHandler]  — инъекция в Click-команду
              └─ ApplicationProvider.train_handler(loader, preprocessor, classifier)
                   └─ InfrastructureProvider.classifier() → PytorchSentimentClassifier
```

Зависимости текут **внутрь**: `presentation → application → domain`. Инфраструктура реализует порты, определённые в `application/ports/`.

---

## Ход выполнения работы

### 1. Загрузка базы данных

Датасет скачивается по ссылке Yandex Cloud и распаковывается из ZIP-архива:

```bash
text-analyzer download
```

Содержит 2 файла:
| Файл | Класс | Количество отзывов |
|------|-------|--------------------|
| `Позитивный отзыв.txt` | Positive | 2191 |
| `Негативный отзыв.txt` | Negative | 1188 |

Каждая строка — один отзыв на русском языке (комментарии из соцсетей о Tesla).

### 2. Подготовка данных

**Балансировка классов** — oversampling (дублирование) минорного класса (negative: 1188 → 2191):

| Этап               | Positive | Negative | Всего |
|--------------------|----------|----------|-------|
| Исходные данные    | 2191     | 1188     | 3379  |
| После балансировки | 2191     | 2191     | 4382  |
| Train (80%)        | ~1752    | ~1753    | 3505  |
| Validation (20%)   | ~439     | ~438     | 877   |

> **Почему oversampling, а не undersampling?** При undersampling (1188 + 1188 = 2376) теряется ~46% позитивных отзывов. Oversampling сохраняет все уникальные данные и увеличивает обучающую выборку на 84%.

### 3. Извлечение признаков (Feature Engineering)

**Токенизация** — комбинированная стратегия:
1. **Word unigrams**: `"тесла топ"` → `["тесла", "топ"]`
2. **Word bigrams**: `"тесла топ"` → `["w_тесла_топ"]`
3. **Character n-grams (2–5)**: `"топ"` → `["c_ т", "c_то", "c_топ", "c_оп ", ...]`

**TF-IDF взвешивание** — поверх Bag-of-Words:
- TF: частота токена в отзыве
- IDF: `log((N+1)/(df+1)) + 1` (сглаженная обратная документная частота)
- L2-нормализация результирующих векторов

Размерность словаря: **40 000 токенов** (из 96 450 уникальных).

### 4. Архитектура нейронной сети

**Feedforward Neural Network** на TF-IDF признаках:

```
Input: TF-IDF vector (dim=40000)
  ↓
Linear(40000, 128)
  ↓
ReLU → Dropout(0.3)
  ↓
Linear(128, 1)
  ↓
Sigmoid → {0: Negative, 1: Positive}
```

- **Loss**: BCEWithLogitsLoss (бинарная кросс-энтропия)
- **Optimizer**: AdamW (lr=0.003, weight_decay=0.01)
- **Scheduler**: CosineAnnealingLR (T_max=30, eta_min=1e-5)
- **Параметров**: 5 120 257

### 5. Обучение

```bash
text-analyzer train --epochs 30
```

Модель обучается на MPS (Apple Silicon) / CUDA / CPU. Лучшие веса сохраняются автоматически (early stopping по val accuracy).

---

## Результаты

### Итоговые метрики

| Метрика                | Значение   |
|------------------------|------------|
| **Accuracy**           | **87.80%** |
| **Best epoch**         | 5 / 30     |
| **Train loss (final)** | 0.004      |
| **Val loss (best)**    | 0.359      |

### Confusion Matrix

|                   | Predicted Negative | Predicted Positive |
|-------------------|--------------------|--------------------|
| **True Negative** | 393 (44.8%)        | 45 (5.1%)          |
| **True Positive** | 62 (7.1%)          | 377 (43.0%)        |

- **Precision** (Positive): 377 / (377+45) = 89.3%
- **Recall** (Positive): 377 / (377+62) = 85.9%
- **F1-score** (Positive): 87.6%

### Графики

Все графики генерируются командой:
```bash
text-analyzer visualize --output-dir plots
```

Генерируются 4 файла:
- `plots/dataset_distribution.png` — распределение классов до и после балансировки
- `plots/review_lengths.png` — гистограмма длин отзывов + статистика
- `plots/training_curves.png` — кривые loss и accuracy по эпохам
- `plots/confusion_matrix.png` — матрица ошибок

---

## CLI-команды

| Команда                   | Описание                       |
|---------------------------|--------------------------------|
| `text-analyzer download`  | Скачать и распаковать датасет  |
| `text-analyzer train`     | Обучить модель                 |
| `text-analyzer evaluate`  | Оценить на проверочной выборке |
| `text-analyzer visualize` | Сгенерировать графики          |
| `text-analyzer pipeline`  | Полный цикл: скачать + обучить |

### Параметры обучения

```bash
text-analyzer train \
  --data-dir data \
  --model-dir output \
  --epochs 30 \
  --batch-size 64 \
  --lr 0.003 \
  --max-vocab 40000 \
  --max-seq-len 500 \
  --hidden-dim 128
```

### Пример вывода

```
text-analyzer pipeline --epochs 15

Step 1/2: Downloading dataset...
Dataset ready.

Step 2/2: Training model...
Epoch  1/15 — train_loss: 0.5420, val_loss: 0.3924, val_acc: 82.67%
Epoch  2/15 — train_loss: 0.1945, val_loss: 0.3417, val_acc: 85.06%
Epoch  3/15 — train_loss: 0.0709, val_loss: 0.3223, val_acc: 87.80%
...
Epoch 15/15 — train_loss: 0.0035, val_loss: 0.4380, val_acc: 87.00%

=== Pipeline Complete ===
Best validation accuracy: 87.80%
Best epoch: 3
```

---

## Стек технологий

| Компонент     | Технология                   |
|---------------|------------------------------|
| ML Framework  | PyTorch                      |
| CLI           | Click                        |
| IoC Container | Dishka                       |
| HTTP Client   | httpx                        |
| Visualization | matplotlib                   |
| Architecture  | Clean Architecture, CQRS, DI |
