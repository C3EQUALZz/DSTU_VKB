# Лабораторная работа №2

**Дисциплина:** Методы тестирования и отладки программного обеспечения
**Тема:** знакомство с библиотекой `pytest`. Проектирование тестов и
поиск логических ошибок в коде.

---

## Условие

На рисунке 1 приведена реализация функции определения типа треугольника.
Функция принимает значения трёх сторон треугольника и возвращает его тип.

**Исходный код функции (по заданию):**

```python
def classify_triangle(a, b, c):
    """
    Классифицирует треугольник по трём сторонам.
    Возвращает:
        - "Equilateral"  : равносторонний
        - "Isosceles"    : равнобедренный (но не равносторонний)
        - "Scalene"      : разносторонний
        - "InvalidInput" : недопустимый ввод (<= 0 или не int)
    """
    # Проверка типа и положительности
    if not all(isinstance(side, int) for side in (a, b, c)):
        return "InvalidInput"
    if any(side <= 0 for side in (a, b, c)):
        return "InvalidInput"
    # Определение типа
    if a == b == c:
        return "Равносторонний"
    elif a == b or b == c or a == c:
        return "Равнобедренный"
    else:
        return "Разносторонний"


if __name__ == "__main__":
    print(classify_triangle(7, 7, 14))
```

**Задачи:**

1. Что необходимо добавить в данную функцию, чтобы учесть все возможные
   варианты входных данных и обеспечить корректность работы функции?
   *Подсказка: не каждый набор входных значений относится к треугольнику.*
2. Реализовать данную функцию с учётом необходимых исправлений.
3. Установить библиотеку `pytest` и составить полный набор тест-кейсов
   по данной задаче.

---

## Задание 1 — какие дефекты есть и что нужно добавить

В исходной реализации обнаруживается **три** логических дефекта:

### Дефект 1 (главный) — отсутствует проверка неравенства треугольника

Геометрически треугольник существует только тогда, когда сумма длин
любых двух сторон **строго больше** длины третьей стороны:

```
a + b > c   и   a + c > b   и   b + c > a
```

В оригинальной функции этой проверки нет. На примере из задания —
`classify_triangle(7, 7, 14)` — возвращается `"Равнобедренный"`,
хотя:

* `7 + 7 = 14`, что **не** строго больше `14`.
* Геометрически точки лежат на одной прямой (вырожденный треугольник).

То же справедливо для `(1, 2, 10)`, `(5, 5, 10)`, `(100, 1, 1)` и
любых других «несуществующих» наборов: функция выдаёт ложно-валидный
ответ вместо `"InvalidInput"`.

**Что добавить:**

```python
if a + b <= c or a + c <= b or b + c <= a:
    return "InvalidInput"
```

Знак `<=` важен: равенство (`a + b == c`) даёт вырожденный треугольник
с нулевой площадью, который тоже нельзя классифицировать как обычный.

### Дефект 2 — рассогласование docstring и реальных return-значений

`docstring` обещает возвращать английские строки:

| Тип        | По docstring  | Фактически возвращается |
|------------|---------------|-------------------------|
| Равносторонний | `Equilateral`  | `Равносторонний`        |
| Равнобедренный | `Isosceles`    | `Равнобедренный`        |
| Разносторонний | `Scalene`      | `Разносторонний`        |

Это типичная «двойственность» спецификации: либо нужно менять
docstring, либо менять реализацию. В лабораторной приводим реализацию в
соответствие с docstring (английские строки) — так контракт остаётся
тем же, что был задокументирован.

### Дефект 3 — `bool` пропускается как валидный `int`

В Python `bool` — подкласс `int`, поэтому
`isinstance(True, int) == True`. Из-за этого `classify_triangle(True, True, True)`
без претензий возвращает «равносторонний» с длинами сторон `1, 1, 1`.
С точки зрения семантики «длина стороны треугольника» — это
некорректный ввод.

**Что добавить:** явная фильтрация `bool` **до** проверки `isinstance(..., int)`:

