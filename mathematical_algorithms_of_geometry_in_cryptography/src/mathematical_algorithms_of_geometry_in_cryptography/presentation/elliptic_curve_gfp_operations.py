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
    FindAllOrdersCommand,
    FindAllOrdersCommandHandler,
    FindPointOrderCommand,
    FindPointOrderCommandHandler,
    GenerateEllipticCurveGFpCommand,
    GenerateEllipticCurveGFpCommandHandler,
    GenerateSequenceCommand,
    GenerateSequenceCommandHandler,
    MultiplyPointCommand,
    MultiplyPointCommandHandler,
)
from mathematical_algorithms_of_geometry_in_cryptography.application.views.elliptic_curve_gfp_view import (
    EllipticCurveGFpView,
    PointOperationView,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.values.sequence_result import (
    SequenceResult,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.entities.elliptic_curve_gfp import (
    EllipticCurveGFp,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.errors.elliptic_curve_gfp_errors import (
    PointNotOnCurveError,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.services.elliptic_curve_gfp_service import (
    EllipticCurveGFpService,
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


@elliptic_curve_gfp_group.command(name="order")
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
def cmd_order_handler(
    a: int,
    b: int,
    p: int,
    px: int,
    py: int,
    generate_interactor: FromDishka[GenerateEllipticCurveGFpCommandHandler],
    order_interactor: FromDishka[FindPointOrderCommandHandler],
) -> None:
    """Найти порядок точки P на эллиптической кривой над GF(p)."""
    try:
        # Сначала генерируем кривую
        generate_command = GenerateEllipticCurveGFpCommand(a=a, b=b, p=p)
        curve: EllipticCurveGFp = generate_interactor(generate_command)

        # Выполняем поиск порядка
        order_command = FindPointOrderCommand(
            curve=curve,
            p_x=px,
            p_y=py,
        )
        order: int = order_interactor(order_command)

        # Выводим результат
        click.echo("\n" + "=" * 60)
        click.echo("Результат поиска порядка точки")
        click.echo("=" * 60)
        click.echo(f"P = ({px}, {py})")
        click.echo(f"Порядок точки P: {order}")
        click.echo("=" * 60 + "\n")

    except PointNotOnCurveError as e:
        click.echo(f"Ошибка: {e}", err=True)
        raise
    except Exception as e:
        click.echo(f"Ошибка при поиске порядка точки: {e}", err=True)
        logger.exception("Ошибка при поиске порядка точки")
        raise


@elliptic_curve_gfp_group.command(name="all-orders")
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
def cmd_all_orders_handler(
    a: int,
    b: int,
    p: int,
    generate_interactor: FromDishka[GenerateEllipticCurveGFpCommandHandler],
    all_orders_interactor: FromDishka[FindAllOrdersCommandHandler],
) -> None:
    """Найти порядки всех точек на эллиптической кривой над GF(p)."""
    try:
        # Сначала генерируем кривую
        generate_command = GenerateEllipticCurveGFpCommand(a=a, b=b, p=p)
        curve: EllipticCurveGFp = generate_interactor(generate_command)

        # Выполняем поиск порядков
        all_orders_command = FindAllOrdersCommand(curve=curve)
        orders: dict[GFpPoint, int] = all_orders_interactor(all_orders_command)

        # Выводим результат
        click.echo("\n" + "=" * 60)
        click.echo("Порядки точек ЭК:")
        click.echo("=" * 60)

        orders_table: PrettyTable = PrettyTable()
        orders_table.field_names = ["Точка", "Порядок"]
        for point, order in sorted(orders.items(), key=lambda x: (x[0].x, x[0].y)):
            orders_table.add_row([str(point), order])

        click.echo(orders_table)
        click.echo("=" * 60 + "\n")

    except Exception as e:
        click.echo(f"Ошибка при поиске порядков точек: {e}", err=True)
        logger.exception("Ошибка при поиске порядков точек")
        raise


@elliptic_curve_gfp_group.command(name="generate-sequence")
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
    "-c",
    "--c",
    required=True,
    help="Коэффициент c (множитель)",
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
    "--x0-x",
    required=True,
    help="x-координата начальной точки X0",
    type=int,
)
@click.option(
    "--x0-y",
    required=True,
    help="y-координата начальной точки X0",
    type=int,
)
@click.option(
    "-n",
    "--count",
    required=True,
    help="Количество итераций",
    type=int,
)
def cmd_generate_sequence_handler(
    a: int,
    b: int,
    p: int,
    c: int,
    px: int,
    py: int,
    x0_x: int,
    x0_y: int,
    count: int,
    generate_interactor: FromDishka[GenerateEllipticCurveGFpCommandHandler],
    congruent_interactor: FromDishka[GenerateSequenceCommandHandler],
    inversive_interactor: FromDishka[GenerateSequenceCommandHandler],
    service: FromDishka[EllipticCurveGFpService],
) -> None:
    """Сгенерировать псевдослучайные последовательности конгруэнтным и инверсивным генераторами."""
    # Валидация входных параметров
    if count <= 0:
        click.echo("Количество итераций должно быть положительным", err=True)
        return

    try:
        # Сначала генерируем кривую
        generate_command = GenerateEllipticCurveGFpCommand(a=a, b=b, p=p)
        curve: EllipticCurveGFp = generate_interactor(generate_command)

        # Проверяем условия
        x0 = GFpPoint(x=x0_x, y=x0_y)
        p_point = GFpPoint(x=px, y=py)

        # Проверка: c * X0 + P != X0
        c_x0 = service.multiply_point(curve, x0, c)
        c_x0_plus_p = service.add_points(curve, c_x0, p_point)
        if c_x0_plus_p == x0:
            click.echo("Ошибка: должно выполняться условие c * X0 + P != X0", err=True)
            return

        # Проверка: c * X0^(-1) + P != X0
        x0_inverse = service.reverse_point(curve, x0)
        c_x0_inv = service.multiply_point(curve, x0_inverse, c)
        c_x0_inv_plus_p = service.add_points(curve, c_x0_inv, p_point)
        if c_x0_inv_plus_p == x0:
            click.echo("Ошибка: должно выполняться условие c * X0^(-1) + P != X0", err=True)
            return

        # Генерируем конгруэнтную последовательность
        click.echo("\n" + "=" * 60)
        click.echo("Конгруэнтный генератор")
        click.echo("=" * 60)

        congruent_command = GenerateSequenceCommand(
            curve=curve,
            c=c,
            x0_x=x0_x,
            x0_y=x0_y,
            p_x=px,
            p_y=py,
            count=count,
            is_congruent=True,
        )
        congruent_result: SequenceResult = congruent_interactor(congruent_command)

        click.echo(f"Период: {congruent_result.period}")
        click.echo(f"Двоичная последовательность: {congruent_result.binary_sequence}")

        # Генерируем инверсивную последовательность
        click.echo("\n" + "=" * 60)
        click.echo("Инверсивный генератор:")
        click.echo("=" * 60)

        inversive_command = GenerateSequenceCommand(
            curve=curve,
            c=c,
            x0_x=x0_x,
            x0_y=x0_y,
            p_x=px,
            p_y=py,
            count=count,
            is_congruent=False,
        )
        inversive_result: SequenceResult = inversive_interactor(inversive_command)

        click.echo(f"Период: {inversive_result.period}")
        click.echo(f"Двоичная последовательность: {inversive_result.binary_sequence}")

        # Выводим таблицу сравнения
        click.echo("\n" + "=" * 60)
        click.echo("Таблица сравнения последовательностей")
        click.echo("=" * 60)

        comparison_table: PrettyTable = PrettyTable()
        opt_len = len(str(count - 1)) + 2
        comparison_table.field_names = ["i", "КГ", "ИГ"]

        max_len = max(len(congruent_result.sequence), len(inversive_result.sequence))
        for i in range(max_len):
            kg_str = (
                congruent_result.sequence[i]["str"]
                if i < len(congruent_result.sequence)
                else "-"
            )
            ig_str = (
                inversive_result.sequence[i]["str"]
                if i < len(inversive_result.sequence)
                else "-"
            )
            comparison_table.add_row([i, kg_str, ig_str])

        click.echo(comparison_table)
        click.echo("=" * 60 + "\n")

    except PointNotOnCurveError as e:
        click.echo(f"Ошибка: {e}", err=True)
        raise
    except Exception as e:
        click.echo(f"Ошибка при генерации последовательностей: {e}", err=True)
        logger.exception("Ошибка при генерации последовательностей")
        raise


