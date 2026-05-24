"""Отчёт по лаб 4 — тестирование MLP-архитектуры (PyTorch) на классификации фигур."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from report_builder import (  # noqa: E402
    LabMeta,
    add_heading,
    add_image,
    add_listing,
    add_page_break,
    add_para,
    add_qa,
    add_table_simple,
    add_title_page,
    make_doc,
    save,
)

LAB_DIR = ROOT / "4"
SCREENS = ROOT / "docs" / "screenshots" / "lab_04"


def read_source(rel: str) -> str:
    return (LAB_DIR / rel).read_text(encoding="utf-8")


def load_results() -> list[dict]:
    return json.loads((LAB_DIR / "results.json").read_text(encoding="utf-8"))


def find_best(results: list[dict]) -> dict:
    return max(results, key=lambda r: r["accuracy"])


def main() -> None:
    meta = LabMeta(
        number=4,
        title="Тестирование полносвязной архитектуры искусственной нейронной сети",
    )
    doc = make_doc()
    add_title_page(doc, meta)
    add_page_break(doc)

    add_heading(doc, "Тема и цель работы")
    add_para(
        doc,
        "Тема: тестирование полносвязной (Fully-Connected / MLP) архитектуры "
        "искусственной нейронной сети — сравнение конфигураций с разным числом "
        "нейронов в скрытом слое, типом активации и размером батча на задаче "
        "классификации простых геометрических фигур.",
    )
    add_para(
        doc,
        "Цель работы: создать систему компьютерного зрения, определяющую тип "
        "геометрической фигуры (треугольник, круг, квадрат), и провести "
        "серию из 18 экспериментов по подбору гиперпараметров MLP. Дополнительно "
        "— покрыть генератор датасета, конструктор модели и цикл обучения "
        "unit-тестами на pytest.",
    )
    add_para(
        doc,
        "Стек: PyTorch вместо TensorFlow/Keras (по согласованию с преподавателем). "
        "Архитектура от этого не меняется — фреймворк просто заменён на "
        "эквивалентный, для которого нет нужды в TensorFlow на macOS/MPS.",
    )

    # === Что варьируется ===
    add_heading(doc, "Гиперпараметры", level=2)
    add_table_simple(
        doc,
        [
            ["Гиперпараметр", "Значения"],
            ["Число нейронов в скрытом слое", "10, 100, 5000"],
            ["Активация в скрытом слое", "relu, linear"],
            ["batch_size", "10, 100, 1000"],
        ],
        caption="Таблица 1 — варьируемые гиперпараметры (3 × 2 × 3 = 18 экспериментов)",
    )
    add_para(doc, "Метрики, выводимые по каждому эксперименту:")
    add_table_simple(
        doc,
        [
            ["Метрика", "Смысл"],
            ["accuracy", "Доля верно классифицированных тестовых изображений (1.0 = 100%)."],
            ["MSE", "Среднеквадратичная ошибка softmax(logits) против one-hot истинных меток."],
            ["MAE", "Среднеабсолютная ошибка по той же постановке."],
            ["final_train_loss", "Кросс-энтропия на тренировочном батче в последнюю эпоху."],
            ["num_parameters", "Число обучаемых параметров модели."],
            ["elapsed_seconds", "Время одного полного прогона (обучение + оценка)."],
        ],
        caption="Таблица 2 — метрики",
    )

    # === Датасет ===
    add_page_break(doc)
    add_heading(doc, "Датасет")
    add_para(
        doc,
        "В исходном задании предлагалось загрузить датасет из Google Colab. "
        "Чтобы лаба была воспроизводимой и не зависела от внешнего ресурса, "
        "датасет генерируется программно через Pillow (модуль "
        "fourth_laboratory.dataset):",
    )
    add_table_simple(
        doc,
        [
            ["Параметр", "Значение"],
            ["Классы", "circle (0), square (1), triangle (2)"],
            ["Формат изображений", "grayscale 28×28 пикселей (как MNIST)"],
            ["Варьируется", "размер фигуры, положение центра, угол поворота, толщина контура / заливка, шум"],
            ["Размер train", "800 примеров каждого класса (всего 2400)"],
            ["Размер test", "200 примеров каждого класса (всего 600)"],
            ["Детерминизм", "по seed=42 — повторный запуск даёт идентичный датасет"],
        ],
        caption="Таблица 3 — параметры программного датасета",
    )
    add_image(doc, SCREENS / "00_dataset_samples.png", caption="Рисунок 1 — примеры сгенерированных фигур (по 6 каждого класса)")

    # === Архитектура ===
    add_heading(doc, "Архитектура модели", level=2)
    add_listing(
        doc,
        "Input  : (B, 28, 28)\n"
        "Flatten        -> (B, 784)\n"
        "Linear(784, H) -> (B, H)\n"
        "Activation     -> (B, H)        # ReLU или Identity (linear)\n"
        "Linear(H, 3)   -> (B, 3)        # логиты по 3 классам\n",
        caption="Листинг 1 — схема архитектуры ShapeClassifier",
    )
    add_para(
        doc,
        "Число параметров: 784·H + H + H·3 + 3. Для H = 10 это 7 883 параметра, "
        "для H = 100 — 78 803, для H = 5000 — 3 940 003. Функция потерь — "
        "CrossEntropyLoss (включает softmax и NLL). Оптимизатор — Adam, "
        "learning_rate = 1e-3. Эпох — 10.",
    )
    add_image(doc, SCREENS / "05_model_py.png", caption="Рисунок 2 — model.py (ShapeClassifier на PyTorch)")

    # === Результаты ===
    add_page_break(doc)
    add_heading(doc, "Результаты 18 экспериментов")
    add_para(
        doc,
        "Все 18 экспериментов выполнены за единый прогон на устройстве MPS "
        "(Apple Silicon GPU), seed = 42, эпох = 10. Сохранённые в results.json "
        "результаты сведены в таблицу:",
    )
    results = load_results()
    best = find_best(results)

    table_rows: list[list[str]] = [
        ["Hidden", "Activation", "Batch", "Accuracy", "MSE", "MAE", "Final loss", "Params", "Time, s"],
    ]
    for r in results:
        accuracy = r["accuracy"]
        marker = " ★" if r is best else ""
        table_rows.append(
            [
                str(r["hidden_dim"]),
                r["activation"],
                str(r["batch_size"]),
                f"{accuracy:.4f}{marker}",
                f"{r['mse']:.4f}",
                f"{r['mae']:.4f}",
                f"{r['final_train_loss']:.4f}",
                str(r["num_parameters"]),
                f"{r['elapsed_seconds']:.1f}",
            ]
        )
    add_table_simple(doc, table_rows, caption="Таблица 4 — результаты 18 экспериментов (★ — лучший)")

    add_para(
        doc,
        f"Лучшая конфигурация — hidden_dim = {best['hidden_dim']}, "
        f"activation = {best['activation']}, batch_size = {best['batch_size']}: "
        f"accuracy = {best['accuracy']:.4f}, MSE = {best['mse']:.4f}, "
        f"MAE = {best['mae']:.4f}.",
    )

    # === Демо запуска ===
    add_heading(doc, "Демонстрация запуска экспериментов", level=2)
    add_para(
        doc,
        "Скриншот ниже — реальный прогон CLI на уменьшенном датасете "
        "(--epochs 3 --n-train 200 --n-test 80) для демонстрации структуры "
        "вывода. Скрипт по очереди обучает все 18 конфигураций и в одну "
        "строку печатает accuracy/MSE/MAE/время. На штатных 10 эпохах и "
        "n-train = 800 значения совпадают с таблицей выше.",
    )
    add_image(doc, SCREENS / "03_mini_run.png", caption="Рисунок 3 — реальный прогон uv run python -m fourth_laboratory")

    # === Краткие наблюдения ===
    add_page_break(doc)
    add_heading(doc, "Краткие наблюдения")
    add_para(
        doc,
        "ReLU стабильно лучше Linear. На любой ширине слоя и при любом "
        "batch_size ReLU даёт точность выше: разница достигает 19 п.п. "
        "(5000/linear/10 vs 5000/relu/100). Это закономерно: с linear-"
        "активацией двухслойная сеть математически эквивалентна одному "
        "линейному преобразованию, теряя выразительность.",
    )
    add_para(
        doc,
        "Большой слой помогает, но не безусловно. Прирост от 100 → 5000 "
        "нейронов виден только в связке с relu и batch_size = 100. Малый "
        "batch_size = 10 с 5000 нейронами проигрывает 100-нейронной сети с "
        "тем же batch (0.8267 против 0.8500) — слишком много шума градиента "
        "на огромных весах.",
    )
    add_para(
        doc,
        "Большой batch_size = 1000 стабильно проигрывает. При наших 2400 "
        "примерах батч в 1000 — это всего 2–3 шага оптимизатора за эпоху, "
        "чего недостаточно. Лучше всего работает batch_size = 100 (3–4 "
        "десятка шагов на эпоху, при этом градиент достаточно стабилен).",
    )
    add_para(
        doc,
        "Главный вывод по тестированию архитектуры: качество MLP-сети "
        "существенно зависит от взаимодействия всех трёх гиперпараметров, "
        "а не от каждого по отдельности. Перебор в духе эксперимента нужен "
        "именно потому, что наивная подстановка «больше нейронов = выше "
        "точность» не выполняется.",
    )

    # === Тестирование ===
    add_page_break(doc)
    add_heading(doc, "Unit-тестирование (pytest)")
    add_para(
        doc,
        "Всего 40 unit-тестов в трёх группах. Все три модуля проекта "
        "(dataset, model, train) покрыты отдельно — это и есть «тестирование "
        "архитектуры», заявленное в цели лабораторной.",
    )
    add_table_simple(
        doc,
        [
            ["Файл", "Тестов", "Что проверяется"],
            ["test_dataset.py", "15", "Формы и dtype массивов, диапазон значений, наличие фигуры на изображении, балансировка train, детерминированность по seed."],
            ["test_model.py", "19", "Конструкция всех 6 комбинаций (3 размеров × 2 активации), валидация некорректных размеров и неизвестных активаций, формы выхода, корректные классы активаций, точная формула числа параметров для каждой ширины."],
            ["test_train.py", "6", "Конечность и диапазон метрик evaluate, факт убывания train-loss за 5 эпох, точность выше случайного уровня (>0.5 на 3-х классах), запись num_parameters, воспроизводимость по seed."],
        ],
        caption="Таблица 5 — структура тестового набора (40 тестов)",
    )

    add_image(doc, SCREENS / "01_pytest_summary.png", caption="Рисунок 4 — успешный прогон uv run pytest (40 passed)")
    add_para(
        doc,
        "Подробный отчёт по каждому тесту модели — иллюстрирует, как "
        "@parametrize даёт отдельный test item на каждую комбинацию "
        "гиперпараметров (показано 19 тестов test_model.py):",
    )
    add_image(doc, SCREENS / "02_pytest_model.png", caption="Рисунок 5 — подробный прогон test_model.py -v (19 тестов)")

    # === Листинги ===
    add_page_break(doc)
    add_heading(doc, "Листинги исходного кода")
    add_image(doc, SCREENS / "04_dataset_py.png", caption="Рисунок 6 — dataset.py (генератор фигур через Pillow)")
    add_image(doc, SCREENS / "06_train_py.png", caption="Рисунок 7 — train.py (цикл обучения + evaluate)")
    add_image(doc, SCREENS / "07_experiments_py.png", caption="Рисунок 8 — experiments.py (перебор 18 конфигураций)")
    add_image(doc, SCREENS / "08_test_model_py.png", caption="Рисунок 9 — test_model.py (тесты архитектуры)")

    # === Контрольные вопросы ===
    add_page_break(doc)
    add_heading(doc, "Контрольные вопросы")
    QA = [
        (
            "Чем полносвязная (Fully-Connected / Dense) архитектура отличается от свёрточной (CNN)?",
            "В FC-сети каждый нейрон следующего слоя соединён со всеми нейронами "
            "предыдущего, поэтому число параметров слоя — input_dim × hidden_dim "
            "(для H = 5000 на 28×28 входе это уже ~3.94 млн весов). CNN использует "
            "локальные фильтры с разделяемыми весами, которые проходят по всему "
            "изображению (translation invariance), и pooling-слои для понижения "
            "размерности. На задачах компьютерного зрения CNN на порядки эффективнее "
            "по числу параметров и качеству, но FC-сеть проще и подходит для "
            "учебного анализа.",
        ),
        (
            "Почему linear-активация двухслойной сети эквивалентна одному линейному преобразованию?",
            "Если activation = identity, то y = W₂·(W₁·x + b₁) + b₂ = (W₂·W₁)·x + "
            "(W₂·b₁ + b₂), что является аффинным преобразованием с матрицей весов "
            "W₂·W₁. То есть какой бы ширины ни был скрытый слой, выразительная "
            "сила такой сети не превышает одного линейного слоя. Нелинейность "
            "(ReLU, sigmoid, tanh) разрывает эту цепочку и позволяет аппроксимировать "
            "сложные нелинейные функции (теорема универсального аппроксиматора).",
        ),
        (
            "Зачем при ReLU использовать инициализацию Kaiming/He, а не обычную нормальную?",
            "PyTorch для nn.Linear по умолчанию делает Kaiming uniform с "
            "a = √5 — это рассчитано на ReLU. Простая Gaussian (μ = 0, σ = 0.01) "
            "приводит к экспоненциальному затуханию активаций при глубокой сети: "
            "после ReLU исчезает половина (отрицательные значения), и пройдя "
            "несколько слоёв сигнал угасает. Kaiming-инициализация компенсирует "
            "эту потерю фактором √(2/fan_in), сохраняя дисперсию выходов слоёв.",
        ),
        (
            "Почему слишком большой batch_size может ухудшить качество?",
            "Большой батч даёт точную оценку градиента, но за эпоху делается мало "
            "шагов оптимизатора (для 2400 примеров батч 1000 — это всего 2–3 шага). "
            "Меньшие батчи дают шумный градиент, что (а) даёт регуляризующий эффект "
            "(не зацикливаемся в локальном минимуме) и (б) даёт больше итераций "
            "Adam на ту же эпоху. Эмпирически для большинства задач оптимум — "
            "batch_size в районе 32–128.",
        ),
        (
            "Что такое MSE и MAE на выходе классификатора, и почему именно softmax-вектор сравнивается с one-hot?",
            "Для задачи многоклассовой классификации модель выдаёт логиты (логарифмы "
            "ненормированных вероятностей). После softmax(logits) получается вектор "
            "вероятностей принадлежности к каждому классу. One-hot истинной метки — "
            "это вектор-индикатор. MSE = mean(||softmax - one_hot||²) и MAE = "
            "mean(||softmax - one_hot||₁) измеряют, насколько уверенно модель указала "
            "именно правильный класс — в отличие от accuracy, который смотрит только "
            "на argmax. Это типовые метрики calibration / confidence качества.",
        ),
    ]
    for i, (q, a) in enumerate(QA, start=1):
        add_qa(doc, i, q, a)

    # === Выводы ===
    add_page_break(doc)
    add_heading(doc, "Выводы")
    add_para(
        doc,
        "Реализована полносвязная MLP-архитектура на PyTorch — эквивалент "
        "Dense → Activation → Dense из Keras. Подготовлен воспроизводимый "
        "программный генератор датасета через Pillow, что снимает зависимость "
        "от внешнего Google Drive. Проведены все 18 экспериментов по заданию, "
        "результаты сведены в таблицу.",
    )
    add_para(
        doc,
        f"Лучшее значение accuracy — {best['accuracy']:.4f}, при hidden = "
        f"{best['hidden_dim']} / {best['activation']} / batch_size = "
        f"{best['batch_size']}. Подтверждены типовые наблюдения теории "
        "машинного обучения: (1) ReLU существенно лучше линейной активации в "
        "скрытом слое; (2) больший слой помогает только при «здоровом» режиме "
        "обучения (умеренный batch_size); (3) слишком большие батчи режут "
        "число шагов оптимизатора и ухудшают результат.",
    )
    add_para(
        doc,
        "Покрытие unit-тестами включает корректность форм, типов, шейпов и "
        "базовую обучаемость модели — 40 тестов в 3 файлах. Все тесты "
        "проходят за 3.4 с на CPU. Это и есть «тестирование архитектуры», "
        "заявленное в цели лабораторной.",
    )

    # === Полный листинг ===
    add_page_break(doc)
    add_heading(doc, "Полный листинг исходного кода")
    for caption, rel in [
        ("Листинг 2 — src/fourth_laboratory/dataset.py", "src/fourth_laboratory/dataset.py"),
        ("Листинг 3 — src/fourth_laboratory/model.py", "src/fourth_laboratory/model.py"),
        ("Листинг 4 — src/fourth_laboratory/train.py", "src/fourth_laboratory/train.py"),
        ("Листинг 5 — src/fourth_laboratory/experiments.py", "src/fourth_laboratory/experiments.py"),
        ("Листинг 6 — src/fourth_laboratory/__main__.py", "src/fourth_laboratory/__main__.py"),
        ("Листинг 7 — tests/unit/test_dataset.py", "tests/unit/test_dataset.py"),
        ("Листинг 8 — tests/unit/test_model.py", "tests/unit/test_model.py"),
        ("Листинг 9 — tests/unit/test_train.py", "tests/unit/test_train.py"),
    ]:
        add_listing(doc, read_source(rel), caption=caption)

    out = ROOT / "docs" / "reports" / "lab_04" / "Ковалев Д.П. ВКБ43 4 лаба.docx"
    save(doc, out)
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
