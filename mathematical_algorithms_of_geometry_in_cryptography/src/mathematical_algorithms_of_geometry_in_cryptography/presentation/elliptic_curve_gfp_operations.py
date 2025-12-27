import logging
from typing import Final

import click
from dishka import FromDishka
from prettytable import PrettyTable

from mathematical_algorithms_of_geometry_in_cryptography.application.commands.elliptic_curve_gfp_operations import (
    AddPointsCommand,
    AddPointsCommandHandler,
    DoublePointCommand,
    DoublePointCommandHandler,
    GenerateEllipticCurveGFpCommand,
    GenerateEllipticCurveGFpCommandHandler,
    MultiplyPointCommand,
    MultiplyPointCommandHandler,
)
from mathematical_algorithms_of_geometry_in_cryptography.application.views.elliptic_curve_gfp_view import (
    EllipticCurveGFpView,
    PointOperationView,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.entities.elliptic_curve_gfp import (
    EllipticCurveGFp,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.errors.elliptic_curve_gfp_errors import (
    PointNotOnCurveError,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.values.gfp_point import (
    GFpPoint,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@click.group(name="elliptic-curve-gfp")
def elliptic_curve_gfp_group() -> None:
    """Группа команд для работы с эллиптическими кривыми над GF(p)."""


def _convert_curve_to_view(curve: EllipticCurveGFp) -> EllipticCurveGFpView:
    """Преобразовать EllipticCurveGFp в View."""
    points_data = [{"x": p.x, "y": p.y, "str": str(p)} for p in curve.points]

    return EllipticCurveGFpView(
        a=curve.parameters.a,
        b=curve.parameters.b,
        p=int(curve.parameters.p),
        order=curve.order,
        points=tuple(points_data),
    )


@elliptic_curve_gfp_group.command(name="generate")
@click.option(
    "-a",
    "--a",
    required=True,
    help="Коэффициент a",
    type=int,
)
@click.option(
    "-b",
    "--b",
    required=True,
    help="Коэффициент b",
    type=int,
)
@click.option(
    "-p",
    "--p",
    required=True,
    help="Простое число p (характеристика поля)",
    type=int,
)
def cmd_generate_handler(
    a: int,
    b: int,
    p: int,
    interactor: FromDishka[GenerateEllipticCurveGFpCommandHandler],
) -> None:
    """Сгенерировать эллиптическую кривую y² = x³ + ax + b над GF(p) и найти все точки."""
    # Валидация входных параметров
    if p <= 1:
        click.echo("p должно быть простым числом больше 1", err=True)
        return

    if a < 0 or a >= p:
        click.echo(f"Коэффициент a должен быть в диапазоне [0, {p-1}]", err=True)
        return

    if b < 0 or b >= p:
        click.echo(f"Коэффициент b должен быть в диапазоне [0, {p-1}]", err=True)
        return

    # Создаем команду
    command: GenerateEllipticCurveGFpCommand = GenerateEllipticCurveGFpCommand(
        a=a,
        b=b,
        p=p,
    )

    try:
        # Выполняем команду
        curve: EllipticCurveGFp = interactor(command)

        # Преобразуем в View
        view: EllipticCurveGFpView = _convert_curve_to_view(curve)

        # Выводим информацию о кривой
        click.echo("\n" + "=" * 60)
        click.echo("Результаты генерации эллиптической кривой над GF(p)")
        click.echo("=" * 60)
        click.echo(f"Уравнение: y² = x³ + {view.a}x + {view.b} над GF({view.p})")
        click.echo(f"Порядок кривой: {view.order}")
        click.echo(f"Количество точек: {view.order}")
        click.echo("=" * 60 + "\n")

        # Выводим таблицу точек
        points_table: PrettyTable = PrettyTable()
        points_table.title = "Точки эллиптической кривой"
        points_table.field_names = ["№", "Точка", "x", "y"]
        for idx, point_data in enumerate(view.points, start=1):
            points_table.add_row(
                [
                    idx,
                    point_data["str"],
                    point_data["x"] if point_data["x"] != -1 else "∞",
                    point_data["y"] if point_data["y"] != -1 else "∞",
                ],
            )

        click.echo(points_table)

    except Exception as e:
        click.echo(f"Ошибка при генерации кривой: {e}", err=True)
        logger.exception("Ошибка при генерации эллиптической кривой над GF(p)")
        raise


@elliptic_curve_gfp_group.command(name="add")
@click.option(
    "-a",
    "--a",
    required=True,
    help="Коэффициент a",
    type=int,
)
@click.option(
    "-b",
    "--b",
    required=True,
    help="Коэффициент b",
    type=int,
)
@click.option(
    "-p",
    "--p",
    required=True,
    help="Простое число p",
    type=int,
)
@click.option(
    "--px",
    required=True,
    help="x-координата точки P",
    type=int,
)
@click.option(
    "--py",
    required=True,
    help="y-координата точки P",
    type=int,
)
@click.option(
    "--qx",
    required=True,
    help="x-координата точки Q",
    type=int,
)
@click.option(
    "--qy",
    required=True,
    help="y-координата точки Q",
    type=int,
)
def cmd_add_handler(
    a: int,
    b: int,
    p: int,
    px: int,
    py: int,
    qx: int,
    qy: int,
    generate_interactor: FromDishka[GenerateEllipticCurveGFpCommandHandler],
    add_interactor: FromDishka[AddPointsCommandHandler],
) -> None:
    """Вычислить P + Q для точек на эллиптической кривой над GF(p)."""
    try:
        # Сначала генерируем кривую
        generate_command = GenerateEllipticCurveGFpCommand(a=a, b=b, p=p)
        curve: EllipticCurveGFp = generate_interactor(generate_command)

        # Выполняем сложение
        add_command = AddPointsCommand(
            curve=curve,
            p_x=px,
            p_y=py,
            q_x=qx,
            q_y=qy,
        )
        result: GFpPoint = add_interactor(add_command)

        # Выводим результат
        click.echo("\n" + "=" * 60)
        click.echo("Результат сложения точек")
        click.echo("=" * 60)
        click.echo(f"P = ({px}, {py})")
        click.echo(f"Q = ({qx}, {qy})")
        click.echo(f"P + Q = {result}")
        click.echo("=" * 60 + "\n")

    except PointNotOnCurveError as e:
        click.echo(f"Ошибка: {e}", err=True)
        raise
    except Exception as e:
        click.echo(f"Ошибка при сложении точек: {e}", err=True)
        logger.exception("Ошибка при сложении точек")
        raise


@elliptic_curve_gfp_group.command(name="double")
@click.option(
    "-a",
    "--a",
    required=True,
    help="Коэффициент a",
    type=int,
)
@click.option(
    "-b",
    "--b",
    required=True,
    help="Коэффициент b",
    type=int,
)
@click.option(
    "-p",
    "--p",
    required=True,
    help="Простое число p",
    type=int,
)
@click.option(
    "--px",
    required=True,
    help="x-координата точки P",
    type=int,
)
@click.option(
    "--py",
    required=True,
    help="y-координата точки P",
    type=int,
)
def cmd_double_handler(
    a: int,
    b: int,
    p: int,
    px: int,
    py: int,
    generate_interactor: FromDishka[GenerateEllipticCurveGFpCommandHandler],
    double_interactor: FromDishka[DoublePointCommandHandler],
) -> None:
    """Вычислить 2P (удвоение точки) на эллиптической кривой над GF(p)."""
    try:
        # Сначала генерируем кривую
        generate_command = GenerateEllipticCurveGFpCommand(a=a, b=b, p=p)
        curve: EllipticCurveGFp = generate_interactor(generate_command)

        # Выполняем удвоение
        double_command = DoublePointCommand(
            curve=curve,
            p_x=px,
            p_y=py,
        )
        result: GFpPoint = double_interactor(double_command)

        # Выводим результат
        click.echo("\n" + "=" * 60)
        click.echo("Результат удвоения точки")
        click.echo("=" * 60)
        click.echo(f"P = ({px}, {py})")
        click.echo(f"2P = {result}")
        click.echo("=" * 60 + "\n")

    except PointNotOnCurveError as e:
        click.echo(f"Ошибка: {e}", err=True)
        raise
    except Exception as e:
        click.echo(f"Ошибка при удвоении точки: {e}", err=True)
        logger.exception("Ошибка при удвоении точки")
        raise


@elliptic_curve_gfp_group.command(name="multiply")
@click.option(
    "-a",
    "--a",
    required=True,
    help="Коэффициент a",
    type=int,
)
@click.option(
    "-b",
    "--b",
    required=True,
    help="Коэффициент b",
    type=int,
)
@click.option(
    "-p",
    "--p",
    required=True,
    help="Простое число p",
    type=int,
)
@click.option(
    "--px",
    required=True,
    help="x-координата точки P",
    type=int,
)
@click.option(
    "--py",
    required=True,
    help="y-координата точки P",
    type=int,
)
@click.option(
    "-m",
    "--multiplier",
    required=True,
    help="Множитель m (для вычисления mP)",
    type=int,
)
def cmd_multiply_handler(
    a: int,
    b: int,
    p: int,
    px: int,
    py: int,
    multiplier: int,
    generate_interactor: FromDishka[GenerateEllipticCurveGFpCommandHandler],
    multiply_interactor: FromDishka[MultiplyPointCommandHandler],
) -> None:
    """Вычислить mP (скалярное умножение точки) на эллиптической кривой над GF(p)."""
    # Валидация входных параметров
    if multiplier <= 0:
        click.echo("Множитель должен быть положительным", err=True)
        return

    try:
        # Сначала генерируем кривую
        generate_command = GenerateEllipticCurveGFpCommand(a=a, b=b, p=p)
        curve: EllipticCurveGFp = generate_interactor(generate_command)

        # Выполняем скалярное умножение
        multiply_command = MultiplyPointCommand(
            curve=curve,
            p_x=px,
            p_y=py,
            multiplier=multiplier,
        )
        result: GFpPoint = multiply_interactor(multiply_command)

        # Выводим результат
        click.echo("\n" + "=" * 60)
        click.echo("Результат скалярного умножения точки")
        click.echo("=" * 60)
        click.echo(f"P = ({px}, {py})")
        click.echo(f"{multiplier}P = {result}")
        click.echo("=" * 60 + "\n")

    except PointNotOnCurveError as e:
        click.echo(f"Ошибка: {e}", err=True)
        raise
    except Exception as e:
        click.echo(f"Ошибка при скалярном умножении точки: {e}", err=True)
        logger.exception("Ошибка при скалярном умножении точки")
        raise


