import logging
from math import isnan
from typing import Final

import click
import matplotlib.pyplot as plt
from dishka import FromDishka
from matplotlib.figure import Figure

from mathematical_algorithms_of_geometry_in_cryptography.application.commands.generate_elliptic_curve import (
    GenerateEllipticCurveCommand,
    GenerateEllipticCurveCommandHandler,
)
from mathematical_algorithms_of_geometry_in_cryptography.application.views.elliptic_curve_view import (
    EllipticCurveView,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve.entities.elliptic_curve import (
    EllipticCurve,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@click.group(name="elliptic-curve")
def elliptic_curve_group() -> None:
    """Группа команд для работы с эллиптическими кривыми."""


def _convert_curve_to_view(curve: EllipticCurve) -> EllipticCurveView:
    """Преобразовать EllipticCurve в View."""
    upper_points_data = [
        {"x": p.x, "y": p.y} for p in curve.upper_branch_points
    ]
    lower_points_data = [
        {"x": p.x, "y": p.y} for p in curve.lower_branch_points
    ]

    return EllipticCurveView(
        a=curve.parameters.a,
        b=curve.parameters.b,
        discriminant=curve.discriminant,
        singularity_status=curve.singularity_status,
        is_singular=curve.is_singular,
        upper_branch_points=tuple(upper_points_data),
        lower_branch_points=tuple(lower_points_data),
    )


def _plot_curve(view: EllipticCurveView, output_path: str | None = None) -> None:
    """
    Plot the elliptic curve using matplotlib.
    
    Args:
        view: The view containing curve data
        output_path: Optional path to save the plot
    """
    # Extract x and y coordinates
    upper_x = [p["x"] for p in view.upper_branch_points]
    upper_y = [p["y"] for p in view.upper_branch_points]
    lower_x = [p["x"] for p in view.lower_branch_points]
    lower_y = [p["y"] for p in view.lower_branch_points]

    # Create figure
    fig: Figure = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)

    # Determine title based on singularity
    if view.is_singular:
        title = f"Эллиптическая кривая (СИНГУЛЯРНАЯ) y² = x³ + {view.a}x + {view.b}"
    else:
        title = f"Эллиптическая кривая (НЕСИНГУЛЯРНАЯ) y² = x³ + {view.a}x + {view.b}"

    # Plot upper and lower branches
    ax.plot(upper_x, upper_y, "b-", label="Верхняя ветвь", linewidth=1.5)
    ax.plot(lower_x, lower_y, "b-", label="Нижняя ветвь", linewidth=1.5)

    # Set title and labels
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel("x", fontsize=12)
    ax.set_ylabel("y", fontsize=12)

    # Add grid
    ax.grid(True, alpha=0.3)

    # Add subtitle with discriminant info
    if view.discriminant < 0:
        disc_symbol = "<"
    elif view.discriminant > 0:
        disc_symbol = ">"
    else:
        disc_symbol = "="

    subtitle = f"дискриминант {disc_symbol} 0"
    ax.text(
        0.5,
        0.98,
        subtitle,
        transform=ax.transAxes,
        fontsize=12,
        fontweight="bold",
        ha="center",
        va="top",
    )

    # Set equal aspect ratio
    ax.set_aspect("equal", adjustable="box")

    # Add legend
    ax.legend(loc="best")

    # Adjust layout
    plt.tight_layout()

    # Save or show
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        logger.info("График сохранен в файл: %s", output_path)
    else:
        plt.show()


@elliptic_curve_group.command(name="generate")
@click.option(
    "-a",
    "--a",
    required=True,
    help="Коэффициент a",
    type=float,
)
@click.option(
    "-b",
    "--b",
    required=True,
    help="Коэффициент b",
    type=float,
)
@click.option(
    "--x-min",
    default=-2.0,
    help="Минимальное значение x (по умолчанию: -2.0)",
    type=float,
)
@click.option(
    "--x-max",
    default=2.0,
    help="Максимальное значение x (по умолчанию: 2.0)",
    type=float,
)
@click.option(
    "--step",
    default=0.00001,
    help="Шаг для генерации точек (по умолчанию: 0.00001)",
    type=float,
)
@click.option(
    "-o",
    "--output",
    default=None,
    help="Путь для сохранения графика (опционально)",
    type=str,
)
def cmd_generate_handler(
    a: float,
    b: float,
    x_min: float,
    x_max: float,
    step: float,
    output: str | None,
    interactor: FromDishka[GenerateEllipticCurveCommandHandler],
) -> None:
    """Сгенерировать эллиптическую кривую y² = x³ + ax + b и построить график."""
    # Валидация входных параметров
    if x_min >= x_max:
        click.echo("x_min должно быть меньше x_max", err=True)
        return

    if step <= 0:
        click.echo("Шаг должен быть положительным", err=True)
        return

    # Создаем команду
    command: GenerateEllipticCurveCommand = GenerateEllipticCurveCommand(
        a=a,
        b=b,
        x_min=x_min,
        x_max=x_max,
        step=step,
    )

    try:
        # Выполняем команду
        curve: EllipticCurve = interactor(command)

        # Преобразуем в View
        view: EllipticCurveView = _convert_curve_to_view(curve)

        # Выводим информацию о кривой
        click.echo("\n" + "=" * 60)
        click.echo("Результаты анализа эллиптической кривой")
        click.echo("=" * 60)
        click.echo(f"Уравнение: y² = x³ + {view.a}x + {view.b}")
        click.echo(f"Дискриминант Δ = 4a³ + 27b² = {view.discriminant}")
        click.echo(f"Статус: {'СИНГУЛЯРНАЯ' if view.is_singular else 'НЕСИНГУЛЯРНАЯ'}")

        upper_valid = [p for p in view.upper_branch_points if not isnan(p["y"])]
        lower_valid = [p for p in view.lower_branch_points if not isnan(p["y"])]
        click.echo(f"Количество точек: верхняя ветвь={len(upper_valid)}, нижняя ветвь={len(lower_valid)}")
        click.echo("=" * 60 + "\n")

        # Строим график
        logger.info("Начинается построение графика")
        _plot_curve(view, output_path=output)
        logger.info("График успешно построен")

    except Exception as e:
        click.echo(f"Ошибка при генерации кривой: {e}", err=True)
        logger.exception("Ошибка при генерации эллиптической кривой")
        raise

