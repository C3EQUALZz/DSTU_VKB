"""
Лабораторная работа №1
Тестирование полносвязной архитектуры искусственной нейронной сети

Задание: Классификация геометрических фигур (треугольник, круг, квадрат)
с использованием полносвязной нейронной сети (PyTorch).

Эксперименты:
  - Количество нейронов: 10, 100, 5000
  - Активационная функция: relu, linear
  - Размер batch_size: 10, 100, 1000
"""

import os
import zipfile

import gdown
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from PIL import Image
from sklearn.model_selection import train_test_split
from tabulate import tabulate
from torch.utils.data import DataLoader, TensorDataset

# ─── Параметры ───────────────────────────────────────────────────────
IMG_HEIGHT = 20
IMG_WIDTH = 20
CLASS_COUNT = 3
CLASS_NAMES = ["Треугольник", "Круг", "Квадрат"]
EPOCHS = 30
LEARNING_RATE = 0.001
RANDOM_STATE = 42

# Гиперпараметры для перебора
NEURONS_LIST = [10, 100, 5000]
ACTIVATIONS = ["relu", "linear"]
BATCH_SIZES = [10, 100, 1000]


# ─── 1. Загрузка и подготовка датасета ────────────────────────────────
def download_dataset(data_dir: str = "hw_light") -> str:
    """Скачивает и распаковывает архив с датасетом."""
    zip_path = "hw_light.zip"

    if not os.path.isdir(data_dir):
        if not os.path.isfile(zip_path):
            print("⏬  Загрузка датасета из Yandex Cloud…")
            gdown.download(
                "https://storage.yandexcloud.net/aiueducation/Content/base/l3/hw_light.zip",
                zip_path,
                quiet=False,
            )
        print("📦  Распаковка архива…")
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(".")
        print("✅  Датасет готов!\n")
    else:
        print("✅  Датасет уже существует.\n")

    return data_dir


def load_images(base_dir: str) -> tuple[np.ndarray, np.ndarray]:
    """
    Загружает изображения из папок датасета.
    Структура: base_dir/0/..., base_dir/3/..., base_dir/...
      - Папка '0' → класс 0 (треугольник)
      - Папка '3' → класс 1 (круг)
      - Остальные  → класс 2 (квадрат)
    """
    x_data: list[np.ndarray] = []
    y_data: list[int] = []

    for folder in sorted(os.listdir(base_dir)):
        folder_path = os.path.join(base_dir, folder)
        if not os.path.isdir(folder_path):
            continue

        for img_name in os.listdir(folder_path):
            img_path = os.path.join(folder_path, img_name)
            try:
                img = Image.open(img_path).convert("L")  # grayscale
                img = img.resize((IMG_WIDTH, IMG_HEIGHT))
                img_arr = np.array(img, dtype=np.float32) / 255.0
                x_data.append(img_arr.flatten())
            except Exception:
                continue

            if folder == "0":
                y_data.append(0)
            elif folder == "3":
                y_data.append(1)
            else:
                y_data.append(2)

    return np.array(x_data), np.array(y_data)


# ─── 2. Определение модели ────────────────────────────────────────────
class ShapeClassifier(nn.Module):
    """
    Полносвязная нейронная сеть с одним скрытым слоем.

    Параметры:
        input_size  – размер входного вектора (20*20 = 400)
        hidden_size – количество нейронов в скрытом слое
        num_classes – количество классов (3)
        activation  – 'relu' или 'linear'
    """

    def __init__(
        self,
        input_size: int,
        hidden_size: int,
        num_classes: int,
        activation: str = "relu",
    ):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, num_classes)
        self.activation = activation

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.fc1(x)
        if self.activation == "relu":
            x = torch.relu(x)
        # при activation == "linear" — без нелинейности
        x = self.fc2(x)
        return x


# ─── 3. Обучение и тестирование ───────────────────────────────────────
def train_model(
    model: nn.Module,
    train_loader: DataLoader,
    criterion: nn.Module,
    optimizer: optim.Optimizer,
    epochs: int,
    device: torch.device,
) -> list[float]:
    """Обучает модель, возвращает историю loss по эпохам."""
    model.train()
    history: list[float] = []

    for epoch in range(epochs):
        running_loss = 0.0
        for x_batch, y_batch in train_loader:
            x_batch, y_batch = x_batch.to(device), y_batch.to(device)
            optimizer.zero_grad()
            outputs = model(x_batch)
            loss = criterion(outputs, y_batch)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * x_batch.size(0)

        epoch_loss = running_loss / len(train_loader.dataset)  # type: ignore[arg-type]
        history.append(epoch_loss)

    return history