```python
for side in (a, b, c):
    if isinstance(side, bool) or not isinstance(side, int):
        return "InvalidInput"
```

### Сводная таблица дефектов

| № | Дефект | Демонстрация | Класс ошибки |
|---|--------|--------------|--------------|
| 1 | Нет неравенства треугольника | `(7,7,14) → "Равнобедренный"` вместо `InvalidInput` | Пропущенная валидация (missing case) |
| 2 | Несогласованность docstring/реализации | `(5,5,5) → "Равносторонний"`, обещано `"Equilateral"` | Spec/impl mismatch |
| 3 | `bool` проходит как `int` | `(True, True, True) → "Равносторонний"` | Слишком слабая проверка типа |

---

## Задание 2 — исправленная реализация

Полный код — в [`src/second_laboratory/triangle.py`](src/second_laboratory/triangle.py):

```python
from typing import Literal

TriangleKind = Literal["Equilateral", "Isosceles", "Scalene", "InvalidInput"]


def classify_triangle(a: int, b: int, c: int) -> TriangleKind:
    # 1. Тип: только int, bool явно отвергаем
    for side in (a, b, c):
        if isinstance(side, bool) or not isinstance(side, int):
            return "InvalidInput"

    # 2. Положительность сторон
    if a <= 0 or b <= 0 or c <= 0:
        return "InvalidInput"

    # 3. Неравенство треугольника
    if a + b <= c or a + c <= b or b + c <= a:
        return "InvalidInput"

    # 4. Классификация
    if a == b == c:
        return "Equilateral"
    if a == b or b == c or a == c:
        return "Isosceles"
    return "Scalene"
```

Оригинальная (дефектная) версия сохранена в
[`src/second_laboratory/legacy.py`](src/second_laboratory/legacy.py) —
для наглядного сравнения и для тестов-«пугалок».

---

## Задание 3 — набор тест-кейсов в pytest

Все тесты — в каталоге `tests/unit/`. Текущий набор: **69 тестов**.

### Структура

| Файл | Что проверяет |
|------|---------------|
| `tests/unit/test_triangle.py` | Основные тесты исправленной функции |
| `tests/unit/test_legacy_fault.py` | Фиксирует наблюдаемые дефекты оригинала + сравнение с фиксом |

### Классы тестов в `test_triangle.py`

| Класс | Покрытие |
|-------|----------|
| `TestEquilateral` | `(s,s,s)` для разных `s` — от 1 до 10⁶ |
| `TestIsosceles` | две равные стороны во всех 3 позициях (`a==b`, `b==c`, `a==c`) |
| `TestScalene` | пифагоровы тройки и обычные разносторонние |
| `TestInvalidType` | строки, float, None, list, object, bool в 3 положениях |
| `TestNonPositive` | нули и отрицательные числа в каждой позиции |
| `TestTriangleInequality` | вырожденные (`a+b==c`) и невозможные (`a+b<c`) во всех 3 положениях |
| `TestArgumentOrderInvariance` | результат не зависит от порядка аргументов (все 6 перестановок) |
| `TestBoundary` | минимальный треугольник `(1,1,1)`, очень большие числа `10⁹`, smoke-table |

Параметризация делается через `@pytest.mark.parametrize`, что даёт
компактный код и подробный отчёт по каждому случаю отдельно.

### Тесты дефектов оригинала (`test_legacy_fault.py`)

Эти тесты **закрепляют** наблюдаемое неправильное поведение оригинальной
функции и показывают, что исправленная версия его не повторяет:

```python
def test_77_14_legacy_returns_isosceles():
    assert legacy_classify(7, 7, 14) == "Равнобедренный"  # фактический баг

def test_77_14_fixed_returns_invalid():
    assert fixed_classify(7, 7, 14) == "InvalidInput"     # корректное поведение
```

Так каждый дефект из таблицы выше превращается в пару тестов «есть в
legacy / исправлено в triangle».

---

## Установка и запуск

### Требования

