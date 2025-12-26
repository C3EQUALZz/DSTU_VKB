import click
from dishka import FromDishka
from prettytable import PrettyTable

from mathematical_algorithms_of_geometry_in_cryptography.application.commands.find_divisor import (
    FindDivisorCommand,
    FindDivisorCommandHandler,
)
from mathematical_algorithms_of_geometry_in_cryptography.application.views.pollard_rho_test_view import (
    PollardRhoTestView,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.entities.pollard_rho_test import (
    PollardRhoTest,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.errors.pollard_rho_errors import (
    DivisorNotFoundError,
    FunctionEvaluationError,
)


@click.group(name="pollard-rho")
def pollard_rho_test_group() -> None:
    """Группа команд для метода Полларда."""


def _convert_test_to_view(test: PollardRhoTest) -> PollardRhoTestView:
    """Преобразовать PollardRhoTest в View."""
    steps_data = []
    for step in test.steps:
        step_dict = {
            "step_number": step.step_number,
            "a": step.a,
            "b": step.b,
            "d": step.d,
        }
        steps_data.append(step_dict)

    return PollardRhoTestView(
        number=int(test.number),
        initial_value=int(test.initial_value),
        function_expression=str(test.function_expression),
        steps_count=test.steps_count,
        is_complete=test.is_complete,
        divisor=test.divisor,
        steps=tuple(steps_data),
    )


@pollard_rho_test_group.command(name="find-divisor")
@click.option(
    "-n",
    "--number",
    required=True,
    help="Число для поиска делителя",
    type=int,
)
@click.option(
    "-c",
    "--initial-value",
    required=True,
    help="Начальное значение c",
    type=int,
)
@click.option(
    "-f",
    "--function",
    required=True,
    help="Выражение для функции f(x), где x - переменная (например: x^2 + 1)",
    type=str,
)
def cmd_find_divisor_handler(
    number: int,
    initial_value: int,
    function: str,
    interactor: FromDishka[FindDivisorCommandHandler],
) -> None:
    """Найти нетривиальный делитель заданного числа методом Полларда."""
    # Валидация входных параметров
    if number <= 1:
        click.echo("Число должно быть больше 1", err=True)
        return

    if initial_value < 0:
        click.echo("Начальное значение должно быть неотрицательным", err=True)
        return

    if not function or not function.strip():
        click.echo("Функция не может быть пустой", err=True)
        return

    if "x" not in function.lower():
        click.echo("Функция должна содержать переменную 'x'", err=True)
        return

    # Создаем команду
    command: FindDivisorCommand = FindDivisorCommand(
        number=number,
        initial_value=initial_value,
        function_expression=function,
    )

    try:
        # Выполняем команду
        test: PollardRhoTest = interactor(command)

        # Преобразуем в View
        view: PollardRhoTestView = _convert_test_to_view(test)

        # Выводим основную таблицу с результатами
        main_table: PrettyTable = PrettyTable()
        main_table.title = "Результат алгоритма Полларда"
        main_table.field_names = [
            "Число",
            "Начальное значение",
            "Функция",
            "Шагов выполнено",
            "Завершен",
            "Делитель",
        ]
        main_table.add_row(
            [
                view.number,
                view.initial_value,
                view.function_expression,
                view.steps_count,
                "Да" if view.is_complete else "Нет",
                view.divisor if view.divisor is not None else "Не найден",
            ],
        )

        click.echo(main_table)

        # Выводим детальную таблицу для каждого шага
        if view.steps:
            click.echo("\nДетальные результаты шагов:")
            for step in view.steps:
                step_table: PrettyTable = PrettyTable()
                step_table.title = f"Шаг {step['step_number']}"
                step_table.field_names = ["Параметр", "Значение"]
                step_table.add_row(["a", step["a"]])
                step_table.add_row(["b", step["b"]])
                step_table.add_row(["d", step["d"]])

                click.echo(step_table)

    except DivisorNotFoundError as e:
        click.echo(f"Делитель не найден: {e}", err=True)
        raise
    except FunctionEvaluationError as e:
        click.echo(f"Ошибка при вычислении функции: {e}", err=True)
        raise
    except Exception as e:
        click.echo(f"Ошибка при выполнении алгоритма: {e}", err=True)
        raise