@torch.no_grad()
def evaluate_model(
    model: nn.Module,
    test_loader: DataLoader,
    device: torch.device,
) -> float:
    """Вычисляет точность модели на тестовой выборке."""
    model.eval()
    correct = 0
    total = 0

    for x_batch, y_batch in test_loader:
        x_batch, y_batch = x_batch.to(device), y_batch.to(device)
        outputs = model(x_batch)
        _, predicted = torch.max(outputs, 1)
        total += y_batch.size(0)
        correct += (predicted == y_batch).sum().item()

    return correct / total


# ─── 4. Основная логика ───────────────────────────────────────────────
def run_experiment(
    x_train: torch.Tensor,
    y_train: torch.Tensor,
    x_test: torch.Tensor,
    y_test: torch.Tensor,
    hidden_size: int,
    activation: str,
    batch_size: int,
    device: torch.device,
) -> tuple[float, list[float]]:
    """Запускает один эксперимент и возвращает (accuracy, loss_history)."""
    input_size = x_train.shape[1]

    # DataLoader-ы
    train_ds = TensorDataset(x_train, y_train)
    test_ds = TensorDataset(x_test, y_test)
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)

    # Модель, loss, оптимизатор
    model = ShapeClassifier(input_size, hidden_size, CLASS_COUNT, activation).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    # Обучение
    loss_history = train_model(model, train_loader, criterion, optimizer, EPOCHS, device)

    # Оценка
    accuracy = evaluate_model(model, test_loader, device)

    return accuracy, loss_history