| Инструмент | Версия |
|------------|--------|
| Python | **3.14+** (указано в `.python-version`) |
| [`uv`](https://docs.astral.sh/uv/) | актуальная |

### 1. Установка `uv`

macOS / Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Через Homebrew:

```bash
brew install uv
```

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Проверка:

```bash
uv --version
```

### 2. Клонирование и переход в каталог лабы

```bash
git clone https://github.com/C3EQUALZz/DSTU_VKB.git
cd DSTU_VKB/testing_and_debugging_methods/2025/2
```

### 3. Установка зависимостей

`uv` сам поставит Python 3.14, создаст виртуальное окружение `.venv/`
и подтянет `pytest`:

```bash
uv sync
```

Что произойдёт:
* установится Python 3.14 (если ещё не установлен);
* создастся `.venv/`;
* установится `pytest` (из `dependency-groups.dev`);
* в режиме editable установится сам пакет `second_laboratory`.

### 4. Запуск всех тестов

```bash
uv run pytest
```

Ожидаемый вывод:

```
69 passed in 0.03s
```

### 5. Полезные варианты запуска

Подробный вывод по каждому кейсу:

```bash
uv run pytest -v
```

Запуск **только** тестов исправленной функции (без legacy):

```bash
uv run pytest tests/unit/test_triangle.py
```

Запуск **только** тестов, демонстрирующих дефекты оригинала:

```bash
uv run pytest tests/unit/test_legacy_fault.py -v
```

Запуск одного конкретного класса:

```bash
uv run pytest tests/unit/test_triangle.py::TestTriangleInequality -v
```

Запуск одного конкретного теста:

```bash
uv run pytest tests/unit/test_triangle.py::TestEquilateral::test_minimum_equilateral
```

Фильтрация по имени (substring match):

```bash
uv run pytest -k "inequality" -v
```

С покрытием (потребует `pytest-cov` — поставить можно через
`uv add --dev pytest-cov`):

```bash
uv run pytest --cov=second_laboratory --cov-report=term-missing
```

### 6. Прямой запуск функции

После `uv sync` доступен импорт пакета:

```bash
uv run python -c "from second_laboratory import classify_triangle; print(classify_triangle(7, 7, 14))"
# InvalidInput

uv run python -m second_laboratory.triangle
# InvalidInput
# Scalene
# Equilateral
# Isosceles

uv run python -m second_laboratory.legacy
# Равнобедренный   ← демонстрация fault на примере из задания
```

---

## Структура проекта

```
2025/2/
├── pyproject.toml                          ← uv + setuptools + pytest config
├── .python-version                         ← 3.14
├── README.md                               ← этот файл
├── Лаб. работа №2.pdf                      ← оригинал задания
├── src/
│   └── second_laboratory/
│       ├── __init__.py                     ← реэкспорт classify_triangle
│       ├── triangle.py                     ← исправленная функция
│       └── legacy.py                       ← оригинал из задания (для сравнения)
└── tests/
    ├── __init__.py
    └── unit/
        ├── __init__.py
        ├── test_triangle.py                ← основной набор тестов
        └── test_legacy_fault.py            ← тесты, демонстрирующие fault legacy
```

---

## Выводы

1. **Главный пропущенный случай в коде из задания** — неравенство
   треугольника. Без его проверки функция принимает на вход
   вырожденные и попросту несуществующие треугольники и возвращает
   ложно-валидный тип. Демонстрация прямо из условия задачи —
   `classify_triangle(7, 7, 14)` возвращает `"Равнобедренный"`.
2. Помимо главного дефекта в коде есть ещё две менее очевидные
   проблемы: расхождение docstring и фактических возвращаемых
   значений и слишком слабая проверка типа (`bool` пропускается как
   `int`).
3. Исправленная функция (`second_laboratory.triangle.classify_triangle`)
   полностью соответствует docstring, корректно отсекает все
   некорректные входы и проходит **69 pytest-тестов**, включая
   тесты, фиксирующие исходные дефекты.
4. `pytest` через `uv` устанавливается одной командой `uv sync` и
   позволяет компактно описать большой набор кейсов через
   параметризацию.