def main() -> None:
    # Устройство
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🖥  Устройство: {device}\n")

    # Загрузка данных
    data_dir = download_dataset()
    x_all, y_all = load_images(data_dir)
    print(f"Всего изображений: {len(x_all)}")
    print(f"Размер вектора признаков: {x_all.shape[1]}  ({IMG_HEIGHT}×{IMG_WIDTH})")
    print(f"Классы: {dict(zip(range(CLASS_COUNT), CLASS_NAMES))}\n")

    # Разбиение на train/test
    x_train_np, x_test_np, y_train_np, y_test_np = train_test_split(
        x_all, y_all, test_size=0.2, random_state=RANDOM_STATE
    )
    print(f"Обучающая выборка: {x_train_np.shape[0]} образцов")
    print(f"Тестовая  выборка:  {x_test_np.shape[0]} образцов\n")

    # Конвертация в тензоры
    x_train_t = torch.tensor(x_train_np, dtype=torch.float32)
    x_test_t = torch.tensor(x_test_np, dtype=torch.float32)
    y_train_t = torch.tensor(y_train_np, dtype=torch.long)
    y_test_t = torch.tensor(y_test_np, dtype=torch.long)

    # ── Показываем примеры изображений ──
    fig, axes = plt.subplots(1, 6, figsize=(12, 2))
    fig.suptitle("Примеры изображений из датасета", fontsize=14)
    indices = np.random.RandomState(42).choice(len(x_train_np), 6, replace=False)
    for ax, idx in zip(axes, indices):
        ax.imshow(
            x_train_np[idx].reshape(IMG_HEIGHT, IMG_WIDTH),
            cmap="gray",
        )
        ax.set_title(CLASS_NAMES[y_train_np[idx]], fontsize=10)
        ax.axis("off")
    plt.tight_layout()
    plt.savefig("samples.png", dpi=100, bbox_inches="tight")
    plt.show()

    # ── Серия экспериментов ──
    results: list[dict] = []
    total_experiments = len(NEURONS_LIST) * len(ACTIVATIONS) * len(BATCH_SIZES)
    exp_num = 0

    for neurons in NEURONS_LIST:
        for activation in ACTIVATIONS:
            for batch_size in BATCH_SIZES:
                exp_num += 1
                label = (
                    f"[{exp_num}/{total_experiments}] "
                    f"neurons={neurons}, act={activation}, bs={batch_size}"
                )
                print(f"🔄  {label} …", end=" ", flush=True)

                accuracy, loss_history = run_experiment(
                    x_train_t,
                    y_train_t,
                    x_test_t,
                    y_test_t,
                    hidden_size=neurons,
                    activation=activation,
                    batch_size=batch_size,
                    device=device,
                )

                print(f"accuracy = {accuracy:.4f}")
                results.append(
                    {
                        "Нейроны": neurons,
                        "Активация": activation,
                        "Batch size": batch_size,
                        "Точность (%)": round(accuracy * 100, 2),
                        "loss_history": loss_history,
                    }
                )

    # ── Таблица результатов ──
    print("\n" + "=" * 70)
    print("  РЕЗУЛЬТАТЫ ЭКСПЕРИМЕНТОВ")
    print("=" * 70)

    table_data = [
        [r["Нейроны"], r["Активация"], r["Batch size"], f"{r['Точность (%)']:.2f}%"]
        for r in results
    ]
    headers = ["Нейроны", "Активация", "Batch size", "Точность"]
    print(
        tabulate(
            table_data,
            headers=headers,
            tablefmt="fancy_grid",
            stralign="center",
            numalign="center",
        )
    )

    # ── Графики loss ──
    fig, axes = plt.subplots(
        len(NEURONS_LIST),
        len(ACTIVATIONS),
        figsize=(14, 4 * len(NEURONS_LIST)),
        squeeze=False,
    )
    fig.suptitle("Кривые обучения (Loss) для разных конфигураций", fontsize=16, y=1.02)

    for i, neurons in enumerate(NEURONS_LIST):
        for j, activation in enumerate(ACTIVATIONS):
            ax = axes[i][j]
            for batch_size in BATCH_SIZES:
                # Найти соответствующий результат
                res = next(
                    r
                    for r in results
                    if r["Нейроны"] == neurons
                    and r["Активация"] == activation
                    and r["Batch size"] == batch_size
                )
                ax.plot(
                    res["loss_history"],
                    label=f"bs={batch_size} ({res['Точность (%)']:.1f}%)",
                )
            ax.set_title(f"Нейронов: {neurons}, Активация: {activation}")
            ax.set_xlabel("Эпоха")
            ax.set_ylabel("Loss")
            ax.legend(fontsize=8)
            ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("loss_curves.png", dpi=120, bbox_inches="tight")
    plt.show()

    # ── Столбчатая диаграмма точностей ──
    fig, ax = plt.subplots(figsize=(16, 6))

    labels = [
        f"n={r['Нейроны']}\n{r['Активация']}\nbs={r['Batch size']}"
        for r in results
    ]
    accuracies = [r["Точность (%)"] for r in results]

    colors = []
    for r in results:
        if r["Активация"] == "relu":
            colors.append("#4CAF50")
        else:
            colors.append("#FF9800")

    bars = ax.bar(range(len(accuracies)), accuracies, color=colors, edgecolor="black", linewidth=0.5)

    for bar, acc in zip(bars, accuracies):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f"{acc:.1f}%",
            ha="center",
            va="bottom",
            fontsize=7,
            fontweight="bold",
        )

    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, fontsize=7, ha="center")
    ax.set_ylabel("Точность (%)")
    ax.set_title("Сравнение точности моделей для разных гиперпараметров", fontsize=14)
    ax.set_ylim(0, 105)
    ax.grid(axis="y", alpha=0.3)

    # Легенда
    from matplotlib.patches import Patch

    legend_elements = [
        Patch(facecolor="#4CAF50", edgecolor="black", label="ReLU"),
        Patch(facecolor="#FF9800", edgecolor="black", label="Linear"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=10)

    plt.tight_layout()
    plt.savefig("accuracy_comparison.png", dpi=120, bbox_inches="tight")
    plt.show()

    # ── Лучшая модель ──
    best = max(results, key=lambda r: r["Точность (%)"])
    print(f"\n🏆  Лучшая конфигурация:")
    print(f"    Нейроны:    {best['Нейроны']}")
    print(f"    Активация:  {best['Активация']}")
    print(f"    Batch size: {best['Batch size']}")
    print(f"    Точность:   {best['Точность (%)']:.2f}%")


if __name__ == "__main__":
    torch.manual_seed(RANDOM_STATE)
    np.random.seed(RANDOM_STATE)
    main()

